# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.classification.product_classification import ProductClassification
from business.mall.corporation_factory import CorporationFactory


class AProductClassification(api_resource.ApiResource):
    """
    商品分类
    """
    app = "mall"
    resource = "product_classification"

    @param_required(['corp_id', 'name', 'father_id', '?note'])
    def put(args):
        name = args['name']
        father_id = args['father_id']
        note = args.get('note', '')

        product_classification = ProductClassification.create({
            'name': name,
            'father_id': father_id,
            'note': note
        })

        return {
            'id': product_classification.id
        }

    @param_required(['corp_id', 'name', 'id', '?note'])
    def post(args):
        corp = args['corp']
        name = args['name']
        classification_id = args['id']
        note = args.get('note', '')

        product_classification = corp.product_classification_repository.get_product_classification(classification_id)
        product_classification.update(name, note)

        return {}

    @param_required(['id'])
    def delete(args):
        weizoom_corp = CorporationFactory.get_weizoom_corporation()
        classification_id = args['id']
        product_classification = weizoom_corp.product_classification_repository.get_product_classification(classification_id)
        if product_classification.is_used_by_product():
            return 500, 'used_by_product' #商品分类正在被使用
        else:
            weizoom_corp.product_classification_repository.delete_product_classification(classification_id)

            return {}
        
   