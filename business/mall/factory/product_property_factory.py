# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from eaglet.core import watchdog

from business import model as business_model
from db.mall import models as mall_models
from eaglet.core.exceptionutil import unicode_full_stack


class ProductPropertyFactory(business_model.Model):
    """
    商品属性模板工厂类
    """
    def __init__(self, model):
        super(ProductPropertyFactory, self).__init__()
        if model:
            self._init_slot_from_model(model)

    @staticmethod
    def create(mall_model):
        """
        创造新模板
        """
        # 创造一个属性模板
        try:
            template = mall_models.ProductPropertyTemplate.create(owner=mall_model.owner_id,
                                                                  name=mall_model.name,
                                                                  )
            ProductPropertyFactory.bulk_create_template_property({'properties': mall_model.properties,
                                                                  'template_id': template.id,
                                                                  'owner_id': mall_model.owner_id})
            return 'SUCCESS', ''
        except:
            msg = unicode_full_stack()
            watchdog.alert(msg)
            return 'Failed', ''

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
            mall_models.TemplateProperty.insert_many(data_resource).execute()

        return True

    @staticmethod
    @param_required(['template_id', 'title', 'new_properties', 'update_properties', 'deleted_ids', 'owner_id'])
    def save(args):
        """
        更新

        """
        owner_id = args['owner_id']
        template_id = args.get('template_id')
        title = args.get('title')
        new_properties = args.get('new_properties')
        update_properties = args.get('update_properties')
        deleted_ids = args.get('deleted_ids')
        try:
            mall_models.ProductPropertyTemplate.update(name=title).dj_where(id=template_id).execute()
            #
            if new_properties:
                ProductPropertyFactory.bulk_create_template_property(dict(properties=new_properties,
                                                                          template_id=template_id,
                                                                          owner_id=owner_id, ))
            if update_properties:
                for update_property in update_properties:
                    mall_models.TemplateProperty.update(name=update_property.get('name'),
                                                        value=update_property.get('value')) \
                        .dj_where(id=update_property.get('id')).execute()
            #
            if deleted_ids:
                mall_models.TemplateProperty.delete().dj_where(id__in=deleted_ids).execute()
            return 'SUCCESS', ''
        except:
            msg = unicode_full_stack()
            print msg
            watchdog.error(msg)
            return 'FAILED', ''

    @staticmethod
    @param_required(['id'])
    def delete_from_id(args):
        """
        删除商品属性模板
        """
        template_id = args.get('id')
        try:
            mall_models.TemplateProperty.delete().dj_where(template=template_id).execute()
            mall_models.ProductPropertyTemplate.delete().dj_where(id=template_id).execute()
            return 'SUCCESS', ''
        except:
            msg = unicode_full_stack()
            watchdog.alert(msg)
            return 'FAILED', ''
