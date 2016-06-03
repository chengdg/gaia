# -*- coding: utf-8 -*-
from eaglet.decorator import param_required

from db.mall import models as mall_models
from business import model as business_model

class Product(business_model.Model):
    __slots__ = (
        'id',
        'name',
        'physical_unit',
        'price',
        'introduction',
        'weight',
        'thumbnails_url',
        'pic_url',
        'detail',
        'remark',
        'display_index',
        'created_at',
        'shelve_type',
        'shelve_start_time',
        'shelve_end_time',
        'stock_type',
        'stocks',
        'is_deleted',
        'is_support_make_thanks_card',
        'type',
        'update_time',
        'postage_id',
        'is_use_online_pay_interface',
        'is_use_cod_pay_interface',
        'promotion_title',
        'user_code',
        'bar_code',
        'unified_postage_money',
        'postage_type',
        'is_member_product',
        'supplier',
        'supplier_user_id',
        'supplier_name',
        'purchase_price',
        'is_enable_bill',
        'is_delivery',
        'buy_in_supplier',

        'model',
        'model_name',
        'is_model_deleted',
        'custom_model_properties'
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
    @param_required(['product_id'])
    def from_id(args):
        product_db_model = mall_models.Product.get(id=args['product_id'])
        return Product(product_db_model)

    @staticmethod
    @param_required(['product_ids'])
    def from_ids(args):
        product_models = mall_models.Product.select().dj_where(id__in=args['product_ids'])
        prodcts = []
        for model in product_models:
            products.append(Product(model))
        return products

    def fill_specific_model(self, model_name):
        product_model = mall_models.ProductModel.select().dj_where(product_id=self.id, name=model_name).first()
        product = self
        product.price = product_model.price
        product.weight = product_model.weight
        product.stock_type = product_model.stock_type
        product.stocks = product_model.stocks
        product.model_name = model_name
        product.model = product_model
        product.is_model_deleted = False
        product.user_code = product_model.user_code
        if product_model.is_deleted:
            product.is_model_deleted = True

        property_ids = []
        property_value_ids = []
        name = product.model_name
        if product.model_name != 'standard':
            for model_property_info in product.model_name.split('_'):
                property_id, property_value_id = model_property_info.split(':')
                property_ids.append(property_id)
                property_value_ids.append(property_value_id)

                id2property = dict(
                    [
                        (property.id, {"id": property.id, "name": property.name})
                        for property in mall_models.ProductModelProperty.select().dj_where(id__in=property_ids)
                    ])
                for property_value in mall_models.ProductModelPropertyValue.select().dj_where(id__in=property_value_ids):
                    id2property[property_value.property_id]['property_value'] = property_value.name
                    id2property[property_value.property_id]['property_pic_url'] = property_value.pic_url
            product.custom_model_properties = id2property.values()
            product.custom_model_properties.sort(lambda x, y: cmp(x['id'], y['id']))
        else:
            product.custom_model_properties = None