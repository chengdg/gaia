# -*- coding: utf-8 -*-
import json

from business import model as business_model
from business.mall.product import Product, ProductModel, ProductSwipeImage, ProductPool
from db.mall import models as mall_models


class ProductFactory(business_model.Model):
    """
    商品工厂类
    """
    __slots__ = (
        )

    def __init__(self):
        super(ProductFactory, self).__init__()

    def save(self, args):
        """

        """
        accounts = json.loads(args.get('accounts'))
        name = args.get('name', '')
        supplier = args.get('supplier', '')
        model_type = args.get('model_type', 'single')

        detail = args.get('detail', '')
        # pic_url = args.get('pic_url')
        purchase_price = args.get('purchase_price')
        promotion_title = args.get('promotion_title')
        swipe_images = json.loads(args.get('images'))
        # 0无限
        stock_type = 0 if args.get('stock_type') == 'unbound' else 1

        product = Product(None)
        product.name = name
        product.supplier = supplier
        product.detail = detail
        # product.pic_url = pic_url
        product.model_type = model_type
        product.purchase_price = purchase_price
        product.promotion_title = promotion_title
        product.thumbnails_url = swipe_images[0].get('url')
        product.swipe_images = swipe_images
        # 保存商品规格信息
        if 'single' == model_type:
            product.price = args.get('price', '')

            product.purchase_price = args.get('purchase_price', '')
            product.weight = args.get('weight', '')
            product.stock_type = stock_type
            # product.stocks = args.get('stocks')

        else:
            # 多规格
            # product.models = json.loads(args.get('model_info', ''))
            pass
        new_product = product.save(panda_product_id=args.get('product_id'))
        if model_type == 'single':
            product_model = ProductModel(None)
            product_model.owner_id = new_product.owner_id
            product_model.product_id = new_product.id
            # 非定制规格
            product_model.is_standard = True
            product_model.stock_type = new_product.stock_type
            product_model.stocks = args.get('stocks') if args.get('stocks') else 0
            product_model.price = new_product.price
            product_model.weight = new_product.weight
            new_product_model = product_model.save()
            # 用来设置规格信息

            new_product.models = [new_product_model]

        else:
            # 多个规格（定制）
            pass
        # 处理论播图
        # TODO 处理论播图的大小暂时无法同步（panda)中无此2字段。
        images = [dict(product=new_product.id,
                       url=image.get('url'),
                       width=100,
                       height=100) for image in product.swipe_images]
        # for image in self.swipe_images:

        ProductSwipeImage.save_many({'images': images})
        # 处理商品在哪个自营平台显示
        pool = [dict(woid=account,
                     product_id=new_product.id,
                     status=mall_models.PP_STATUS_ON_POOL) for account in accounts]
        ProductPool.save_many(pool)
        return new_product

    @staticmethod
    def create():
        return ProductFactory()

    # def __init_product(self, product, product_data):
    #     product.owner_id = product_data.get('owner_id', '')
    #     product.name = product_data.get('name', '')
    #     product.promotion_title = product_data.get('promotion_title', '')
    #     product.introduction = product_data.get('introduction', '')
    #     product.pic_url = product_data.get('pic_url', '')
    #     product.thumbnails_url = product_data.get('thumbnails_url', '')
    #     product.price = float(product_data.get('price', '0.0'))
    #     product.user_code = product_data.get('user_code', '')
    #     product.bar_code = product_data.get('bar_code', '')
    #     product.min_limit = int(product_data.get('min_limit', '0'))
    #     product.is_member_product = int(product_data.get('is_member_product', '0'))
    #     product.purchase_price = float(product_data.get('purchase_price', '0.0'))
    #     product.supplier = int(product_data.get('supplier', '0'))
    #     product.weight = float(product_data.get('weight', '0.0'))
    #     product.stock_type = int(product_data.get('stock_type', '0'))
    #     product.stocks = int(product_data.get('stocks', '0'))
    #     product.postage_type = product_data.get('postage_type', '')
    #     product.unified_postage_money = float(product_data.get('unified_postage_money', '0.0'))
    #     product.is_use_cod_pay_interface = int(product_data.get('is_enable_cod_pay_interface', '0'))
    #     product.is_use_online_pay_interface = int(product_data.get('is_use_online_pay_interface', '0'))
    #     product.is_enable_bill = int(product_data.get('is_enable_bill', '0'))
    #     product.is_delivery = int(product_data.get('is_delivery', '0'))
    #     product.detail = product_data.get('detail', '')
    #
    #     return product

    # def __init_custom_model(self, custom_model_str):
    #     properties = []
    #     property_infos = custom_model_str.split('_')
    #     for property_info in property_infos:
    #         items = property_info.split(':')
    #         properties.append({
    #             'property_id': int(items[0]),
    #             'property_value_id': int(items[1])
    #         })
    #     return properties

    # def __init_product_model(self, product_data):
    #     is_use_custom_models = product_data.get("is_use_custom_model", '') == u'true'
    #
    #     custom_model_data = json.loads(product_data.get('customModels', '[]'))
    #     if custom_model_data and is_use_custom_models:
    #         standard_model = {
    #             "price": 0.0,
    #             "weight": 0.0,
    #             "stock_type": mall_models.PRODUCT_STOCK_TYPE_LIMIT,
    #             "stocks": 0,
    #             "user_code": '',
    #             "is_deleted": True
    #         }
    #         custom_models = custom_model_data
    #         for model in custom_models:
    #             odel['properties'] = self.__init_custom_model(model['name'])
    #             if model.get('stocks') and int(model.get('stocks')) == -1:
    #                 model['stocks'] = 0
    #     else:
    #         stock_type = int(product_data.get(
    #             'stock_type',
    #             mall_models.PRODUCT_STOCK_TYPE_UNLIMIT)
    #         )
    #         stocks = product_data.get('stocks')
    #         if stocks and int(stocks) == -1:
    #             stocks = 0
    #         stocks = int(stocks) if stocks else 0
    #         standard_model = {
    #             "price": product_data.get('price', '0.0').strip(),
    #             "weight": product_data.get('weight', '0.0').strip(),
    #             "stock_type": stock_type,
    #             "stocks": stocks,
    #             "user_code": product_data.get('user_code', '').strip(),
    #         }
    #         custom_models = []
    #
    #     return (standard_model, custom_models)

    # def __save_product(self, product):
    #     product_model = mall_models.Product.create(
    #         owner=product.owner_id,
    #         name=product.name,
    #         promotion_title=product.promotion_title,
    #         introduction=product.introduction,
    #         thumbnails_url=product.thumbnails_url,
    #         pic_url=product.pic_url,
    #         price=product.price,
    #         user_code=product.user_code,
    #         bar_code=product.bar_code,
    #         is_member_product=product.is_member_product,
    #         purchase_price=product.purchase_price,
    #         supplier=product.supplier,
    #         weight=product.weight,
    #         stock_type=product.stock_type,
    #         stocks=product.min_limit,
    #         postage_type=product.postage_type,
    #         unified_postage_money=product.unified_postage_money,
    #         is_use_cod_pay_interface=product.is_use_cod_pay_interface,
    #         is_use_online_pay_interface=product.is_use_online_pay_interface,
    #         is_enable_bill=product.is_enable_bill,
    #         is_delivery=product.is_delivery,
    #         detail=product.detail
    #     )
    #     return product_model
    #
    # def __save_product_model(self, standard_model, custom_models, product_model):
    #
    #     mall_models.ProductModel.create(
    #         owner=product_model.owner,
    #         product=product_model.id,
    #         name='standard',
    #         is_standard=True,
    #         price=standard_model['price'],
    #         weight=standard_model['weight'],
    #         stock_type=standard_model['stock_type'],
    #         stocks=standard_model['stocks'],
    #         user_code=standard_model['user_code'],
    #         is_deleted=standard_model.get('is_deleted', False)
    #     )
    #
    #     # 处理custom商品规格
    #     for custom_model in custom_models:
    #         product_model = mall_models.ProductModel.create(
    #             owner=product_model.owner,
    #             product=product_model.id,
    #             name=custom_model['name'],
    #             is_standard=False,
    #             price=custom_model['price'],
    #             weight=custom_model['weight'],
    #             stock_type=custom_model['stock_type'],
    #             stocks=custom_model['stocks'],
    #             user_code=custom_model['user_code']
    #         )
    #
    #         for property in custom_model['properties']:
    #             mall_models.ProductModelHasPropertyValue.create(
    #                 model=product_model,
    #                 property_id=property['property_id'],
    #                 property_value_id=property['property_value_id']
    #             )
    #
    # def __save_product_swipe_image(self, product_model, product_data):
    #     swipe_images = json.loads(product_data.get('swipe_images', '[]'))
    #     if len(swipe_images) == 0:
    #         thumbnails_url = ''
    #     else:
    #         thumbnails_url = swipe_images[0]["url"]
    #
    #     for swipe_image in swipe_images:
    #         if swipe_image['width'] and swipe_image['height']:
    #             mall_models.ProductSwipeImage.create(
    #                 product=product_model,
    #                 url=swipe_image['url'],
    #                 width=swipe_image['width'],
    #                 height=swipe_image['height']
    #             )
    #
    #     product_model.thumbnails_url = thumbnails_url
    #     product_model.save()
    #
    # def __save_product_category(self, product_model, product_data):
    #     product_category_id = product_data.get('product_category', -1)
    #     if product_category_id != -1:
    #         for category_id in product_category_id.split(','):
    #             if not category_id.isdigit():
    #                 continue
    #             cid = int(category_id)
    #             mall_models.CategoryHasProduct.create(
    #                 category=cid,
    #                 product=product_model)
    #
    # def __save_product_property(self, product_model, product_data):
    #     properties = json.loads(product_data.get('properties', '[]'))
    #     for property in properties:
    #         mall_models.ProductProperty.create(
    #             owner=product_model.owner_id,
    #             product=product_model,
    #             name=property['name'],
    #             value=property['value']
    #         )

    # def create_product(self, product_data):
    #     product = Product.empty_product()
    #     # 商品信息
    #     product = self.__init_product(product, product_data)
    #     # 保存商品
    #     product_model = self.__save_product(product)
    #     # 商品规格
    #     standard_model, custom_models = self.__init_product_model(product_data)
    #
    #     self.__save_product_model(standard_model, custom_models, product_model)
    #     # 商品图片
    #     self.__save_product_swipe_image(product_model, product_data)
    #     # 商品分组
    #     self.__save_product_category(product_model, product_data)
    #     # 商品属性
    #     self.__save_product_property(product_model, product_data)
    #     return product_model