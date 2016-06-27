# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.product_factory import ProductFactory

class ASyncProduct(api_resource.ApiResource):
    """
    商品
    """
    app = "mall"
    resource = "sync_product"

    @param_required(['owner_ids', 'suppliers'])
    def put(args):
        owner_ids = args['owner_ids'].split('_')
        suppliers = args['suppliers'].split('_')
        args.pop('owner_ids')
        args.pop('suppliers')
        product_infos = []
        for i in range(0, len(owner_ids)):
            product_data = args
            product_data['owner_id'] = owner_ids[i]
            product_data['supplier'] = suppliers[i]
            product_factory = ProductFactory.get()
            product_model = product_factory.create_product(args)
            product_infos.append({'owner_id': product_model.owner_id, 'product_id': product_model.id})
        return product_infos