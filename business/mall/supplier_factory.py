# -*- coding: utf-8 -*-
import json
from business import model as business_model
from db.mall import models as mall_models
from eaglet.decorator import param_required

class SupplierFactory(business_model.Model):
    """
    供货商工厂类
    """

    __slots__ = ()

    @staticmethod
    @param_required(['owner_id', 'name', 'responsible_person', 'supplier_tel', 'supplier_address', 'remark'])
    def create(args):
        """
        工厂方法，创建SupplierFactory对象
        """

        supplier_factory = SupplierFactory(
                            args['owner_id'],
                            args['name'],
                            args['responsible_person'],
                            args['supplier_tel'],
                            args['supplier_address'],
                            args['remark']
                            )
        return supplier_factory

    def __init__(self, owner_id, name, responsible_person, supplier_tel, supplier_address, remark):
        business_model.Model.__init__(self)

        self.context['owner_id'] = owner_id
        self.context['name'] = name
        self.context['responsible_person'] = responsible_person
        self.context['supplier_tel'] = supplier_tel
        self.context['supplier_address'] = supplier_address
        self.context['remark'] = remark

    def save(self):
        """
        保存信息
        """
        supplier, created = mall_models.Supplier.get_or_create(
                owner=self.context['owner_id'],
                name=self.context['name'],
                responsible_person=self.context['responsible_person'],
                supplier_tel=self.context['supplier_tel'],
                supplier_address=self.context['supplier_address'],
                remark=self.context['remark']
            )
        return supplier.to_dict()