# -*- coding: utf-8 -*-
import json
from business import model as business_model
from eaglet.decorator import param_required

from business.mall.supplier import Supplier

class SupplierFactory(business_model.Model):
    """
    供货商工厂类
    """

    __slots__ = ()

    @staticmethod
    def create():
        """
        工厂方法，创建SupplierFactory对象
        """

        return SupplierFactory()

    def __init__(self):
        super(SupplierFactory, self).__init__()

    @staticmethod
    @param_required(['owner_id', 'name', 'responsible_person', 'supplier_tel', 'supplier_address', 'remark'])
    def save(args):
        """
        保存信息
        """
        supplier = Supplier(None)
        supplier.owner_id = args.get('owner_id')
        supplier.name = args.get('name')
        supplier.responsible_person = args.get('responsible_person')
        supplier.supplier_tel = args.get('supplier_tel')
        supplier.supplier_address = args.get('supplier_address')
        supplier.remark = args.get('remark')
        new_obj = supplier.save()
        return new_obj
