# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business import model as business_model
from db.mall import models as mall_models
from business.mall.product_property import ProductPropertyTemplate, ProductTemplateProperty


class ProductPropertyFactory(business_model.Model):
    """
    商品属性模板工厂类
    """
    def __init__(self):
        super(ProductPropertyFactory, self).__init__()

    @staticmethod
    def create():
        """
        创造模板工厂类
        """
        return ProductPropertyFactory()

    @staticmethod
    @param_required(['owner_id', 'title'])
    def save(args):
        """

        """
        template = ProductPropertyTemplate(None)
        template.owner_id = args['owner_id']
        template.name = args['title']
        return template.save()


class ProductTemplatePropertyFactory(business_model.Model):
    """
    商品模板的属性工厂类
    """

    def __init__(self):
        super(ProductTemplatePropertyFactory, self).__init__()

    @staticmethod
    def create():
        """
        创造模板工厂类
        """
        return ProductTemplatePropertyFactory()

    @staticmethod
    @param_required(['template_id', 'name', 'value', 'owner_id'])
    def save(args):
        """

        """
        template_id = args['template_id']
        owner_id = args['owner_id']
        template_property = ProductTemplateProperty(None)
        template_property.template_id = template_id
        template_property.owner_id = owner_id
        template_property.name = args['name']
        template_property.value = args['value']
        rs = template_property.save()
        return rs

    @staticmethod
    @param_required(['template_id', 'properties', 'owner_id'])
    def save_many(args):
        properties = args['properties']
        template_id = args['template_id']
        owner_id = args['owner_id']
        model_properties = []
        for pro in properties:
            template_property = ProductTemplateProperty(None)
            template_property.name = pro['name']
            template_property.value = pro['value']
            template_property.owner_id = owner_id
            template_property.template_id = template_id
            temp = template_property.save()
            model_properties.append(ProductTemplateProperty(temp))

        return model_properties
