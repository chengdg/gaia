# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.classification.product_classification import ProductClassification


class AProductClassificationTree(api_resource.ApiResource):
    """
    商品分类的tree结构
    """
    app = "mall"
    resource = "product_classification_tree"

    @param_required(['end_id'])
    def get(args):
        corp = args['corp']
        end_id = args['end_id']

        product_classifications = corp.product_classification_repository.get_product_classification_tree_by_end(end_id)

        datas = []
        for product_classification in product_classifications:
            qualifications = product_classification.get_qualifications()
            datas.append({
                'id': product_classification.id,
                'name': product_classification.name,
                'level': product_classification.level,
                'father_id': product_classification.father_id,
                'product_count': product_classification.product_count,
                'created_at': product_classification.created_at.strftime('%Y-%m-%d %H:%M'),
                'qualification_infos': [{
                    "id": qualification.id, 
                    "name": qualification.name, 
                    'created_at': qualification.created_at,
                    'index': i
                    } for i, qualification in enumerate(qualifications)]
            })

        return {
            'product_classifications': datas
        }
   