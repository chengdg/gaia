# -*- coding: utf-8 -*-


from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.product_config import ProductConfig


class AProductConfig(api_resource.ApiResource):
	"""
	商品配置相关信息
	"""
	app = "product"
	resource = "product_config"

	@param_required(['owner_id'])
	def get(args):
		# 确定支付接口配置
		owner_id = args['owner_id']
		product_id = args.get('product_id', None)
		if product_id:
			product_config = ProductConfig.get({'owner_id': owner_id, 'product_id':product_id})
			return product_config.to_dict()
		else:
			product_config = ProductConfig.get({'owner_id': owner_id})
			return product_config.to_dict()


