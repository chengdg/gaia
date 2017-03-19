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

	@param_required(['corp_id', '?father_id:int', '?check_label:bool', '?root_only:bool'])
	def get(args):
		"""
		root_only: 只获取顶级分类
		"""
		corp = args['corp']
		father_id = args.get('father_id', None)
		if args.get('root_only'):
			product_classifications = corp.product_classification_repository.get_root_product_classifications()
		elif father_id:
			product_classifications = [ProductClassification(model.classification) for model in corp.product_classification_repository.get_children_product_classifications(father_id)]
		else:
			product_classifications = corp.product_classification_repository.get_product_classifications()

		if args.get('check_label'):
			classification_id2haslabel = corp.product_classification_repository.check_labels(product_classifications)

		product_calssification_id2qualification = dict()
		qualifications = corp.product_classification_repository.get_qualifications_by_classification_ids([p.id for p in product_classifications])
		for qualification in qualifications:
			if not product_calssification_id2qualification.has_key(qualification.classification_id):
				product_calssification_id2qualification[qualification.classification_id] = [qualification]
			else:
				product_calssification_id2qualification[qualification.classification_id].append(qualification)


		datas = []
		for product_classification in product_classifications:
			qualifications = product_calssification_id2qualification.get(product_classification.id, [])
			datas.append({
				'id': product_classification.id,
				'name': product_classification.name,
				'level': product_classification.level,
				'father_id': product_classification.father_id,
				'product_count': product_classification.total_product_count,
				'note': product_classification.note,
				'created_at': product_classification.created_at.strftime('%Y-%m-%d %H:%M'),
				'qualification_infos': [{
					"id": qualification.id,
					"name": qualification.name,
					'created_at': qualification.created_at,
					'index': i
					} for i, qualification in enumerate(qualifications)],
				'has_label': classification_id2haslabel[product_classification.id] if args.get('check_label') else False
			})

		return {
			'product_classifications': datas
		}