# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required
from business.mall.corporation_factory import CorporationFactory


class AChildProductClassifications(api_resource.ApiResource):
    """
    商品分类
    """
    app = "mall"
    resource = "child_product_classifications"

    @param_required(['corp_id', 'classification_id'])
    def get(args):
        corp = CorporationFactory.get()
        father_id = int(args['classification_id'])
        product_classifications = corp.product_classification_repository.get_child_product_classifications(father_id)

        datas = []
        for product_classification in product_classifications:
            datas.append({
                'id': product_classification.id,
                'name': product_classification.name,
                'level': product_classification.level,
                'father_id': product_classification.father_id,
                'product_count': product_classification.total_product_count
            })

        return {
            'product_classifications': datas
        }        
   