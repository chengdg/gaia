# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.product_classification import ProductClassification


class AProductClassification(api_resource.ApiResource):
    """
    商品分类
    """
    app = "mall"
    resource = "product_classification"

    @param_required(['name', 'level', 'father_id'])
    def put(args):
        name = args['name']
        level = args['level']
        father_id = args['father_id']

        product_classification = ProductClassification.create({
            'name': name,
            'level': level,
            'father_id': father_id
        })

        return {
            'id': product_classification.id
        }

    @param_required(['id'])
    def delete(args):
        corp = args['corp']
        corp.product_classification_repository.delete_product_classification(args['id'])

        return {}
        
   