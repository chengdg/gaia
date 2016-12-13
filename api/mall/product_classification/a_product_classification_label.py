# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.corporation_factory import CorporationFactory


class AProductClassificationLabel(api_resource.ApiResource):
    """
    商品分类标签
    """
    app = "mall"
    resource = "product_classification_label"

    @param_required(['classification_id', 'qualification_infos:json'])
    def put(args):
        classification_id = args['classification_id']
        qualification_infos = args['qualification_infos']

        weizoom_corp = CorporationFactory.get_weizoom_corporation()
        classification = weizoom_corp.product_classification_repository.get_product_classification(classification_id)
        classification.set_qualifications(qualification_infos)

        return {}

