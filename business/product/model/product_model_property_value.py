# -*- coding: utf-8 -*-
__author__ = 'Eugene'

from eaglet.decorator import param_required

from business import model as business_model
from business.mall.corporation_factory import CorporationFactory
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

    def is_used(self):
        corp = CorporationFactory.get()
        relation_models = mall_models.ProductModelHasPropertyValue.select().dj_where(property_value_id=self.id)
        if relation_models.count() > 0:
            product_model_ids = [relation_model.model_id for relation_model in relation_models]
            product_model_data_models = mall_models.ProductModel.select().dj_where(id__in=product_model_ids,
                                                                                   is_deleted=0)
            if product_model_data_models.count() > 0:
                product_ids = [model_data.product_id for model_data in product_model_data_models]
                if mall_models.ProductPool.select().dj_where(
                        woid=corp.id,
                        product_id__in=product_ids,
                        status__in=[mall_models.PP_STATUS_OFF, mall_models.PP_STATUS_ON]).count() > 0:
                    return True
        return False