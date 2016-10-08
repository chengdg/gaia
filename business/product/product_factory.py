# -*- coding: utf-8 -*-
import json

from eaglet.core import watchdog

from business import model as business_model
from business.product.product import Product
from db.mall import models as mall_models
from eaglet.decorator import param_required


class ProductFactory(business_model.Service):
	"""
	商品工厂
	"""
	def __create_product(self, base_info, image_info, postage_info, pay_info):
		product = mall_models.Product.create(
			owner=self.corp.id,
			name=base_info.get('name', '').strip(),
			promotion_title=base_info.get('promotion_title', '').strip(),
			bar_code=base_info.get('bar_code', '').strip(),
			thumbnails_url=image_info.get('thumbnails_url', '').strip(),
			pic_url='',
			detail=base_info.get('detail', '').strip(),
			type=base_info.get('type', mall_models.PRODUCT_DEFAULT_TYPE),
			is_use_online_pay_interface='is_enable_online_pay_interface' in pay_info,
			is_use_cod_pay_interface='is_enable_cod_pay_interface' in pay_info,
			postage_type=postage_info['postage_type'],
			postage_id=postage_info.get('postage_id', 0),
			unified_postage_money=postage_info['unified_postage_money'],
			stocks=base_info['min_limit'],
			is_member_product=base_info.get("is_member_product", "false") == 'true',
			supplier=base_info.get('supplier_id', 0),
			purchase_price=base_info.get('purchase_price', 0.0),
			is_enable_bill=base_info.get('is_enable_bill', 'false') == 'true',
			is_delivery=base_info.get('is_delivery', 'false') == 'true',
			limit_zone_type=int(postage_info.get('limit_zone_type', '0')),
			limit_zone=int(postage_info.get('limit_zone_template', '0'))
		)
		
		return product

	def __add_product_to_categories(self, product, category_ids):
		"""
		将商品加入到多个商品分组中
		"""
		if len(category_ids) == 0:
			return

		for category_id in category_ids:
			mall_models.CategoryHasProduct.create(
				category = category_id,
				product = product.id
			)

	def __set_product_models(self, product, models_info):
		# 处理standard商品规格
		is_delete_standard_model = (models_info.get('is_use_custom_model', 'false') == 'true')
		corp_id = self.corp.id

		#在任何情况下，都创建一个的standard model
		if is_delete_standard_model:
			mall_models.ProductModel.create(
				owner=corp_id,
				product=product.id,
				name='standard',
				is_standard=True,
				price=0.0,
				weight=0,
				stock_type=mall_models.PRODUCT_STOCK_TYPE_UNLIMIT,
				stocks=-1,
				user_code='',
				is_deleted=True
			)
		else:
			standard_model = models_info['standard_model']
			mall_models.ProductModel.create(
				owner=corp_id,
				product=product.id,
				name='standard',
				is_standard=True,
				price=standard_model['price'],
				weight=standard_model['weight'],
				stock_type=mall_models.PRODUCT_STOCK_TYPE_UNLIMIT if standard_model['stock_type'] == 'unlimit' else mall_models.PRODUCT_STOCK_TYPE_LIMIT,
				stocks=standard_model['stocks'],
				user_code=standard_model['user_code'],
				is_deleted=False
			)

		# 处理custom商品规格
		custom_models = models_info['custom_models']
		for custom_model in custom_models:
			product_model = mall_models.ProductModel.create(
				owner=corp_id,
				product=product.id,
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

	def __add_images_to_product(self, product, image_info):
		"""
		设置商品图片
		"""
		images = image_info['images']
		if len(images) == 0:
			return

		for swipe_image in images:
			if swipe_image['width'] and swipe_image['height']:
				mall_models.ProductSwipeImage.create(
					product=product.id,
					url=swipe_image['url'],
					width=swipe_image['width'],
					height=swipe_image['height']
				)

	def create_product(self, args):
		base_info = json.loads(args['base_info'])
		models_info = json.loads(args['models_info'])
		image_info = json.loads(args['image_info'])
		postage_info = json.loads(args['postage_info'])
		pay_info = json.loads(args['pay_info'])
		categories = json.loads(args['categories'])
		properties = json.loads(args['properties'])

		product = self.__create_product(base_info, image_info, postage_info, pay_info)
		self.__add_product_to_categories(product, categories)
		self.__add_images_to_product(product, image_info)
		self.__set_product_models(product, models_info)

		corp = self.corp
		#将商品放入product pool
		corp.product_pool.add_products([product.id])
		#将商品放入待售shelf
		corp.forsale_shelf.add_products([product.id])

		return product

	def __init_base_info(self, product, args):
		"""
		初始化基本信息
		@param args:
		@return:
		"""
		base_info = json.loads(args['base_info'])

		product.owner_id = base_info['owner_id']
		product.name = base_info.get('name', '').strip()
		product.promotion_title = base_info.get('promotion_title', '').strip()
		product.bar_code = base_info.get('bar_code', '').strip()
		product.min_limit = int(base_info.get('min_limit', 0))
		product.is_member_product = int(base_info.get('is_member_product', '0'))
		product.detail = base_info['detail']

		product_category_id = base_info.get('product_category', '')

		product.product_category_id = product_category_id.split(',')

	def __init_models_info(self, product, args):
		models_info = json.loads(args['models_info'])

		if models_info['is_use_custom_models']:
			custom_models_info = models_info['custom_model']
			# 多规格商品创建默认标准规格

			custom_models = []
			standard_model = {
				"price": 0.0,
				"weight": 0.0,
				"stock_type": mall_models.PRODUCT_STOCK_TYPE_LIMIT,
				"stocks": 0,
				"user_code": '',
				"is_deleted": True
			}

			def __init_custom_model(model_name):

				properties = []
				property_infos = model_name.split('_')
				for property_info in property_infos:
					items = property_info.split(':')
					properties.append({
						'property_id': int(items[0]),
						'property_value_id': int(items[1])
					})
				return properties

			for model in custom_models_info:

				model['properties'] = __init_custom_model(model['name'])
				if model.get('stocks') and int(model.get('stocks')) == -1:
					model['stocks'] = 0

				custom_models.append({
					'name': model['name'],
					'is_standard': False,
					'price': model['price'],
					'weight': model['weight'],
					'stock_type': model['stock_type'],
					'stocks': model['stocks'],
					'user_code': model['user_code'],

				})

		else:
			standard_model = {}
			custom_models = {}

		product.standard_model = standard_model
		product.custom_models = custom_models

	def __init_image_info(self, product, args):
		image_info = json.loads(args['image_info'])

		product.swipe_images = json.loads(image_info['swipe_images'])

	def __init_postage_info(self, product, args):
		postage_info = json.loads(args['postage_info'])
		product.postage_type = postage_info.get('postage_type', '')
		product.unified_postage_money = float(postage_info.get('unified_postage_money', '0.0'))
		product.is_delivery = int(postage_info.get('is_delivery', '0'))

	def __init_pay_info(self, product, args):
		pay_info = json.loads(args['pay_info'])

		product.is_use_cod_pay_interface = int(pay_info.get('is_enable_cod_pay_interface', '0'))
		product.is_use_online_pay_interface = int(pay_info.get('is_use_online_pay_interface', '0'))
		product.is_enable_bill = int(pay_info.get('is_enable_bill', '0'))
