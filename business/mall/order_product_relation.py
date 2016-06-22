# -*- coding: utf-8 -*-

from eaglet.decorator import param_required

from db.mall import models as mall_models
from business import model as business_model
from business.mall.product import Product

class OrderProductRelation(business_model.Model):
    """订单商品
    """
    __slots__ = (
        'id',
        'order_id',
        'product_id',
        'product_name',
        'product_model_name',
        'price',
        'total_price',
        'is_shiped',
        'number',
        'promotion_id',
        'promotion_money',
        'grade_discounted_money',
        'integral_sale_id',
        'origin_order_id',
        'purchase_price'
    )

    def __init__(self, model):
        business_model.Model.__init__(self)

        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

    @staticmethod
    @param_required(['product_ids'])
    def get_for_product(args):
        relation_models = mall_models.OrderHasProduct.select().join(mall_models.Product).where(
            mall_models.OrderHasProduct.product.in_(args['product_ids'])
        )
        relations = []
        for relation_model in relation_models:
            relation = OrderProductRelation(relation_model)
            relations.append(relation)
        return relations

    @staticmethod
    @param_required(['order_ids'])
    def get_for_order(args):
        relation_models = mall_models.OrderHasProduct.select().join(mall_models.Product).where(
            mall_models.OrderHasProduct.order.in_(args['order_ids'])
        )
        relations = []
        for relation_model in relation_models:
            relation = OrderProductRelation(relation_model)
            relations.append(relation)
        return relations
