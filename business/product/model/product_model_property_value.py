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
        is_using_product_model_value_id = []
        product_ids = [model.product_id for model in mall_models.ProductPool.select().dj_where(
            woid=corp.id,
            status__in=[mall_models.PP_STATUS_OFF, mall_models.PP_STATUS_ON])]
        product_model_data_models = mall_models.ProductModel.select().dj_where(
            product_id__in=product_ids,
            name__not='standard',
            is_deleted=0
        )
        for model in product_model_data_models:
            product_model_datas = model.name.split('_')
            for product_model_data in product_model_datas:
                product_model_value_id = product_model_data.split(':')[1]
                if product_model_value_id not in is_using_product_model_value_id:
                    is_using_product_model_value_id.append(product_model_value_id)

        if str(self.id) in is_using_product_model_value_id:
            return True
        else:
            return False