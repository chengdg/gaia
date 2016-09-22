# -*- coding: utf-8 -*-
import json

from eaglet.core import watchdog

from business import model as business_model
from business.product.product import Product
from business.product.product_pool import ProductPool
from db.mall import models as mall_models
from eaglet.decorator import param_required


class A(object):
	pass

	def add(self):
		pass


class ProductFactory(business_model.Model):
	"""
	商品工厂类
	"""

	def __init__(self):
		super(ProductFactory, self).__init__()

	@staticmethod
	def get():
		return ProductFactory()

	def create_product(self, owner_id, args):

		# _product = A()

		try:
			product = Product()

			additional_data = {}

			self.__init_base_info(product, additional_data, args)
			self.__init_models_info(product, additional_data, args)
			self.__init_image_info(product, additional_data, args)
			self.__init_postage_info(product, additional_data, args)
			self.__init_pay_info(product, additional_data, args)

			# 床架商品（持久化
			product.save(product, additional_data)

			return product


		except BaseException as e:
			from eaglet.core.exceptionutil import unicode_full_stack
			msg = unicode_full_stack()
			print(msg)
			watchdog.alert(msg)

	def __init_base_info(self, product, additional_data, args):
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
		product.detail = base_info.get('detail', '')

		additional_data['category_ids'] = base_info.get('product_category', '').split(',')

	def __init_models_info(self, product, additional_data, args):
		models_info = json.loads(args['models_info'])

		is_use_custom_models = int(models_info['is_use_custom_models'])
		if is_use_custom_models:
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
				stocks = int(model['stocks'])
				if stocks < 0:
					stocks = 0
				else:
					stocks = 0
				custom_models.append({

					'name': model['name'],
					'is_standard': False,
					'price': model['price'],
					'weight': model['weight'],
					'stock_type': model['stock_type'],
					'stocks': stocks,
					'user_code': model['user_code'],

				})

		else:
			standard_model_info = models_info['standard_model']

			stocks = int(standard_model_info['stocks'])
			if stocks < 0:
				stocks = 0
			else:
				stocks = 0
			standard_model = {
				"price": standard_model_info['price'],
				"weight": standard_model_info['weight'],
				"stock_type": standard_model_info['stock_type'],
				"stocks": stocks,
				"user_code": standard_model_info['user_code'],
			}
			custom_models = {}

		additional_data['standard_model'] = standard_model
		additional_data['custom_models'] = custom_models
		additional_data['is_use_custom_models'] = is_use_custom_models

	def __init_image_info(self, product, additional_data, args):
		image_info = json.loads(args['image_info'])

		additional_data['swipe_images'] = json.loads(image_info['swipe_images'])
		product.thumbnails_url = additional_data['swipe_images'][0]['url']

	def __init_postage_info(self, product, additional_data, args):
		postage_info = json.loads(args['postage_info'])

		product.postage_type = postage_info.get('postage_type', '')
		if product.postage_type == mall_models.POSTAGE_TYPE_UNIFIED:
			product.postage_id = -1
		else:
			product.postage_id = 0
		product.unified_postage_money = float(postage_info.get('unified_postage_money', '0.0'))
		product.is_delivery = int(postage_info.get('is_delivery', '0'))

	def __init_pay_info(self, product, additional_data, args):
		pay_info = json.loads(args['pay_info'])

		product.is_use_cod_pay_interface = int(pay_info.get('is_enable_cod_pay_interface', '0'))
		product.is_use_online_pay_interface = int(pay_info.get('is_use_online_pay_interface', '0'))
		product.is_enable_bill = int(pay_info.get('is_enable_bill', '0'))
