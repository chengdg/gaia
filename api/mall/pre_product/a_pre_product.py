# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.pre_product.pre_product_factory import PreProductFactory

from util import string_util


class APreProduct(api_resource.ApiResource):
	"""
	待审核商品
	"""
	app = "mall"
	resource = "pre_product"

	@param_required(['corp_id', 'product_id:int'])
	def get(args):
		product_id = args.get('product_id')
		corp = args['corp']
		pre_product = corp.pre_product_repository.get_pre_product(product_id)
		
		return {
			'id': pre_product.id,
			'product_name': pre_product.name,
			'title': pre_product.title,
			'price': str(pre_product.product_price) if pre_product.product_price > 0 else str(pre_product.settlement_price),
			'settlement_price': str(pre_product.settlement_price),
			'weight': '%s' % pre_product.weight,
			'stock': pre_product.stock,
			'has_limit_time': pre_product.has_limit_time,
			'valid_time_from': '' if not pre_product.valid_time_from else pre_product.valid_time_from.strftime(
				"%Y-%m-%d %H:%M"),
			'valid_time_to': '' if not pre_product.valid_time_to else pre_product.valid_time_to.strftime("%Y-%m-%d %H:%M"),
			'limit_settlement_price': str(pre_product.limit_settlement_price),
			'remark': string_util.raw_html(pre_product.remark),
			'product_model': [], #TODO
			'images': [],
			'limit_zone_type': pre_product.limit_zone_type,
			'limit_zone_id': pre_product.limit_zone,
			'has_same_postage': pre_product.has_same_postage,
			'postage_money': '%.2f' % pre_product.postage_money,
			'classification_name_nav': pre_product.classification_nav
		}

	@param_required(['corp_id', 'name'])
	def put(args):
		pre_product_factory = PreProductFactory.get(args['corp'])
		pre_product = pre_product_factory.create_pre_product({
			'name': args['name'],
			'classification_id': args.get('classification_id', 0),
			'promotion_title': args.get('promotion_title', ''),
			'has_product_model': args.get('has_product_model', False),
			'price': args.get('price', 0),
			'weight': args.get('weight', 0),
			'stock': args.get('stock', 0),
			'limit_zone_type': args.get('limit_zone_type', 0),
			'limit_zone': args.get('limit_zone', 0),
			'postage_id': args.get('postage_id', 0),
			'postage_money': args.get('postage_money', 0),
			'has_same_postage': args.get('has_same_postage', True),
			'remark': args.get('remark', '')
		})

		if not isinstance(pre_product, basestring):
			return {}
		else:
			return (500, pre_product)

	def post(self):
		pass

	def delete(self):
		pass





		