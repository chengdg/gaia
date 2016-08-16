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
        'pic_url',

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

    @staticmethod
    @param_required(['id'])
    def from_id(args):
        db_model = mall_models.ProductModelPropertyValue.select().dj_where(id=args.get('id'),
                                                                           is_deleted=False).first()
        if db_model:
            return ProductModelPropertyValue(db_model)
        return None

    @staticmethod
    @param_required(['model_id'])
    def from_model_id(args):
        """
        从规格id获取所有的规格属性
        """
        values = mall_models.ProductModelPropertyValue.select().dj_where(property=args['model_id'])
        result = [ProductModelPropertyValue(value) for value in values]
        return result

    @staticmethod
    @param_required(['property_id', 'name', 'pic_url'])
    def create(args):
        value_model = mall_models.ProductModelPropertyValue.create(property=args['property_id'],
                                                                   name=args['name'],
                                                                   pic_url=args['pic_url'])
        return ProductModelPropertyValue(value_model) if value_model else None

    def update(self):
        change_rows = mall_models.ProductModelPropertyValue.update(
                        name=self.name,
                        pic_url=self.pic_url
                    ).dj_where(id=self.id).execute()
        return change_rows

    @staticmethod
    @param_required(['id'])
    def delete_from_id(args):
        change_rows = mall_models.ProductModelPropertyValue.update(is_deleted=True) \
            .dj_where(id=args['id']).execute()
        return change_rows