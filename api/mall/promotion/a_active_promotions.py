# -*- coding: utf-8 -*-

import json

from eaglet.core import api_resource
from eaglet.decorator import param_required


class AActivePromotions(api_resource.ApiResource):
    """
    正在进行的促销活动集合
    """
    app = 'promotion'
    resource = 'active_promotions'

    @param_required(['corp_id', 'ids'])
    def delete(args):
        corp = args['corp']
        promotion_ids = json.loads(args['ids'])
        corp.promotion_repository.disable_promotions(promotion_ids)
        return {}
