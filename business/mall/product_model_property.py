# -*- coding: utf-8 -*-

from eaglet.decorator import param_required

from business import model as business_model
from db.mall import models as mall_models


class ProductModelProperty(business_model.Model):
    """
    商品的规格管理
    """

    __slots__ = (
        'id',
        'name',
        'owner_id',
        'type',
    )

    def __init__(self, model):
        super(ProductModelProperty, self).__init__()
        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

    @staticmethod
    @param_required(['id'])
    def from_id(args):
        product_model_property = mall_models.ProductModelProperty.select()\
            .dj_where(id=args['id'], is_deleted=False).first()

        if product_model_property:

            # 使用from_model将数据取回到领域模型
            return ProductModelProperty(product_model_property)
        return None

    @staticmethod
    @param_required(['db_model'])
    def from_model(args):
        model = args['db_model']
        product_model_property = ProductModelProperty(model)
        return product_model_property

    @staticmethod
    @param_required(['owner_id'])
    def from_owner_id(args):
        """
        根据用户id获取所有属性模板
        """
        templates = mall_models.ProductModelProperty.select().dj_where(owner_id=args['owner_id'],
                                                                       is_deleted=False)
        result = []
        for template in templates:
            _model = ProductModelProperty.from_model({'db_model': template})
            result.append({'product_model': _model,
                           'properties': _model.properties})
        return result

    @property
    def properties(self):
        """
        """
        properties = self.context.get('properties', None)
        if not properties and self.id:
            return ProductModelPropertyValue.from_model_id({'model_id': self.id})
        return properties

    @properties.setter
    def properties(self, value):
        self.context['properties'] = value

    def update(self):
        """
        更新

        """

        # default 0(text)
        model_type = mall_models.PRODUCT_MODEL_PROPERTY_TYPE_TEXT
        if self.type == 'image':
            model_type = mall_models.PRODUCT_MODEL_PROPERTY_TYPE_IMAGE
        change_rows = mall_models.ProductModelProperty.update(name=self.name,
                                                              type=model_type).dj_where(id=self.id) \
            .execute()
        return change_rows

    def save(self):
        """
        新增

        """

        # default 0(text)
        model_type = mall_models.PRODUCT_MODEL_PROPERTY_TYPE_TEXT
        if self.type == 'image':
            model_type = mall_models.PRODUCT_MODEL_PROPERTY_TYPE_IMAGE
        product_model = mall_models.ProductModelProperty.create(name=self.name,
                                                                type=model_type,
                                                                owner=self.owner_id)
        return ProductModelProperty(product_model) if product_model else None

    @staticmethod
    @param_required(['id'])
    def delete_from_id(args):
        change_rows = mall_models.ProductModelProperty.update(is_deleted=True) \
            .dj_where(id=args.get('id')).execute()
        return change_rows


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

    def save(self, model_id):
        value_model = mall_models.ProductModelPropertyValue.create(property=model_id,
                                                                   name=self.name,
                                                                   pic_url=self.pic_url)
        return ProductModelPropertyValue(value_model) if value_model else None

    def update(self):
        change_rows = mall_models.ProductModelPropertyValue.update(name=self.name,
                                                                   pic_url=self.pic_url) \
            .dj_where(id=self.id).execute()
        return change_rows

    @staticmethod
    @param_required(['id'])
    def delete_from_id(args):
        change_rows = mall_models.ProductModelPropertyValue.update(is_deleted=True) \
            .dj_where(id=args['id']).execute()
        return change_rows
