# -*- coding: utf-8 -*-


from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.product import Product
from business.mall.product_factory import ProductFactory


class AProduct(api_resource.ApiResource):
	"""
	商品
	"""
	app = "product"
	resource = "product"

	@param_required(['name', 'swipe_images', 'postage_type', 'owner_id'])
	def put(args):
		"""
		创建商品
		@return:
		"""

		# product_data = {
		#
		# 	'owner_id': args['owner_id'],
		# 	'name': args['name'],
		# 	'postage_type': args['postage_type'],
		#
		#
		# 	'unified_postage_money': args.get('unified_postage_money', 0.0),
		# 	'min_limit': float(args['min_limit']),
		# 	'purchase_price': float(args['purchase_price']),
		# 	'is_enable_bill': args['is_enable_bill'],
		# 	'is_delivery': args['is_delivery'],
		# 	'is_bill': args['is_bill'],
		#
		# 	'promotion_title': args['promotion_title'],
		# 	'user_code': args['user_code'],
		# 	'bar_code': args['bar_code'],
		# 	'thumbnails_url': args['thumbnails_url'],
		# 	'pic_url': args['pic_url'],
		#
		# 	'detail': args['detail'],
		# 	'is_use_online_pay_interface': args['is_use_online_pay_interface'],
		#
		# 	'is_use_cod_pay_interface': args['is_use_cod_pay_interface'],
		#
		# 	'is_member_product': args['is_member_product'],
		# 	'supplier': args['supplier'],
		#
		# 	'swipe_images': args.get('swipe_images'),
		#
		# 	# 商品规格数据
		# 	'is_use_custom_model': args['is_use_custom_model'],
		# 	'customModels': args.get('customModels', '[]'),
		#
		# 	# 商品分组数据
		# 	'product_category': args['product_category'],
		#
		# 	# 商品属性数据
		# 	'properties': args['properties', '[]']
		# }

		product_data = args
		product_factory = ProductFactory.get()
		product_factory.create_product(args['owner_id'], product_data)

		return {}

	@param_required([])
	def post(args):
		"""
		修改商品
		@return:
		"""
		product = Product.from_id({
			'product_id': args['product_ids'],
			'owner_id': args['owner_id'],
			'fill_options': {}
		})

		product.modify(args)

		return {}




