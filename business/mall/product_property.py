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
            result.append(_model)

        return result

    @property
    def properties(self):
        """

        """
        properties = self.context.get('properties', None)
        if not properties and self.id:
            return ProductTemplateProperty.from_template_id({"template_id": self.id})

        return properties

    @properties.setter
    def properties(self, properties):
        """

        """
        self.context['properties'] = properties

    def save(self):
        """
        添加

        """

        template = mall_models.ProductPropertyTemplate.create(owner=self.owner_id,
                                                              name=self.name,
                                                              )
        # ProductPropertyTemplate.bulk_create_template_property({'properties': self.properties,
        #                                                        'template_id': template.id,
        #                                                        'owner_id': self.owner_id})
        return ProductPropertyTemplate(template) if template else None

    def update(self):
        """
        更新

        """

        change_rows = mall_models.ProductPropertyTemplate.update(name=self.name).dj_where(id=self.id).execute()

        return change_rows

    @staticmethod
    @param_required(['id'])
    def delete_from_id(args):
        """
        删除商品属性模板
        """
        template_id = args.get('id')
        mall_models.TemplateProperty.delete().dj_where(template=template_id).execute()

        rs = mall_models.ProductPropertyTemplate.delete().dj_where(id=template_id).execute()
        return rs


class ProductTemplateProperty(business_model.Model):
    """
    模板管理的属性管理
    """
    __slots__ = (
        'id',
        'name',
        'value',
        'template_id',
        'owner_id'
    )

    def __init__(self, model):
        super(ProductTemplateProperty, self).__init__()
        if model:
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
        result = [ProductTemplateProperty(pro) for pro in properties]
        return result

    @staticmethod
    @param_required(['id'])
    def from_id(args):
        template_property = mall_models.TemplateProperty.select().dj_where(id=args['id']).get()
        if template_property:
            return ProductTemplateProperty(template_property)
        else:
            return None

    def save(self):
        db_model = mall_models.TemplateProperty.create(name=self.name,
                                                       owner=self.owner_id,
                                                       template=self.template_id,
                                                       value=self.value)
        return ProductTemplateProperty(db_model)

    def update(self):
        """

        """

        change_rows = mall_models.TemplateProperty.update(name=self.name,
                                                          value=self.value).dj_where(id=self.id).execute()
        return change_rows

    @staticmethod
    @param_required(['ids'])
    def delete_from_ids(args):
        """
        删除ids
        """
        change_rows = mall_models.TemplateProperty.delete().dj_where(id__in=args['ids']).execute()
        return change_rows
