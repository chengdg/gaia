# -*- coding: utf-8 -*-

from eaglet.decorator import param_required

from business import model as business_model
from db.mall import models as mall_models


class ProductModelProperty(business_model.Model):
    """
    商品的属性管理
    """

    __slots__ = (
        'id',
        'name',
        'owner_id',
        'type',
        'properties'
    )

    def __init__(self, model):
        super(ProductModelProperty, self).__init__()
        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

    @staticmethod
    @param_required(['id'])
    def from_id(args):
        product_model_properties = mall_models.ProductModelPropertyValue.select(mall_models.ProductModelPropertyValue,
                                                                                mall_models.ProductModelProperty)\
            .join(mall_models.ProductModelProperty)\
            .dj_where(property=args['id'])
        product_model = product_model_properties.first().property
        product_model.properties = product_model_properties
        # 使用from_model将数据取回到领域模型
        return ProductModelProperty.from_model(dict(db_model=product_model)).to_dict(), 'Success'

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
        templates = mall_models.ProductPropertyTemplate.select().dj_where(owner_id=args['owner_id'])
        result = []
        for template in templates:
            template.properties = mall_models.TemplateProperty.select().dj_where(template=template)
            # 使用from_model将数据取回到领域模型
            result.append(ProductModelProperty.from_model(dict(db_model=template)).to_dict())
        return result

    @staticmethod
    def create(resource_model):
        """
        创造新规格
        """

        db_model = mall_models.ProductModelProperty.create(name='',
                                                           owner=resource_model.owner_id,
                                                           type=mall_models.PRODUCT_MODEL_PROPERTY_TYPE_TEXT)
        result = ProductModelProperty.from_model(dict(db_model=db_model))
        return result.to_dict(), 'Success'

    @staticmethod
    @param_required(['resource_model'])
    def save(args):
        """
        更新

        """

        resource_model = args.get('resource_model')
        model_types = [mall_models.PRODUCT_MODEL_PROPERTY_TYPE_TEXT, mall_models.PRODUCT_MODEL_PROPERTY_TYPE_IMAGE]
        model_type = resource_model.type if resource_model.type and int(resource_model.type) in [model_types] \
            else mall_models.PRODUCT_MODEL_PROPERTY_TYPE_TEXT
        mall_models.ProductModelProperty.update(name=resource_model.name,
                                                type=model_type).dj_where(id=resource_model.id)\
            .execute()
        return '', 'Success'

    @staticmethod
    @param_required(['id'])
    def delete_from_id(args):
        mall_models.ProductModelProperty.update(is_deleted=True) \
            .dj_where(id=args.get('id')).execute()
        return '', 'Success'

    def to_dict(self, *extras, **kwargs):
        result = dict()
        if kwargs and 'slots' in kwargs:
            slots = kwargs['slots']
        else:
            slots = self.__slots__

        for slot in slots:
            result[slot] = getattr(self, slot, None)

        if extras:
            for item in extras:
                result[item] = getattr(self, item, None)
        properties = []
        for pro in self.properties:
            properties.append(ProductModelPropertyValue.from_model(dict(db_model=pro)).to_dict())
        result['properties'] = properties
        return result


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
    def create(resource_model):
        """
        创建
        """
        db_model = mall_models.ProductModelPropertyValue.create(property=resource_model.id,
                                                                name=resource_model.name,
                                                                pic_url=resource_model.pic_url)
        return ProductModelPropertyValue.from_model(dict(db_model=db_model)).to_dict(), 'Success'

    @staticmethod
    @param_required(['db_model'])
    def from_model(args):
        model = args['db_model']
        product_model_property = ProductModelPropertyValue(model)
        return product_model_property

    @staticmethod
    def save(resource_model):
        """
        更新
        """
        mall_models.ProductModelPropertyValue.update(name=resource_model.name,
                                                     pic_url=resource_model.pic_url)\
            .dj_where(id=resource_model.id).execute()
        return '', 'Success'

    @staticmethod
    @param_required(['id'])
    def from_id(args):
        db_model = mall_models.ProductModelPropertyValue.select().dj_where(id=args.get('id')).get()
        return ProductModelPropertyValue.from_model(dict(db_model=db_model)).to_dict(), 'Success'

    @staticmethod
    @param_required(['id'])
    def delete_from_id(args):
        mall_models.ProductModelPropertyValue.update(is_deleted=True) \
            .dj_where(id=args.get('id')).execute()
        return '', 'Success'
