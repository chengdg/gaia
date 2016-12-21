# -*- coding: utf-8 -*-

import json
from business import model as business_model
from db.mall import promotion_models

from business.mall.promotion.premium_sale import PremiumSale
from business.mall.promotion.flash_sale import FlashSale
from business.mall.promotion.integral_sale import IntegralSale


class PromotionFactory(business_model.Service):
    """
    促销工厂类
    """
    def __create_flash_sale(self, promotion_data):
        flash_sale = promotion_models.FlashSale.create(
            owner=self.corp.id,
            limit_period=promotion_data['limit_period'],
            promotion_price=promotion_data['promotion_price'],
            count_per_purchase=promotion_data['count_per_purchase'],
            count_per_period=promotion_data['count_per_period']
        )
        return flash_sale

    def __create_integral_sale(self, detail_info):
		# TODO 判断商品是否在做其他促销
        integral_sale = promotion_models.IntegralSale.create(
            owner=self.corp.id,
            type=promotion_models.INTEGRAL_SALE_TYPE_PARTIAL,
            discount=0,
            discount_money=0.0,
            integral_price=0,
            is_permanant_active=detail_info.get('is_permanant_active', 'false') == 'true'
        )
        for rule in detail_info.get("rules"):
            promotion_models.IntegralSaleRule.create(
                owner=self.corp.id,
                integral_sale=integral_sale,
                member_grade_id=rule['member_grade_id'],
                discount=rule['discount'],
                discount_money=rule['discount_money']
            )
        return IntegralSale(integral_sale)

    def __create_premium_sale(self, detail_data):
        is_enable_cycle_mode = True if detail_data['is_enable_cycle'] == 'true' else False
        premium_sale = promotion_models.PremiumSale.create(owner=self.corp.id,
                                                           count=detail_data['count'],
                                                           is_enable_cycle_mode=is_enable_cycle_mode)
        return PremiumSale(premium_sale)

    def __add_product_to_promotion(self, product_ids, promotion):
        for product_id in product_ids:
            promotion_models.ProductHasPromotion.create(
                product=product_id,
                promotion=promotion
            )

    def __create_promotion(self, promotion_data, promotion_detail_id):
        promotion = promotion_models.Promotion.create(
            owner=self.corp.id,
            type=promotion_data['type'],
            name=promotion_data['name'],
            promotion_title=promotion_data.get('promotion_title', ''),
            status=promotion_data.get('status', promotion_models.PROMOTION_STATUS_NOT_START),
            member_grade_id=promotion_data.get('member_grade') if promotion_data.get('member_grade') else 0,
            start_date=promotion_data['start_date'],
            end_date=promotion_data['end_date'],
            detail_id=promotion_detail_id
        )
        return promotion

    def __add_product_to_premium_sale(self, detail_data, premium_sale):

        promotion_models.PremiumSaleProduct.create(
            owner=self.corp.id,
            product=detail_data['premium_product_id'],
            premium_sale=premium_sale.id,
            count=detail_data['premium_count'],
            unit=detail_data['unit']
        )

    def create_promotion(self, promotion_data):
        product_info = json.loads(promotion_data['product_info'])
        promotion_info = json.loads(promotion_data['promotion_info'])
        detail_info = json.loads(promotion_data['detail_info'])

        promotion_detail = None
        if promotion_info['type'] == 'flash_sale':
            flash_sale = self.__create_flash_sale(detail_info)
            promotion_detail = flash_sale
            promotion_info['type'] = promotion_models.PROMOTION_TYPE_FLASH_SALE
        elif promotion_info['type'] == 'premium_sale':
            premium_sale = self.__create_premium_sale(detail_info)
            self.__add_product_to_premium_sale(detail_info, premium_sale)
            promotion_detail = premium_sale
            promotion_info['type'] = promotion_models.PROMOTION_TYPE_PREMIUM_SALE
        elif promotion_info['type'] == 'integral_sale':
            promotion_info['type'] = promotion_models.PROMOTION_TYPE_INTEGRAL_SALE
            integral_sale = self.__create_integral_sale(detail_info)
            promotion_detail = integral_sale

        promotion = self.__create_promotion(promotion_info, promotion_detail.id)
        self.__add_product_to_promotion(product_info['product_ids'], promotion)
