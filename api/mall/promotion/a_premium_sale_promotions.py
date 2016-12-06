# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.common.page_info import PageInfo
from business.mall.promotion.encode_promotion_service import EncodePromotionService


class APremiumSalePromotions(api_resource.ApiResource):
    """
    促销-买赠
    """
    app = 'promotion'
    resource = 'premium_sale_promotions'

    @param_required(['corp_id'])
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
        filters = json.loads(args.get('filters', '{}'))
        # filters['__f-product_name-contains'] = '葡萄酒'
        promotions, page_info = corp.promotion_repository.search_premium_sale_promotions(target_page,
                                                                                         fill_options=fill_options,
                                                                                         filters=filters)
        datas = []
        encode_promotion_service = EncodePromotionService.get(corp)
        for promotion in promotions:
            base_info = encode_promotion_service.get_base_info(promotion)
            product_info = encode_promotion_service.get_product_info(promotion)
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
                'detail': detail_info,
            }

            datas.append(data)

        return {
            'page_info': page_info.to_dict(),
            'premium_sale_promotions': datas
        }

