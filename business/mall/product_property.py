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
            result.append({'template': _model,
                           'properties': _model.properties})

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
        ProductPropertyTemplate.bulk_create_template_property({'properties': self.properties,
                                                               'template_id': template.id,
                                                               'owner_id': self.owner_id})
        return ProductPropertyTemplate(template) if template else None

    def update(self, new_properties, update_properties, deleted_ids):
        """
        生产

        """

        change_rows = mall_models.ProductPropertyTemplate.update(name=self.name).dj_where(id=self.id).execute()
        #
        if new_properties:
            # dict(properties=new_properties,
            #      template_id=template_id,
            #      owner_id=owner_id, )
            change_rows += ProductPropertyTemplate.bulk_create_template_property({"properties": new_properties,
                                                                                  "template_id": self.id,
                                                                                  "owner_id": self.owner_id})
        if update_properties:
            for update_property in update_properties:
                change_rows += mall_models.TemplateProperty.update(name=update_property.get('name'),
                                                                   value=update_property.get('value')) \
                    .dj_where(id=update_property.get('id')).execute()
        #
        if deleted_ids:
            change_rows += mall_models.TemplateProperty.delete().dj_where(id__in=deleted_ids).execute()
        return change_rows

    @staticmethod
    @param_required(['template_id', 'owner_id', 'properties'])
    def bulk_create_template_property(args):
        """
        批量插入,模板属性
        template_id --　模板id
        owner_id -- 用户id
        properties -- 属性[dict(name='', value=''), ]
        """
        data_resource = []
        properties = args.get('properties')
        owner_id = args.get('owner_id')
        template_id = args.get('template_id')
        for template_property in properties:
            data_resource.append(dict(owner=owner_id,
                                      template=template_id,
                                      name=template_property['name'],
                                      value=template_property['value']))

        if data_resource:
            return mall_models.TemplateProperty.insert_many(data_resource).execute()

    @staticmethod
    @param_required(['id'])
    def delete_from_id(args):
        """
        删除商品属性模板
        """
        template_id = args.get('id')
        rs = mall_models.TemplateProperty.delete().dj_where(template=template_id).execute()
        if rs > 0:

            mall_models.ProductPropertyTemplate.delete().dj_where(id=template_id).execute()
            return rs
        return 0


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
        super(ProductTemplateProperty, self).__init__()
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
