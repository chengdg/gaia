# -*- coding: utf-8 -*-
__author__ = 'charles'

from eaglet.decorator import param_required

from business import model as business_model
from db.mall import models as mall_models
from business.product.model.product_model_property_value import ProductModelPropertyValue


class ProductModelProperty(business_model.Model):
    """
    商品的规格管理
    """
    __slots__ = (
        'id',
        'name',
        'type',
    )

    def __init__(self, model):
        business_model.Model.__init__(self)

        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

        if self.type == mall_models.PRODUCT_MODEL_PROPERTY_TYPE_TEXT:
            self.type = 'text'
        else:
            self.type = 'image'

    @staticmethod
    def from_model(db_model):
        product_model_property = ProductModelProperty(db_model)
        return product_model_property

    @property
    def values(self):
        """
        商品规格属性的属性值集合
        """
        value_models = mall_models.ProductModelPropertyValue.select().dj_where(property=self.id, is_deleted=False)

        property_values = []
        for value_model in value_models:
            property_values.append(ProductModelPropertyValue.from_model({
                'db_model': value_model
            }))
        return property_values

    def update(self, field, value):
        """
        更新商品规格属性
        """
        if field == 'name':
            #更新name
            mall_models.ProductModelProperty.update(name=value).dj_where(id=self.id).execute()
        elif field == 'type':
            #更新type
            model_type = mall_models.PRODUCT_MODEL_PROPERTY_TYPE_TEXT
            if value == 'image':
                model_type = mall_models.PRODUCT_MODEL_PROPERTY_TYPE_IMAGE
            mall_models.ProductModelProperty.update(type=model_type).dj_where(id=self.id).execute()

    def add_property_value(self, name, pic_url):
        """
        向商品规格属性中添加一个property value（规格值）
        """
        property_value = mall_models.ProductModelPropertyValue.create(
            property = self.id,
            name = name,
            pic_url = pic_url
        )

        return property_value

    @staticmethod
    @param_required(['corp', 'name', 'type'])
    def create(args):
        #确定type
        type = mall_models.PRODUCT_MODEL_PROPERTY_TYPE_TEXT
        if args['type'] == 'image':
            type = mall_models.PRODUCT_MODEL_PROPERTY_TYPE_IMAGE

        product_model = mall_models.ProductModelProperty.create(
                            name=args['name'],
                            type=type,
                            owner=args['corp'].id
                        )

        if product_model:
            model = ProductModelProperty(product_model)
            return model
        else:
            return None

    def is_product_used(self, corp):
        is_using_product_model_id = []
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
                product_model_id = product_model_data.split(':')[0]
                if product_model_id not in is_using_product_model_id:
                    is_using_product_model_id.append(product_model_id)

        if str(self.id) in is_using_product_model_id:
            return True
        else:
            return False