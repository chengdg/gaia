# -*- coding: utf-8 -*-
__author__ = 'Eugene'

from eaglet.decorator import param_required

from business import model as business_model
from db.mall import models as mall_models

class ProductModelPropertyValue(business_model.Model):
    """
    商品规格的具体值（属性值）
    """
    __slots__ = (
        'id',
        'name',
        'pic_url'
    )

    def __init__(self, model):
        super(ProductModelPropertyValue, self).__init__()
        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

    @staticmethod
    @param_required(['db_model'])
    def from_model(args):
        model = args['db_model']
        product_model_property = ProductModelPropertyValue(model)
        return product_model_property

    def update(self):
        change_rows = mall_models.ProductModelPropertyValue.update(
                        name=self.name,
                        pic_url=self.pic_url
                    ).dj_where(id=self.id).execute()
        return change_rows