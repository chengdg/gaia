# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.supplier import Supplier
from business.mall.supplier_factory import SupplierFactory
from business.account.user_profile import UserProfile


class ASupplier(api_resource.ApiResource):
    """
    供货商的信息
    """
    app = "mall"
    resource = "supplier"

    @param_required(['name', 'responsible_person', 'supplier_tel', 'supplier_address'])
    def put(args):
        user_profile = UserProfile.from_webapp_type({'webapp_type': 2})
        if not user_profile:
            return None
        owner_id = user_profile[0].user_id
        name = args['name']
        responsible_person = args['responsible_person']
        supplier_tel = args['supplier_tel']
        supplier_address = args['supplier_address']
        remark = args.get('remark', '')

        factory = SupplierFactory.create()
        supplier = factory.save({'owner_id': owner_id,
                                 'name': name,
                                 'responsible_person': responsible_person,
                                 'supplier_tel': supplier_tel,
                                 'supplier_address': supplier_address,
                                 'remark': remark
                                 })
        return supplier.to_dict()

    @param_required(['supplier_id', 'name'])
    def post(self):
        """

        """
        supplier_id = self.get('supplier_id')

        name = self.get('name')
        supplier_tel = self.get('supplier_tel', '')
        supplier_address = self.get('supplier_address', '')
        remark = self.get('remark', '')
        supplier = Supplier.from_id({'id': supplier_id})
        supplier.name = name
        supplier.supplier_tel = supplier_tel
        supplier.remark = remark
        supplier.supplier_address = supplier_address
        try:
            change_rows = supplier.update()
            return {
                'change_rows': change_rows
            }
        except:
            msg = unicode_full_stack
            watchdog.error(msg)
            return {
                'change_rows': -1
            }


