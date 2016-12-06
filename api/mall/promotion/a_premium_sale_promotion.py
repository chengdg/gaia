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
            'with_premium_product': True
        }
        promotion = corp.promotion_repository.get_promotion_by_id(promotion_id, fill_options=fill_options)
        if not promotion:
            return {}
        else:
            encode_promotion_service = EncodePromotionService.get(corp)
            product_info = encode_promotion_service.get_product_info(promotion)
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
                'product_info': product_info,
                'detail': detail_info

            }
            return data

    @param_required(['corp_id', 'product_id', 'premium_product_id', 'name', 'start_date', 'end_date',
                     'count', 'is_enable_cycle'])
    def put(args):
        """
        product_id: 参加活动的商品
        premium_product_id: 赠送的商品
        name: 促销活动的名字
        start_date: 促销开始时间
        end_date: 促销结束时间
        count: 购买基数
        is_enable_cycle: 是否可循环购买 true: false (默认true)
        premium_count: 赠送基数
        unit: 赠送单位

        promotion_title: 促销标题
        member_grade: 会员等级id
        """
        factory = PromotionFactory.get(args['corp'])
        args['type'] = 'premium_sale'
        factory.create_promotion(args)
        return {}

    @param_required(['corp_id', 'ids'])
    def delete(args):
        corp = args['corp']
        promotion_ids = json.loads(args['ids'])

        corp.promotion_repository.delete_promotions(promotion_ids)
        return {}
