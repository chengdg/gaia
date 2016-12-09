# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.corporation_factory import CorporationFactory
from business.common.page_info import PageInfo


class AProductClassificationQualification(api_resource.ApiResource):
    """
    商品分类特殊资质
    """
    app = "mall"
    resource = "product_classification_qualification"

    @param_required(['classification_id', 'qualification_infos:json'])
    def put(args):
        classification_id = args['classification_id']
        qualification_infos = args['qualification_infos']

        weizoom_corp = CorporationFactory.get_weizoom_corporation()
        classification = weizoom_corp.product_classification_repository.get_product_classification(classification_id)
        classification.set_qualifications(qualification_infos)

        return {}

