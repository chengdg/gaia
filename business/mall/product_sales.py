# -*- coding: utf-8 -*-
from eaglet.decorator import param_required

from db.mall import models as mall_models
from business import model as business_model

class ProductSales(business_model.Model):
    __slots__ = (
        'product_id',
        'sales'
    )

    def __init__(self, model):
        business_model.Model.__init__(self)

        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

    @staticmethod
    @param_required(['db_model'])
    def from_model(args):
        model = args['db_model']
        product = Product(model)
        return product

    @staticmethod
    @param_required(['product_ids'])
    def from_ids(args):
        product_sales_models = mall_models.ProductSales.select().dj_where(product_id__in=args['product_ids'])
        product_sales = []
        for model in product_sales_models:
            product_sales.append(ProductSales(model))
        return product_sales