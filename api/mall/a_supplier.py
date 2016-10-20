# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.supplier.supplier import Supplier


class ASupplier(api_resource.ApiResource):
    """
    供货商的信息
    """
    app = "mall"
    resource = "supplier"

    @param_required(['corp_id', 'name', 'responsible_person', 'supplier_tel', 'supplier_address'])
    def put(args):
        name = args['name']
        responsible_person = args['responsible_person']
        supplier_tel = args['supplier_tel']
        supplier_address = args['supplier_address']
        remark = args.get('remark', '')
        type = args.get('type', 'normal')
        settlement_period = args.get('settlement_period', 'month')
        divide_info = json.loads(args['divide_info']) if 'divide_info' in args else None
        retail_info = json.loads(args['retail_info']) if 'retail_info' in args else None

        supplier = Supplier.create({
            'name': name,
            'type': type,
            'settlement_period': settlement_period,
            'supplier_tel': supplier_tel,
            'supplier_address': supplier_address,
            'responsible_person': responsible_person,
            'remark': remark,
            'divide_info': divide_info,
            'retail_info': retail_info
        })

        return {
            'id': supplier.id
        }

    @param_required(['corp_id', 'id'])
    def delete(args):
        corp = args['corp']
        corp.supplier_repository.delete_supplier(args['id'])

        return {}
        
   