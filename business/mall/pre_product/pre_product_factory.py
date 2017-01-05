# -*- coding: utf-8 -*-

from business import model as business_model
from db.mall import models as mall_models


class PreProductFactory(business_model.Service):
	"""
	待审核商品工厂
	"""

	def __create_pre_product(self, base_info, postage_info):
		pre_product = mall_models.Product.create(
			owner = self.corp.id,
			name = base_info.get('name', '').strip(),
			promotion_title = base_info.get('promotion_title', '').strip(),
			detail = base_info.get('detail', '').strip(),
			postage_type = postage_info['postage_type'],
			postage_id = postage_info.get('postage_id', 0),
			unified_postage_money = postage_info['unified_postage_money'],
			stocks = 0,
			price = base_info.get('price', 0.0),
			purchase_price = base_info.get('purchase_price', 0.0),
			limit_zone_type = int(postage_info.get('limit_zone_type', '0')),
			limit_zone = int(postage_info.get('limit_zone', '0')),
			pending_status = mall_models.PRODUCT_PENDING_STATUS['SUBMIT'],
			is_pre_product = True,
			is_accepted = False
		)

		return pre_product

	def __add_images_to_pre_product(self, pre_product_id, images):
		"""
		设置商品图片
		"""
		for swipe_image in images:
			if swipe_image['width'] and swipe_image['height']:
				mall_models.ProductSwipeImage.create(
					product = pre_product_id,
					url = swipe_image['url'],
					width = swipe_image['width'],
					height = swipe_image['height']
				)

	def __set_pre_product_models(self, pre_product_id, models_info):
		# 处理standard商品规格
		has_multi_models = models_info.get('has_multi_models', False)
		corp_id = self.corp.id

		#在任何情况下，都创建一个的standard model
		if has_multi_models:
			mall_models.ProductModel.create(
				owner = corp_id,
				product = pre_product_id,
				name = 'standard',
				is_standard = True,
				price = 0.0,
				purchase_price = 0.0,
				weight = 0,
				stock_type = mall_models.PRODUCT_STOCK_TYPE_UNLIMIT,
				stocks = -1,
				user_code = '',
				is_deleted = True
			)
		else:
			standard_model = models_info['standard_model']
			mall_models.ProductModel.create(
				owner = corp_id,
				product = pre_product_id,
				name = 'standard',
				is_standard = True,
				price = standard_model['price'],
				purchase_price = standard_model['purchase_price'],
				weight = standard_model['weight'],
				stock_type = mall_models.PRODUCT_STOCK_TYPE_LIMIT,
				stocks = standard_model['stocks'],
				user_code = '',
				is_deleted = False
			)

		# 处理custom商品规格
		custom_models = models_info['custom_models']
		for custom_model in custom_models:
			product_model = mall_models.ProductModel.create(
				owner = corp_id,
				product = pre_product_id,
				name = custom_model['name'],
				is_standard = False,
				purchase_price = custom_model.get('purchase_price', 0),
				price = custom_model['price'],
				weight = custom_model['weight'],
				stock_type = mall_models.PRODUCT_STOCK_TYPE_LIMIT,
				stocks = custom_model['stocks'],
				user_code = ''
			)

			for property in custom_model['properties']:
				mall_models.ProductModelHasPropertyValue.create(
					model = product_model,
					property_id = property['property_id'],
					property_value_id = property['property_value_id']
				)

	def __add_pre_product_to_classification(self, classification_id, pre_product_id):
		classification = self.corp.product_classification_repository.get_product_classification(classification_id)
		classification.add_product(pre_product_id)

	def create_pre_product(self, args):
		"""
		创建待审核商品
		"""
		db_models = mall_models.Product.select().dj_where(owner_id=self.corp.id, name=args['name'], is_deleted=False)

		if db_models.count() > 0:
			return u'商品名已存在'

		name = args['name']
		promotion_title = args.get('promotion_title', '')
		price = args['price']
		weight = args['weight']
		stocks = args['stocks']
		purchase_price = args.get('purchase_price', 0.0)
		detail = args.get('detail', '')
		postage_id = args.get('postage_id', 0)
		postage_type = 'unified_postage_type' if args['has_same_postage'] else 'custom_postage_type'
		limit_zone_type = args.get('limit_zone_type', 0)
		limit_zone = args.get('limit_zone', 0)
		unified_postage_money = args['postage_money']
		has_multi_models = args['has_multi_models']
		models = args.get('models', [])
		classification_id = args['classification_id']

		base_info = {
			'name': name,
			'promotion_title': promotion_title,
			'detail': detail,
			'price': price,
			'purchase_price': purchase_price
		}

		image_info = args.get('images', [])

		postage_info = {
			'postage_type': postage_type,
			'postage_id': postage_id,
			'unified_postage_money': unified_postage_money,
			'limit_zone_type': limit_zone_type,
			'limit_zone': limit_zone
		}

		models_info = {
			'has_multi_models': has_multi_models,
			'standard_model': {
				'price': price,
				'purchase_price': purchase_price,
				'weight': weight,
				'stocks': stocks
			},
			'custom_models': models
		}

		pre_product_model = self.__create_pre_product(base_info, postage_info)

		self.__add_pre_product_to_classification(classification_id, pre_product_model.id)
		self.__add_images_to_pre_product(pre_product_model.id, image_info)
		self.__set_pre_product_models(pre_product_model.id, models_info)

		return pre_product_model

	def pending_pre_product(self, pre_product_ids):
		print (pre_product_ids)
		#更新待审核商品状态
		mall_models.Product.update(
			pending_status = mall_models.PRODUCT_PENDING_STATUS['NOT_YET'],
			is_updated = False,
			is_accepted = True
		).dj_where(id__in=pre_product_ids, is_pre_product=True).execute()

		corp = self.corp
		# 将商品放入product pool
		corp.product_pool.add_products(pre_product_ids)
		# 将商品放入待售shelf
		corp.forsale_shelf.add_products(pre_product_ids)