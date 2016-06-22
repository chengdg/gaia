# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from eaglet.core import watchdog

from business import model as business_model
from db.mall import models as mall_models
from eaglet.core.exceptionutil import unicode_full_stack


class ProductModelPropertyFactory(business_model.Model):
    """
    商品属性规格工厂类
    """
    def __init__(self, model):
        super(ProductModelPropertyFactory, self).__init__()
        if model:
            self._init_slot_from_model(model)

    @staticmethod
    def create(resource_model):
        """
        创造新规格
        """
        model_types = [mall_models.PRODUCT_MODEL_PROPERTY_TYPE_TEXT, mall_models.PRODUCT_MODEL_PROPERTY_TYPE_IMAGE]
        model_type = resource_model.type \
            if resource_model.type and int(resource_model.type) in model_types \
            else mall_models.PRODUCT_MODEL_PROPERTY_TYPE_TEXT
        try:
            mall_models.ProductModelProperty.create(name=resource_model.name,
                                                    owner=resource_model.owner_id,
                                                    type=model_type)
            return 'SUCCESS', ''
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return 'FAILED', ''

    @staticmethod
    @param_required(['resource_model'])
    def save(args):
        """
        更新

        """

        resource_model = args.get('resource_model')
        model_types = [mall_models.PRODUCT_MODEL_PROPERTY_TYPE_TEXT, mall_models.PRODUCT_MODEL_PROPERTY_TYPE_IMAGE]
        model_type = resource_model.type if resource_model.type and int(resource_model.type) in model_types \
            else mall_models.PRODUCT_MODEL_PROPERTY_TYPE_TEXT
        try:
            mall_models.ProductModelProperty.update(name=resource_model.name,
                                                    type=model_type).dj_where(id=resource_model.id) \
                .execute()
        except:
            return 'FAILED', ''
        return "SUCCESS", ''

    @staticmethod
    @param_required(['id'])
    def delete_from_id(args):
        try:
            mall_models.ProductModelProperty.update(is_deleted=True) \
                .dj_where(id=args.get('id')).execute()
        except:
            return 'FAILED', ''
        return "SUCCESS", ''


class ProductModelPropertyValueFactory(business_model.Model):
    """

    """

    def __init__(self, model):
        super(ProductModelPropertyValueFactory, self).__init__()
        if model:
            self._init_slot_from_model(model)

    @staticmethod
    def create(resource_model):
        """
        创建
        """
        try:
            mall_models.ProductModelPropertyValue.create(property=resource_model.id,
                                                         name=resource_model.name,
                                                         pic_url=resource_model.pic_url)

        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return 'FAILED', ''
        return 'SUCCESS', ''

    @staticmethod
    def save(resource_model):
        """
        更新
        """
        try:
            mall_models.ProductModelPropertyValue.update(name=resource_model.name,
                                                         pic_url=resource_model.pic_url) \
                .dj_where(id=resource_model.id).execute()
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return 'FAILED', ''
        return "SUCCESS", ''

    @staticmethod
    @param_required(['id'])
    def delete_from_id(args):
        try:
            mall_models.ProductModelPropertyValue.update(is_deleted=True) \
                .dj_where(id=args.get('id')).execute()
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return 'FAILED', ''
        return "SUCCESS", ''
