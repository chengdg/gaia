# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack


class AProductClassifications(api_resource.ApiResource):
    """
    商品分类集合
    """
    app = "mall"
    resource = "product_classifications"

    def get(args):
        corp = args['corp']
        product_classifications = corp.product_classification_repository.get_product_classifications()

        datas = []
        for product_classification in product_classifications:
            datas.append({
                'id': product_classification.id,
                'name': product_classification.name,
                'level': product_classification.level,
                'father_id': product_classification.father_id
            })

        return {
            'product_classifications': datas
        }