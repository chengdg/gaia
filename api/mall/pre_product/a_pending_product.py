# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.pre_product.pre_product_factory import PreProductFactory
from db.mall import models as mall_models

class APendingProduct(api_resource.ApiResource):

	app = "mall"
	resource = "pending_product"

	@param_required(['corp_id', 'product_ids:json'])
	def put(args):
		corp = args['corp']
		product_ids = args['product_ids']

		pre_product_factory = PreProductFactory.get(corp)
		pre_product_factory.pending_pre_product(product_ids)

		return {}

	def post(self):
		pass

	@param_required(['corp_id', 'product_id:int', 'reason'])
	def delete(args):
		product_id = args['product_id']
		reason = args['reason']

		mall_models.Product.update(
			refuse_reason = reason,
			pending_status = mall_models.PRODUCT_PENDING_STATUS['REFUSED']
		).dj_where(id=product_id).execute()

		return {}