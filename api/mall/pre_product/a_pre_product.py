# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.pre_product.pre_product import PreProduct

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
			'store': pre_product.store,
			'has_limit_time': pre_product.has_limit_time,
			'valid_time_from': '' if not pre_product.valid_time_from else pre_product.valid_time_from.strftime(
				"%Y-%m-%d %H:%M"),
			'valid_time_to': '' if not pre_product.valid_time_to else pre_product.valid_time_to.strftime("%Y-%m-%d %H:%M"),
			'limit_settlement_price': str(pre_product.limit_settlement_price),
			'remark': pre_product.remark,
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
		"""
		创建待审核商品
		"""
		pre_product, msg = PreProduct.create({
			'owner_id': args['corp'].id,
			'name': args['name'],
			'title': args.get('title', ''),
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

		if pre_product:
			return {}
		else:
			return (500, msg)

	def post(self):
		"""
		修改商品信息
		"""
		pass

	def delete(self):
		"""
		删除商品(待审核、已审核)
		"""
		pass





		