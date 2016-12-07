# -*- coding: utf-8 -*-


import json
from business import model as business_model
from db.mall import promotion_models

from business.mall.promotion.premium_sale import PremiumSale


class PromotionFactory(business_model.Service):
    """
    促销工厂类
    """
    def __create_flash_sale(self, promotion_data):
        flash_sale = promotion_models.FlashSale.create(
            owner=self.corp,
            limit_period=promotion_data['limit_period'],
            promotion_price=promotion_data['promotion_price'],
            count_per_purchase=promotion_data['count_per_purchase'],
            count_per_perio=promotion_data['count_per_perio']
        )

    def __create_integral_sale(self):
        pass

    def __create_premium_sale(self, promotion_data):
        is_enable_cycle_mode = True if promotion_data['is_enable_cycle'] == 'true' else False
        premium_sale = promotion_models.PremiumSale.create(owner=self.corp.id,
                                                           count=promotion_data['count'],
                                                           is_enable_cycle_mode=is_enable_cycle_mode)
        return PremiumSale(premium_sale)

    def __add_product_to_promotion(self, product_ids, promotion):
        product_ids = json.loads(product_ids)
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
            member_grade_id=promotion_data.get('member_grade', 0),
            start_date=promotion_data['start_date'],
            end_date=promotion_data['end_date'],
            detail_id=promotion_detail_id
        )
        return promotion

    def __add_product_to_premium_sale(self, promotion_data, premium_sale):

        promotion_models.PremiumSaleProduct.create(
            owner=self.corp.id,
            product=promotion_data['premium_product_id'],
            premium_sale=premium_sale.id,
            count=promotion_data['premium_count'],
            unit=promotion_data['unit']
        )

    def create_promotion(self, promotion_data):
        if promotion_data['type'] == 'flash_sale':
            flash_sale = self.__create_flash_sale(promotion_data)

            promotion_detail_id = flash_sale.id
            promotion_data['type'] = promotion_models.PROMOTION_TYPE_PREMIUM_SALE
        elif promotion_data['type'] == 'premium_sale':
            premium_sale = self.__create_premium_sale(promotion_data)
            self.__add_product_to_premium_sale(promotion_data, premium_sale)
            promotion_detail_id = premium_sale.id
            promotion_data['type'] = promotion_models.PROMOTION_TYPE_PREMIUM_SALE
        promotion = self.__create_promotion(promotion_data, promotion_detail_id)
        self.__add_product_to_promotion(promotion_data['product_ids'], promotion)
