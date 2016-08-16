# -*- coding: utf-8 -*-


from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.product import Product
from business.mall.product_config import ProductConfig
from business.mall.product_factory import ProductFactory


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
			return {}
		else:
			product_config = ProductConfig.get({'owner_id': owner_id})
			return {
				'product_config': product_config.to_dict()
			}

