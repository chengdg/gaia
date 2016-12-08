# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.product_classification_qualification_repository import ProductClassificationQualificationRepository


class AProductClassifications(api_resource.ApiResource):
    """
    商品分类集合
    """
    app = "mall"
    resource = "product_classifications"

    @param_required(['?father_id'])
    def get(args):
        corp = args['corp']
        father_id = args.get('father_id', None)
        if father_id:
            product_classifications = corp.product_classification_repository.get_child_product_classifications(father_id)
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
                'created_at': product_classification.created_at.strftime('%Y-%m-%d %H:%M'),
                'qualification_infos': ProductClassificationQualificationRepository().get_product_classification_qualifications(product_classification.id)
            })

        return {
            'product_classifications': datas
        }