# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

class AWebappConfig(api_resource.ApiResource):
	"""
	针对webapp的配置
	"""
	app = 'mall'
	resource = 'webapp_config'

	@param_required(['corp_id'])
	def get(args):
		corp = args['corp']
		webapp_config = corp.mall_config_repository.get_webapp_config()

		data = {
			'id': webapp_config.id,
			'max_product_count': webapp_config.max_product_count,
			'is_enable_bill': webapp_config.is_enable_bill,
			'show_product_sales': webapp_config.show_product_sales,
			'show_product_sort': webapp_config.show_product_sort,
			'show_product_search': webapp_config.show_product_search,
			'show_shopping_cart': webapp_config.show_shopping_cart,
			'order_expired_day': webapp_config.order_expired_day
		}

		return data

	@param_required(['corp_id'])
	def post(args):
		corp = args['corp']

		webapp_config = corp.mall_config_repository.get_webapp_config()
		webapp_config.update(args)

		return {}