# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.common.page_info import PageInfo
from business.mall.promotion.encode_promotion_service import EncodePromotionService


class AIntegralSalePromotions(api_resource.ApiResource):
    """
    积分应用集合
    """
    app = 'promotion'
    resource = 'integral_sale_promotions'

    @param_required(['corp_id', '?filters:json'])
    def get(args):
        corp = args['corp']

        target_page = PageInfo.create({
            "cur_page": int(args.get('cur_page', 1)),
            "count_per_page": int(args.get('count_per_page', 10))
        })
        fill_options = {
            'with_detail': True,
            'with_product': True
        }
        filters = args.get('filters', {})
        promotions, page_info = corp.promotion_repository.search_integral_sale_promotions(target_page,
                                                                                 fill_options=fill_options,
                                                                                 filters=filters)
        datas = []
        encode_promotion_service = EncodePromotionService.get(corp)
        for promotion in promotions:
            base_info = encode_promotion_service.get_base_info(promotion)
            products_info = encode_promotion_service.get_products_info(promotion)
            detail_info = encode_promotion_service.get_detail_info(promotion)

            data = {
                'promotion_info': base_info,
                'products_info': products_info,
                'detail': detail_info
            }

            datas.append(data)

        return {
            'page_info': page_info.to_dict(),
            'integral_sale_promotions': datas
        }

