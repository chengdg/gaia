# -*- coding: utf-8 -*-


from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.product_factory import ProductFactory
from business.product.update_product_service import UpdateProductService
from business.product.encode_product_service import EncodeProductService


class AProduct(api_resource.ApiResource):
	"""
	商品
	"""
	app = "product"
	resource = "product"

	@param_required(['corp_id', 'id'])
	def get(args):
		corp = args['corp']
		ids = [args['id']]
		fill_options = {
			'with_category': True,
			'with_image': True,
			'with_product_model': True,
			'with_model_property_info': True,
			'with_property': True,
			'with_supplier_info': True,
			'with_classification': True
		}
		products = corp.product_pool.get_products_by_ids(ids, fill_options)
		if len(products) == 0:
			return {}
		else:
			product = products[0]
			encode_product_service = EncodeProductService.get(corp)

			data = {
				"id": product.id,
				"base_info": encode_product_service.get_base_info(product),
				"categories": encode_product_service.get_categories(product),
				"image_info": encode_product_service.get_image_info(product),
				"models_info": encode_product_service.get_models_info(product),
				"pay_info": encode_product_service.get_pay_info(product),
				'properties': encode_product_service.get_properties(product),
				"logistics_info": encode_product_service.get_logistics_info(product),
				"supplier": encode_product_service.get_supplier_info(product),
				"classifications": encode_product_service.get_classifications(product)
			}

			return data

	@param_required(['corp_id', 'base_info', 'models_info', 'image_info', 'logistics_info', 'pay_info', 'categories', 'properties'])
	def put(args):
		"""
		创建商品
		@return:
		"""
		product_data = args
		product_factory = ProductFactory.get(args['corp'])
		product_factory.create_product(product_data)

		return {}

	@param_required(['corp_id', 'id', 'base_info', 'models_info', 'image_info', 'logistics_info', 'pay_info', 'categories', 'properties'])
	def post(args):
		product_data = args
		product_id = product_data['id']
		update_product_service = UpdateProductService.get(args['corp'])
		update_product_service.update_product(product_id, product_data)

		return {}

	@param_required(['ids'])
	def delete(args):
		pass
