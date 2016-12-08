# -*- coding: utf-8 -*-

import json
from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.promotion.encode_promotion_service import EncodePromotionService
from business.mall.promotion.promotion_factory import PromotionFactory


class APromotionFlashSale(api_resource.ApiResource):
    """
    促销-限时抢购
    """
    app = 'promotion'
    resource = 'flash_sale'

    @param_required(['corp_id', 'id'])
    def get(args):
        corp = args['corp']
        ids = [args['id']]

        fill_options = {
            'with_detail': True,
            'with_product': True
        }
        promotions = corp.promotion_repository.get_promotion_by_ids(promotion_ids=ids, fill_options=fill_options)
        if len(promotions) == 0:
            return {}
        else:
            promotion = promotions[0]
            encode_promotion_service = EncodePromotionService.get(corp)
            base_info = encode_promotion_service.get_base_info(promotion)
            products_info = encode_promotion_service.get_products_info(promotion)
            detail_info = encode_promotion_service.get_detail_info(promotion)
            data = {
                'promotion_info': base_info,
                'products_info': products_info,
                'detail': detail_info
            }
            return data


    @param_required(['corp_id', 'promotion_info', 'detail_info', 'product_info'])
    def put(args):
        promotion_factory = PromotionFactory(args['corp'])
        promotion_factory.create_promotion(args)
        return {}


    @param_required(['corp_id', 'ids'])
    def delete(args):
        corp = args['corp_id']
        promotion_ids = args['ids']
        corp.promotion_repository.delete_promotions(promotion_ids=json.loads(promotion_ids))
        return {}