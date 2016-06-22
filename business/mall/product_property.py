# -*- coding: utf-8 -*-

from eaglet.decorator import param_required

from business import model as business_model
from db.mall import models as mall_models


class ProductPropertyTemplate(business_model.Model):
    """
    商品的属性管理
    """

    __slots__ = (
        'id',
        'name',
        'owner_id',
    )

    def __init__(self, model):
        super(ProductPropertyTemplate, self).__init__()
        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

    @staticmethod
    @param_required(['id'])
    def from_id(args):
        template = mall_models.ProductPropertyTemplate.select().dj_where(id=args['id']).first()
        if template:
            _model = ProductPropertyTemplate(template)
            return _model
        return None

    @staticmethod
    @param_required(['db_model'])
    def from_model(args):
        model = args['db_model']
        order = ProductPropertyTemplate(model)
        return order

    @staticmethod
    @param_required(['owner_id'])
    def from_owner_id(args):
        """
        根据用户id获取所有属性模板
        """
        templates = mall_models.ProductPropertyTemplate.select().dj_where(owner_id=args['owner_id'])
        result = []
        for template in templates:

            _model = ProductPropertyTemplate.from_model({'db_model': template})

            # 使用from_model将数据取回到领域模型
            result.append({'entry': _model,
                           'properties': _model.properties})

        return result

    @property
    def properties(self):
        """

        """

        if self.id:
            return ProductTemplateProperty.from_template_id({"template_id": self.id})

        return self.properties

    @properties.setter
    def properties(self, properties):
        """

        """
        self.properties = properties


class ProductTemplateProperty(business_model.Model):
    """
    模板管理的属性管理
    """
    __slots__ = (
        'id',
        'name',
        'value'
    )

    def __init__(self, model):
        business_model.Model.__init__(self)
        self.context['db_model'] = model
        if model:
            model.product_count = 0
            self._init_slot_from_model(model)

    @staticmethod
    @param_required(["db_model"])
    def from_model(args):
        db_model = args['db_model']
        return ProductTemplateProperty(db_model)

    @staticmethod
    @param_required(['template_id'])
    def from_template_id(args):
        properties = mall_models.TemplateProperty.select().dj_where(template=args['template_id'])
        result = [ProductTemplateProperty.from_model({'db_model': pro}) for pro in properties]
        return result

    @staticmethod
    @param_required(['id'])
    def from_id(args):
        template_property = mall_models.TemplateProperty.select().dj_where(id=args['id']).get()
        if template_property:
            return ProductTemplateProperty(template_property)
        else:
            return None
