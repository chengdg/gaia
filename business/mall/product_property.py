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
        'properties'
    )

    def __init__(self, model):
        super(ProductPropertyTemplate, self).__init__()
        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

    @staticmethod
    @param_required(['id'])
    def from_id(args):
        template = mall_models.ProductPropertyTemplate.select().dj_where(id=args['id']).get()
        template.properties = mall_models.TemplateProperty.select().dj_where(template=template)
        # 使用from_model将数据取回到领域模型
        return ProductPropertyTemplate.from_model(dict(db_model=template)).to_dict()

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
            template.properties = mall_models.TemplateProperty.select().dj_where(template=template)
            # 使用from_model将数据取回到领域模型
            result.append(ProductPropertyTemplate.from_model(dict(db_model=template)).to_dict())
        return result

    @staticmethod
    @param_required([])
    def create(mall_model):
        """
        创造新模板
        """
        # 创造一个属性模板
        template = mall_models.ProductPropertyTemplate.create(owner=mall_model.owner_id,
                                                              name=mall_model.name,
                                                              )

        for template_property in mall_model.properties:
            mall_models.TemplateProperty.create(owner=mall_model.owner_id,
                                                template=template,
                                                name=template_property['name'],
                                                value=template_property['value'])
        return '', 'Success'

    @staticmethod
    @param_required(['template_id', 'title', 'new_properties', 'update_properties', 'deleted_ids', 'owner_id'])
    def save(args):
        """
        更新

        """
        owner_id = args.get('owner_id')
        template_id = args.get('template_id')
        title = args.get('title')
        new_properties = args.get('new_properties')
        update_properties = args.get('update_properties')
        deleted_ids = args.get('deleted_ids')
        mall_models.ProductPropertyTemplate.update(name=title).dj_where(id=template_id).execute()
        for new_property in new_properties:
            mall_models.TemplateProperty.create(template=template_id,
                                                owner=owner_id,
                                                name=new_property.get('name'),
                                                value=new_property.get('value')
                                                )
        for update_property in update_properties:
            mall_models.TemplateProperty.update(name=update_property.get('name'),
                                                value=update_property.get('value'))\
                .dj_where(id=update_property.get('id')).execute()
        # TODO in操作
        # mall_models.TemplateProperty.delete().where(id << deleted_ids)
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
            properties.append(dict(id=pro.id,
                                   name=pro.name,
                                   value=pro.value))
        result['properties'] = properties
        return result
