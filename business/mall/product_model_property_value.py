# -*- coding: utf-8 -*-
from eaglet.decorator import param_required

from db.mall import models as mall_models
from business import model as business_model

class ProductModelPropertyValue(business_model.Model):
    __slots__ = (
        'id',
        'property_id',
        'name',
        'pic_url',
        'is_deleted',
        'created_at'
    )

    def __init__(self, model):
        business_model.Model.__init__(self)

        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

    @staticmethod
    @param_required(['ids', 'property_ids'])
    def from_ids_and_property_ids(args):
        value_models = mall_models.ProductModelPropertyValue.select().dj_where(
                id__in=args['ids'],
                property_id__in=args['property_ids']
            )
        property_values = []
        for model in value_models:
            property_values.append(ProductModelPropertyValue(model))
        return property_values