# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.promotion.promotion_factory import PromotionFactory
from business.mall.promotion.encode_promotion_service import EncodePromotionService


class APremiumSalePromotion(api_resource.ApiResource):
    """
    促销-买赠
    """
    app = 'promotion'
    resource = 'premium_sale_promotion'

    @param_required(['corp_id', 'id'])
    def get(args):
        corp = args['corp']
        promotion_id = args['id']

        fill_options = {
            'with_detail': True,
            'with_product': True,
        }
        promotion = corp.promotion_repository.get_promotion_by_id(promotion_id, fill_options=fill_options)
        if not promotion:
            return {}
        else:
            encode_promotion_service = EncodePromotionService.get(corp)
            products_info = encode_promotion_service.get_products_info(promotion)
            base_info = encode_promotion_service.get_base_info(promotion)
            detail_info = encode_promotion_service.get_detail_info(promotion)
            data = {
                'id': base_info['id'],
                'name': base_info['name'],
                'promotion_title': base_info['promotion_title'],
                'type': base_info['type'],
                'type_name': base_info['type_name'],
                'status': base_info['status'],
                'start_date': base_info['start_date'],
                'end_date': base_info['end_date'],
                'member_grade_id': base_info['member_grade_id'],
                'created_at': base_info['created_at'],
                'products_info': products_info,
                'detail': detail_info

            }
            return data

    @param_required(['corp_id', 'product_info', 'promotion_info', 'detail_info'])
    def put(args):
        """

        """
        factory = PromotionFactory.get(args['corp'])
        factory.create_promotion(args)
        return {}

    @param_required(['corp_id', 'ids'])
    def delete(args):
        corp = args['corp']
        promotion_ids = json.loads(args['ids'])

        corp.promotion_repository.delete_promotions(promotion_ids)
        return {}
