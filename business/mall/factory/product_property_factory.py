# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business import model as business_model
from db.mall import models as mall_models
from business.mall.product_property import ProductPropertyTemplate


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
    @param_required(['owner_id', 'title', 'properties'])
    def save(args):
        """

        """
        template = ProductPropertyTemplate(None)
        template.owner_id = args['owner_id']
        template.name = args['title']
        template.properties = args['properties']
        return template.save()
