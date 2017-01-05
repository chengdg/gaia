# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.pre_product.pre_product_factory import PreProductFactory

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
			'name': pre_product.name,
			'promotion_title': pre_product.promotion_title,
			'price': str(pre_product.price) if pre_product.price > 0 else str(pre_product.purchase_price),
			'purchase_price': str(pre_product.purchase_price),
			'weight': '%s' % pre_product.weight,
			'stocks': pre_product.stocks,
			'detail': pre_product.detail,
			'models': [], #TODO
			'images': [],
			'limit_zone_type': pre_product.limit_zone_type,
			'limit_zone': pre_product.limit_zone,
			'has_same_postage': pre_product.has_same_postage,
			'postage_money': '%.2f' % pre_product.unified_postage_money,
			'classification_name_nav': pre_product.classification_nav
		}

	@param_required(['corp_id', 'name', '?has_multi_models:bool', '?models:json'])
	def put(args):
		pre_product_factory = PreProductFactory.get(args['corp'])
		pre_product = pre_product_factory.create_pre_product({
			'name': args['name'],
			'classification_id': args.get('classification_id', 0),
			'promotion_title': args.get('promotion_title', ''),
			'has_multi_models': args.get('has_multi_models', False),
			'models': args.get('models', []),
			'price': args.get('price', 0),
			'weight': args.get('weight', 0),
			'stocks': args.get('stocks', 0),
			'limit_zone_type': args.get('limit_zone_type', 0),
			'limit_zone': args.get('limit_zone', 0),
			'postage_id': args.get('postage_id', 0),
			'postage_money': args.get('postage_money', 0),
			'has_same_postage': args.get('has_same_postage', True),
			'detail': args.get('detail', '')
		})

		if not isinstance(pre_product, basestring):
			return {}
		else:
			return (500, pre_product)

	def post(self):
		pass

	def delete(self):
		pass





		