# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from business.mall.supplier import Supplier
from business.account.user_profile import UserProfile

class ASupplierName(api_resource.ApiResource):
    """
    供货商名称
    """
    app = "mall"
    resource = "supplier_name"

    @param_required(['supplier_ids', 'supplier_user_ids'])
    def get(args):
        supplier_ids = args['supplier_ids'].split('_')
        supplier_user_ids = args['supplier_user_ids'].split('_')

        id2supplier_name = {}
        user_id2store_name = {}
        if supplier_ids:
            id2supplier_name = Supplier.get_id_2_supplier_name({'ids': supplier_ids})
        if supplier_user_ids:
            user_id2store_name = UserProfile.get_user_id_2_store_name({'user_ids': supplier_user_ids})

        return {
            'id2supplier_name': id2supplier_name,
            'user_id2store_name': user_id2store_name
        }