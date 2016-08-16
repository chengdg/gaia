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

		product_config = ProductConfig.get({'owner_id': owner_id, 'product_id': product_id})

		return {
			'postage_config_info': product_config.postage_config_info,
			'property_templates': product_config.property_templates,
			'pay_interface_config': product_config.pay_interface_config,
			'mall_type': product_config.mall_type,
			'is_bill': product_config.is_bill,
			'store_name': product_config.store_name
		}
