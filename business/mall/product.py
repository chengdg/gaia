# -*- coding: utf-8 -*-
from eaglet.decorator import param_required

from db.mall import models as mall_models
from business import model as business_model
from settings import PRODUCT_POOL_WEAPP_ID
from business.account.user_profile import UserProfile


class Product(business_model.Model):
    __slots__ = (
        'id',
        'owner_id',
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
        'min_limit',
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

        'is_model_deleted',
        'custom_model_properties',
        'model_type',
    )

    def __init__(self, model):
        super(Product, self).__init__()

        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

    @staticmethod
    def empty_product():
        product = Product(None)
        return product

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
        products = []
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

    @property
    def models(self):
        """

        """
        models = self.context.get('models', None)
        if not models and self.id:
            # return ProductTemplateProperty.from_template_id({"template_id": self.id})
            pass
        return models

    @models.setter
    def models(self, models):
        """

        """
        self.context['models'] = models

    def save(self, panda_product_id):
        owner = UserProfile.from_webapp_id({'webapp_id': PRODUCT_POOL_WEAPP_ID})
        product = mall_models.Product.create(
            owner=owner.user_id,
            name=self.name,
            supplier=self.supplier,
            detail=self.detail,
            pic_url='',
            introduction='',
            thumbnails_url=self.thumbnails_url,
            price=self.price,
            weight=self.weight,
            stock_type=0 if self.stock_type == 'unbound' else 1,
            stocks=self.stocks if self.stocks else 0,
            purchase_price=self.purchase_price

        )
        mall_models.PandaProductToProduct.create(
            owner=owner.user_id,
            panda_product_id=panda_product_id,
            weapp_product=product.id,
        )
        new_product = Product(product)
        if self.model_type == 'single':
            product_model = ProductModel(None)
            product_model.owner_id = owner.user_id
            product_model.product_id = product.id
            # 非定制规格
            product_model.is_standard = True
            product_model.stock_type = self.stock_type
            product_model.stocks = self.stocks
            product_model.price = self.price
            product_model.weight = self.weight
            new_product_model = product_model.save()
            # 用来设置规格信息

            new_product.models = [new_product_model]

        else:
            # 多个规格（定制）
            pass
        # 处理论播图
        # TODO 处理论播图
        return new_product


class ProductModel(business_model.Model):

    __slots__ = (
        'id',
        'owner_id',
        'product_id',
        'name',
        'is_standard',
        'price',
        'stock_type',
        'stocks',
        'weight'
    )

    def __init__(self, model):
        super(ProductModel, self).__init__()
        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

    def save(self):
        product_model = mall_models.ProductModel.create(
            owner=self.owner_id,
            product=self.product_id,
            name=self.name if self.name else '',
            is_standard=self.is_standard,
            price=self.price,
            stock_type=0 if self.stock_type == 'unbound' else 1,
            stocks=self.stocks if self.stocks else 0,
            weight=self.weight
        )
        return ProductModel(product_model)


class ProductSwipeImage(business_model.Model):
    __slots__ = ()

    def __init__(self, model):
        super(ProductSwipeImage, self).__init__()
        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)
        # mall_models.ProductSwipeImage
        #     product = product,
        #     url = swipe_image['url'],
        #     width = swipe_image['width'],
        #     height = swipe_image['height']