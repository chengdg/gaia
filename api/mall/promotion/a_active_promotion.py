# -*- coding: utf-8 -*-

import json

from eaglet.core import api_resource
from eaglet.decorator import param_required


class AActivePromotion(api_resource.ApiResource):
    """
    开启/结束促销活动
    """
    app = 'promotion'
    resource = 'active_promotion'

    @param_required(['corp_id', 'id'])
    def put(args):
        corp = args['corp']
        promotion_id = args['id']
        corp.promotion_repository.enable_promotion(promotion_id)
        return {}

    @param_required(['corp_id', 'id'])
    def delete(args):
        corp = args['corp']
        promotion_id = args['id']
        corp.promotion_repository.disable_promotion(promotion_id)
        return {}
