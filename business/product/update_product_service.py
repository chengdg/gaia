# -*- coding: utf-8 -*-
import json

from eaglet.core import watchdog

from business import model as business_model
from business.product.product import Product
from db.mall import models as mall_models
from eaglet.decorator import param_required


class UpdateProductService(business_model.Service):
	"""
	商品工厂
	"""
	def __update_product(self, product_id, base_info, image_info, postage_info, pay_info):
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
			postage_type=postage_info['postage_type'],
			postage_id=postage_info.get('postage_id', 0),
			unified_postage_money=postage_info['unified_postage_money'],
			stocks=base_info['min_limit'],
			is_member_product=base_info['is_member_product'],
			supplier=base_info.get('supplier_id', 0),
			purchase_price=base_info.get('purchase_price', 0.0),
			is_enable_bill=base_info['is_enable_bill'],
			is_delivery=base_info.get('is_delivery', 'false') == 'true',
			limit_zone_type=int(postage_info.get('limit_zone_type', '0')),
			limit_zone=int(postage_info.get('limit_zone_template', '0'))
		).dj_where(owner_id=self.corp.id, id=product_id).execute()
		
		return product

	def __update_product_categories(self, product_id, category_ids):
		"""
		更新商品分组
		"""
		if len(category_ids) == 0:
			return

		mall_models.CategoryHasProduct.delete().dj_where(product_id=product_id).execute()
		for category_id in category_ids:
			mall_models.CategoryHasProduct.create(
				category = category_id,
				product = product_id
			)

	def __update_standard_model(self, product_id, models_info):
		"""
		更新标准规格
		"""
		is_delete_standard_model = (models_info.get('is_use_custom_model', 'false') == 'true')
		corp_id = self.corp.id

		if is_delete_standard_model:
			mall_models.ProductModel.update(
				price=0.0,
				weight=0,
				stock_type=mall_models.PRODUCT_STOCK_TYPE_UNLIMIT,
				stocks=-1,
				user_code='',
				is_deleted=True
			).dj_where(owner_id=corp_id, product_id=product_id, name='standard').execute()
		else:
			standard_model = models_info['standard_model']
			mall_models.ProductModel.update(
				price=standard_model['price'],
				weight=standard_model['weight'],
				stock_type=mall_models.PRODUCT_STOCK_TYPE_UNLIMIT if standard_model['stock_type'] == 'unlimit' else mall_models.PRODUCT_STOCK_TYPE_LIMIT,
				stocks=standard_model['stocks'],
				user_code=standard_model['user_code'],
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
				user_code=custom_model['user_code']
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
				stock_type=mall_models.PRODUCT_STOCK_TYPE_UNLIMIT if new_model['stock_type'] == 'unlimit' else mall_models.PRODUCT_STOCK_TYPE_LIMIT,
				stocks=new_model['stocks'],
				user_code=new_model['user_code']
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
		existed_models = [model for model in  mall_models.ProductModel.select().dj_where(product_id=product_id, is_deleted=False) if not model.is_standard]
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

	def update_product(self, product_id, args):
		base_info = json.loads(args['base_info'])
		models_info = json.loads(args['models_info'])
		image_info = json.loads(args['image_info'])
		postage_info = json.loads(args['postage_info'])
		pay_info = json.loads(args['pay_info'])
		categories = json.loads(args['categories'])
		properties = json.loads(args['properties'])

		product = self.__update_product(product_id, base_info, image_info, postage_info, pay_info)
		self.__update_product_categories(product_id, categories)
		self.__update_product_images(product_id, image_info)
		self.__update_product_models(product_id, models_info)
		self.__update_product_properties(product_id, properties)

		return product