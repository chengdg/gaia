# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.product_classification_qualification import ProductClassificationQualification
from business.common.page_info import PageInfo


class AProductClassificationQualification(api_resource.ApiResource):
    """
    商品分类特殊资质
    """
    app = "mall"
    resource = "product_classification_qualification"

    @param_required(['classification_id', 'qualification_infos'])
    def put(args):		
        classification_id = args['classification_id']
        qualification_infos = args['qualification_infos']

        ProductClassificationQualification.update({
            'classification_id': classification_id,
            'qualification_infos': qualification_infos
        })

        return {}

