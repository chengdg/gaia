# -*- coding: utf-8 -*-
import json

from bdem import msgutil
from eaglet.core import api_resource
from eaglet.decorator import param_required

from gaia_conf import TOPIC


class AProductCustomizePrice(api_resource.ApiResource):
	"""
	商品改价
	"""
	app = "product"
	resource = "product_customize_price"

	@param_required(['corp_id', 'product_id:int'])
	def get(args):
		corp = args['corp']
		product_id = args['product_id']
		product = corp.product_pool.get_product_by_id(product_id)
		if not product:
			return []
		else:
			customized_price_models = product.get_customized_price()
			return [{
				'corp_id': model.corp_id,
				'product_id': model.product_id,
				'product_model_id': model.product_model_id,
				'price': model.price
			} for model in customized_price_models]


	@param_required(['corp_id', 'product_id:int', 'customized_models:json'])
	def post(args):
		corp = args['corp']
		product = corp.product_pool.get_product_by_id(args['product_id'])
		price_info = []
		for product_model_id, price in args['customized_models'].items():
			price_info.append(float(price))
			product.customize_price(float(price), int(product_model_id))

		topic_name = TOPIC['product']
		data = {
			"product_id": args['product_id'],
			"corp_id": corp.id,
			"price_info": json.dumps(price_info)
		}
		msgutil.send_message(topic_name, "community_changed_price", data)
		return {}
