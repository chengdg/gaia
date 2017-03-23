# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required


class ASuppliers(api_resource.ApiResource):
    """
    供货商集合
    """
    app = "mall"
    resource = "suppliers"

    @param_required(['corp_id'])
    def get(args):
        corp = args['corp']
        suppliers = corp.supplier_repository.get_suppliers()

        datas = []
        for supplier in suppliers:
            data = {
                'id': supplier.id,
                'name': supplier.name,
                'type': supplier.type,
                'responsible_person': supplier.responsible_person,
                'supplier_tel': supplier.supplier_tel,
                'supplier_address': supplier.supplier_address,
                'remark': supplier.remark,
                'settlement_period': supplier.settlement_period,
                'divide_type_info': None,
                'retail_type_info': None
            }

            if supplier.is_retail_type():
                retail_info = supplier.get_retail_info()
                data['retail_type_info'] = {
                    "id": retail_info.id,
                    "rebate": retail_info.rebate
                }

            datas.append(data)

        return {
            'suppliers': datas
        }