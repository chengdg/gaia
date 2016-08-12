# -*- coding: utf-8 -*-


from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.product import Product
from business.mall.product_factory import ProductFactory

class AProduct(api_resource.ApiResource):
    """
    商品
    """
    app = "product"
    resource = "product"

    @param_required([])
    def put(args):
        """
        创建商品
        @return:
        """
        product_factory = ProductFactory.get()
        owner_id = args['owner_id']
        product_factory.create_product(owner_id, args)
        return {}

    @param_required([])
    def post(args):
        product_factory = ProductFactory.create()
        product_factory.update_product(args['id'], args)

        return {}

    @param_required(['ids'])
    def delete(args):

        pids= args['ids'].split(',')

    @param_required(['product_id', 'owner_id'])
    def get(args):
        product = Product.get_from_id({"product_id": args['product_id'], 'owner_id': args['owner_id']})

        if product:
            return product.to_dict()
        else:
            return 500, {}

