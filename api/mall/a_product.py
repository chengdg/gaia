# -*- coding: utf-8 -*-

import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.product_factory import ProductFactory
from business.mall.product import Product, ProductModel, ProductSwipeImage, ProductPool
from settings import PANDA_IMAGE_DOMAIN


class AProduct(api_resource.ApiResource):
    """
    商品
    """
    app = "mall"
    resource = "product"

    @param_required(['name', 'supplier', 'model_type', 'stock_type',
                     'images', 'product_id', 'purchase_price', 'accounts'])
    def put(self):
        """
        同步商品（添加商品）
        product_id -- panda系统商品的id
        name -- 商品名称
        supplier -- 供货商id（同步过来的供货商id）
        model_type -- 规格类型 single： 默认单规格,
                        ;custom: 定制规格（此时必须传递规格信息参数）
        stock_type -- 库存类型limit:有限(1) unbound: 无限(0)
        images -- 商品路播图[{order:1, url: url}]
        purchase_price -- 进价
        accounts -- 要同步到哪个平台

        --------------非必须------------------
        stocks -- 库存数量
        detail -- 商品详情
        price -- 价格（单品）
        weight -- 重量（单品）
        model_info -- 规格信息
        promotion_title -- 促销信息
        """
        #
        factory = ProductFactory.create()
        try:
            product = factory.save(args=self)
            return {
                'product': product.to_dict(),
                'models': product.models

            }
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return {
                'product': None
            }

    @param_required(['product_id', 'model_type'])
    def post(self):
        """
        更新同步的商品（添加商品）
        product_id -- Weapp系统商品的id
        model_type -- 规格类型 single： 默认单规格,
                        ;custom: 定制规格（此时必须传递规格信息参数）
        --------------非必须------------------
        name -- 商品名称
        supplier -- 供货商id（同步过来的供货商id）

        stock_type -- 库存类型limit:有限(1) unbound: 无限(0)
        swipe_images -- 商品路播图[{order:1, url: url}]
        purchase_price -- 进价
        accounts -- 要同步到哪个平台

        stocks -- 库存数量
        detail -- 商品详情
        price -- 价格（单品）
        weight -- 重量（单品）
        model_info -- 规格信息
        """
        #
        product_id = self.get('product_id')
        name = self.get('name', '')
        supplier = self.get('supplier', None)
        model_type = self.get('model_type')
        stock_type = self.get('stock_type', None)
        if stock_type:
            stock_type = 0 if stock_type == 'unbound' else 1
        swipe_images = self.get('swipe_images', None)
        purchase_price = self.get('purchase_price', None)
        stocks = self.get('stocks', None)
        accounts = self.get('accounts', None)
        detail = self.get('detail', '')
        price = self.get('price', purchase_price)
        weight = self.get('weight', 0)
        promotion_title = self.get('promotion_title', '')

        product = Product.from_id({'product_id': product_id})
        product.name = name if name else product.name
        product.supplier = supplier if supplier else product.supplier
        if stock_type is not None:
            product.stock_type = stock_type
        # product.swipe_images = swipe_images if swipe_images else product.swipe_images
        product.purchase_price = purchase_price if purchase_price else product.purchase_price
        product.stocks = stocks if stocks else product.stocks
        product.detail = detail if detail else product.detail
        product.price = price if price else product.price
        product.weight = weight if weight else product.weight
        product.promotion_title = promotion_title if promotion_title else product.promotion_title

        if swipe_images:
            swipe_images = json.loads(swipe_images)
            thumbnails_url = swipe_images[0].get('url')
            if not thumbnails_url.startswith('http'):
                thumbnails_url = PANDA_IMAGE_DOMAIN + thumbnails_url
            product.thumbnails_url = thumbnails_url
            # product.thumbnails_url = swipe_images[0].get('url')

        product.update()
        # 更新规格
        many_models = []
        models_info = self.get('model_info', '')
        if model_type == 'single':
            # 创建标准规格
            stand_product_model = ProductModel(None)
            stand_product_model.owner_id = product.owner_id
            stand_product_model.product_id = product.id
            stand_product_model.is_standard = True
            stand_product_model.stock_type = product.stock_type
            stand_product_model.stocks = stocks if stocks else product.stocks
            stand_product_model.price = product.price
            stand_product_model.weight = product.weight
            stand_product_model.purchase_price = product.purchase_price
            stand_product_model.name = 'standard'
            stand_product_model.is_deleted = False
            many_models.append(stand_product_model)
        can_not_update = False
        if models_info:
            models_info = json.loads(models_info)

            for model_info in models_info:
                # 多规格
                name = model_info.get('name')
                if not name or name == 'standard':
                    can_not_update = True
                purchase_price = model_info.get('purchase_price', 0)
                price = model_info.get('price', 0)
                stock_type = 0 if model_info.get('stock_type') == 'unbound' else 1
                stocks = model_info.get('stocks') if model_info.get('stocks') else 0
                weight = model_info.get('weight')
                product_model = ProductModel(None)
                product_model.owner_id = product.owner_id
                product_model.product_id = product.id
                product_model.name = name
                product_model.purchase_price = purchase_price
                product_model.stock_type = stock_type
                product_model.stocks = stocks
                product_model.weight = weight
                product_model.price = price
                product_model.is_standard = False
                product_model.is_deleted = model_info.get('is_deleted')
                many_models.append(product_model)
        if can_not_update:
            return {
                'success': False
            }
        try:
            ProductModel.update_many_models({'models': many_models,
                                             'product_id': product.id,
                                             })
            if swipe_images:
                # 论播图
                ProductSwipeImage.update_product_many({'swipe_images': swipe_images,
                                                       'product_id': product.id})
            # 商品关联关系更新 主要是，可能更新的商家变化
            if accounts:
                accounts = json.loads(accounts)
                ProductPool.update_many({'product_id': product.id,
                                         'accounts': accounts})
            return {
                'success': True
            }
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return {
                'success': False
            }

    @param_required(['weapp_product_id'])
    def delete(self):
        """
        商品同步删除
        weapp_product_id -- 云商通的商品id
        """
        product_id = self['weapp_product_id']
        product = Product.from_id({'product_id': product_id})
        try:
            change_rows = product.delete()
            return {
                'change_rows': change_rows
            }
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return {
                'change_rows': -1
            }

