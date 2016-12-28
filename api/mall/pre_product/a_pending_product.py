# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.product.product_factory import ProductFactory
from db.mall import models as mall_models

class APendingProduct(api_resource.ApiResource):

	app = "mall"
	resource = "pending_product"

	@param_required(['corp_id', 'product_ids:json'])
	def put(args):
		corp = args['corp']
		product_ids = args['product_ids']

		product_factory = ProductFactory.get(corp)
		product_factory.create_product_from_pre_product(product_ids)

		return {}

	def post(self):
		pass

	@param_required(['corp_id', 'product_id:int', 'reason'])
	def delete(args):
		product_id = args['product_id']
		reason = args['reason']

		mall_models.PreProduct.update(
			refuse_reason = reason,
			review_status = mall_models.PRE_PRODUCT_STATUS['REFUSED']
		).dj_where(id=product_id).execute()

		return {}