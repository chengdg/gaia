# -*- coding: utf-8 -*-

import json

from eaglet.core import api_resource
from eaglet.decorator import param_required


class AActivePremiumSalePromotion(api_resource.ApiResource):
    """
    开启一个买赠促销活动
    """
    app = 'promotion'
    resource = 'active_premium_sale_promotion'

    @param_required(['corp_id', 'ids'])
    def put(args):
        corp = args['corp']
        promotion_ids = args['ids']
        promotion_ids = json.loads(promotion_ids)
        promotion_repository = corp.promotion_repository
        promotion_repository.active_promotions(promotion_ids)
        return {}

    @param_required(['corp_id', 'ids'])
    def delete(args):
        corp = args['corp']
        promotion_ids = args['ids']
        promotion_ids = json.loads(promotion_ids)
        promotion_repository = corp.promotion_repository
        promotion_repository.off_promotions(promotion_ids)
        return {}
