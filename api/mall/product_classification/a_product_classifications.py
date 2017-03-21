# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.corporation_factory import CorporationFactory
from business.mall.product_classification.product_classification import ProductClassification


class AProductClassifications(api_resource.ApiResource):
	"""
	商品分类集合
	"""
	app = "mall"
	resource = "product_classifications"

	@param_required(['corp_id', '?father_id:int'])
	def get(args):
		corp = args['corp']
		father_id = args.get('father_id', None)
		if father_id != None:
			product_classifications = corp.product_classification_repository.get_children_product_classifications(father_id)
		else:
			product_classifications = corp.product_classification_repository.get_product_classifications()

		datas = []
		for product_classification in product_classifications:
			datas.append({
				'id': product_classification.id,
				'name': product_classification.name,
				'level': product_classification.level,
				'father_id': product_classification.father_id,
				'product_count': product_classification.product_count,
				'note': product_classification.note,
				'created_at': product_classification.created_at.strftime('%Y-%m-%d %H:%M')
			})

		return {
			'product_classifications': datas
		}