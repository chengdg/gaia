# -*- coding: utf-8 -*-


import json
from business import model as business_model
from db.mall import promotion_models

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

    def __create_premium_sale(self):
        pass

    def __add_product_to_promotion(self, promotion_data, promotion):
        products = json.loads(promotion_data['products'])
        for product in products:
            promotion_models.ProductHasPromotion.create(
                product_id=product['id'],
                promotion=promotion
            )

    def __create_promotion(self, promotion_data, promotion_detail_id):
        promotion = promotion_models.Promotion.create(
            owner=self.crop,
            type=promotion_data['type'],
            name=promotion_data['promotion_title'],
            promotion_title=promotion_data['promotion_title'],
            status=promotion_data['status'],
            member_grade_id=promotion_data['member_grade'],
            start_date=promotion_data['start_date'],
            end_date=promotion_data['end_date'],
            detail_id=promotion_detail_id
        )

    def create_promotion(self, promotion_data):
        if promotion_data['type'] == 'flash_sale':
            flash_sale = self.__create_flash_sale(promotion_data)
        promotion_detail_id = flash_sale.id
        promotion = self.__create_promotion(promotion_data, promotion_detail_id)
        self.__add_product_to_promotion(promotion_data, promotion)
