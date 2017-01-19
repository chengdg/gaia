# -*- coding: utf-8 -*-
import json

from bdem import msgutil
from eaglet.core import watchdog

from business import model as business_model
from business.product.product import Product
from db.mall import models as mall_models
from eaglet.decorator import param_required
from gaia_conf import TOPIC
from business.product import product_pool
from business.mall.category.category import Category

class UpdateProductService(business_model.Service):
	"""
	商品工厂
	"""
	def __update_product(self, product_id, base_info, image_info, logistics_info, pay_info):
		product = mall_models.Product.update(
			name=base_info.get('name', '').strip(),
			promotion_title=base_info.get('promotion_title', '').strip(),
			bar_code=base_info.get('bar_code', '').strip(),
			thumbnails_url=image_info.get('thumbnails_url', '').strip(),
			pic_url='',
			detail=base_info.get('detail', '').strip(),
			type=base_info.get('type', mall_models.PRODUCT_DEFAULT_TYPE),
			is_use_online_pay_interface=pay_info['is_use_online_pay_interface'],
			is_use_cod_pay_interface=pay_info['is_use_cod_pay_interface'],
			postage_type=logistics_info['postage_type'],
			postage_id=logistics_info.get('postage_id', 0),
			unified_postage_money=logistics_info['unified_postage_money'],
			stocks=base_info.get('min_limit', 0),
			is_member_product=base_info.get('is_member_product', False),
			supplier=base_info.get('supplier_id', 0),
			purchase_price=base_info.get('purchase_price', 0.0),
			is_enable_bill=base_info.get('is_enable_bill', False),
			is_delivery=base_info.get('is_delivery', 'false') == 'true',
			limit_zone_type=int(logistics_info.get('limit_zone_type', '0')),
			limit_zone=int(logistics_info.get('limit_zone_id', '0'))
		).dj_where(owner_id=self.corp.id, id=product_id).execute()
		
		return product

	def __update_product_categories(self, product_id, category_ids):
		"""
		更新商品分组
		"""
		#由于不同渠道创建的代销商品，在ProductCategory表中的product_id，所以这里要筛选出当前公司（渠道）拥有的category，进行选择性删除
		#不能只根据product_id进行删除
		existed_category_ids = [category.id for category in mall_models.ProductCategory.select().dj_where(owner_id=self.corp.id)]
		mall_models.CategoryHasProduct.delete().dj_where(product_id=product_id, category_id__in=existed_category_ids).execute()
		for category_id in category_ids:
			mall_models.CategoryHasProduct.create(
				category = category_id,
				product = product_id
			)

		for category_id in category_ids:
			Category.update_product_count(category_id)

	def __update_standard_model(self, product_id, models_info):
		"""
		更新标准规格
		"""
		is_delete_standard_model = models_info.get('is_use_custom_model', False)
		corp_id = self.corp.id
		if is_delete_standard_model:
			mall_models.ProductModel.update(
				price=0.0,
				weight=0,
				stock_type=mall_models.PRODUCT_STOCK_TYPE_UNLIMIT,
				stocks=-1,
				user_code='',
				purchase_price=0,
				is_deleted=True
			).dj_where(owner_id=corp_id, product_id=product_id, name='standard').execute()
		else:
			standard_model = models_info['standard_model']
			mall_models.ProductModel.update(
				price=standard_model['price'],
				weight=standard_model['weight'],
				stock_type=mall_models.PRODUCT_STOCK_TYPE_UNLIMIT if standard_model['stock_type'] == 'unlimit' else mall_models.PRODUCT_STOCK_TYPE_LIMIT,
				stocks=standard_model['stocks'],
				user_code=standard_model.get('user_code', ''),
				purchase_price=standard_model['purchase_price'],
				is_deleted=False
			).dj_where(owner_id=corp_id, product_id=product_id, name='standard').execute()


	def __add_custom_models(self, product_id, models):
		"""
		添加多个定制规格
		"""
		for custom_model in models:
			product_model = mall_models.ProductModel.create(
				owner=self.corp.id,
				product=product_id,
				name=custom_model['name'],
				is_standard=False,
				price=custom_model['price'],
				weight=custom_model['weight'],
				stock_type=mall_models.PRODUCT_STOCK_TYPE_UNLIMIT if custom_model['stock_type'] == 'unlimit' else mall_models.PRODUCT_STOCK_TYPE_LIMIT,
				stocks=custom_model['stocks'],
				user_code=custom_model['user_code'],
				purchase_price=custom_model['purchase_price']
			)

			for property in custom_model['properties']:
				mall_models.ProductModelHasPropertyValue.create(
					model=product_model,
					property_id=property['property_id'],
					property_value_id=property['property_value_id']
				)

	def __update_existed_custom_models(self, product_id, new_models):
		"""
		更新已存在的多个定制规格
		"""
		for new_model in new_models:
			product_model = mall_models.ProductModel.update(
				price=new_model['price'],
				weight=new_model['weight'],
				stock_type=mall_models.PRODUCT_STOCK_TYPE_UNLIMIT if new_model.get('stock_type', 'limit') == 'unlimit' else mall_models.PRODUCT_STOCK_TYPE_LIMIT,
				stocks=new_model['stocks'],
				user_code=new_model.get('user_code', ''),
				purchase_price=new_model.get('purchase_price', 0.0)
			).dj_where(owner_id=self.corp.id, id=new_model['id']).execute()

	def __delete_custom_models(self, need_delete_ids):
		"""
		根据id删除一组商品规格
		"""
		if not need_delete_ids:
			return

		mall_models.ProductModel.update(is_deleted=True).dj_where(id__in=list(need_delete_ids)).execute()

	def __update_custom_models(self, product_id, models_info):
		"""
		更新定制规格
		"""
		custom_models = models_info['custom_models']
		print custom_models
		existed_models = [model for model in mall_models.ProductModel.select().dj_where(product_id=product_id, is_deleted=False) if not model.is_standard]
		existed_model_ids = set([model.id for model in existed_models])
		if len(custom_models) == 0:
			if len(existed_models) == 0:
				pass
			else:
				#将定制规格全部删除
				need_delete_ids = existed_model_ids
				self.__delete_custom_models(need_delete_ids)
		else:
			model_ids = set([model['id'] for model in custom_models])

			need_add_ids = model_ids - existed_model_ids
			need_delete_ids = existed_model_ids - model_ids
			need_update_ids = model_ids.intersection(existed_model_ids)
			
			need_add_models = []
			need_update_models = []
			for custom_model in custom_models:
				if custom_model['id'] in need_add_ids:
					need_add_models.append(custom_model)
				elif custom_model['id'] in need_update_ids:
					need_update_models.append(custom_model)
				else:
					pass

			self.__add_custom_models(product_id, need_add_models)
			self.__update_existed_custom_models(product_id, need_update_models)
			self.__delete_custom_models(need_delete_ids)

	def __update_product_models(self, product_id, models_info):
		"""
		更新商品规格
		"""
		self.__update_standard_model(product_id, models_info)
		self.__update_custom_models(product_id, models_info)

	def __update_product_images(self, product_id, image_info):
		"""
		更新商品图片
		"""
		images = image_info['images']
		if len(images) == 0:
			return

		mall_models.ProductSwipeImage.delete().dj_where(product=product_id).execute()
		for swipe_image in images:
			if swipe_image['width'] and swipe_image['height']:
				mall_models.ProductSwipeImage.create(
					product=product_id,
					url=swipe_image['url'],
					width=swipe_image['width'],
					height=swipe_image['height']
				)

	def __update_product_properties(self, product_id, properties):
		"""
		更新商品属性
		"""
		if len(properties) == 0:
			return

		mall_models.ProductProperty.delete().dj_where(product_id=product_id).execute()
		for product_property in properties:
			mall_models.ProductProperty.create(
				owner=self.corp.id,
				product=product_id,
				name=product_property['name'],
				value=product_property['value']
			)

	def __update_product_classifications(self, product_id, base_info):
		"""
		更新商品分类
		"""
		classification_id = int(base_info.get('classification_id'))
		if not classification_id:
			return

		classification = self.corp.product_classification_repository.get_product_classification(classification_id)
		classification.add_product(product_id)

	def __send_msg_to_topic(self, product_id, msg_name):
		topic_name = TOPIC['product']
		data = {
			"product_id": product_id,
			"corp_id": self.corp.id
		}
		msgutil.send_message(topic_name, msg_name, data)

	def update_product(self, product_id, args):
		"""
		更新商品
		"""
		base_info = args['base_info']
		models_info = args['models_info']
		image_info = args['image_info']
		logistics_info = args['logistics_info']
		pay_info = args.get('pay_info', {
			'is_use_online_pay_interface': False,
			'is_use_cod_pay_interface': False
		})
		categories = args.get('categories', [])
		properties = args.get('properties', [])

		self.__update_product(product_id, base_info, image_info, logistics_info, pay_info)
		self.__update_product_categories(product_id, categories)
		self.__update_product_images(product_id, image_info)
		self.__update_product_models(product_id, models_info)
		self.__update_product_properties(product_id, properties)
		self.__update_product_classifications(product_id, base_info)
		# 更新缓存
		self.__send_msg_to_topic(product_id, "product_updated")

	def update_product_price(self, product_id, price_infos):
		"""
		更新商品价格
		"""
		for price_info in price_infos:
			model_id = price_info['model_id']
			price = price_info['price']
			mall_models.ProductModel.update(price=price).dj_where(owner_id=self.corp.id, id=model_id).execute()
		# 发送更新缓存的消息
		self.__send_msg_to_topic(product_id, "product_updated")

	def update_product_stock(self, product_id, stock_infos):
		"""
		更新商品库存
		"""
		for stock_info in stock_infos:
			model_id = stock_info['model_id']
			stock_type = mall_models.PRODUCT_STOCK_TYPE_UNLIMIT if stock_info['stock_type'] == 'unlimit' else mall_models.PRODUCT_STOCK_TYPE_LIMIT
			stocks = stock_info['stocks']
			mall_models.ProductModel.update(stock_type=stock_type, stocks=stocks).dj_where(owner_id=self.corp.id, id=model_id).execute()

	def add_product_stock(self, product_id, stock_infos):
		for stock_info in stock_infos:
			model_id = stock_info['model_id']
			changed_count = stock_info['changed_count']

			product_model = mall_models.ProductModel.select().dj_where(id=model_id).first()
			if product_model and product_model.stock_type == mall_models.PRODUCT_STOCK_TYPE_LIMIT:
				mall_models.ProductModel.update(
					stocks=mall_models.ProductModel.stocks + changed_count).dj_where(
					id=model_id).execute()


	def update_product_position(self, product_id, position):
		"""
		更新商品排序的顺序
		"""
		#将以前display_index是position的商品，设置为product_pool.NEW_PRODUCT_DISPLAY_INDEX
		mall_models.ProductPool.update(display_index=product_pool.NEW_PRODUCT_DISPLAY_INDEX).dj_where(woid=self.corp.id, display_index=position).execute()

		#设置指定商品的position
		mall_models.ProductPool.update(display_index=position).dj_where(woid=self.corp.id, product_id=product_id).execute()
		self.__send_msg_to_topic(product_id, "product_updated")


	def update_product_sale(self,product_id,changed_count):
		if mall_models.ProductSales.select().dj_where(product_id=product_id).first():
			mall_models.ProductSales.update(
				sales=mall_models.ProductSales.sales + changed_count).dj_where(product_id=product_id).execute()
		else:
			mall_models.ProductSales.create(product=product_id, sales=changed_count)
