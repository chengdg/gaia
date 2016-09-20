# -*- coding: utf-8 -*-
import json

from eaglet.core import watchdog

from business import model as business_model
from business.mall.product import Product, ProductModel, ProductSwipeImage, ProductPool
from db.mall import models as mall_models
from settings import PANDA_IMAGE_DOMAIN
from eaglet.decorator import param_required


class A(object):
	pass

class ProductFactory(business_model.Model):
    """
    商品工厂类
    """

    def __init__(self):
        super(ProductFactory, self).__init__()

    @staticmethod
    def get():
        return ProductFactory()

    def create_product(self, owner_id, args):
        # product = Product.empty_product()
        _product = A()

        # try:
        #     product_model = self.__save_db(product, product_data)
        #     product = Product.from_model({"db_model": product_model})
        #     pool = ProductPool.get({'owner_id': owner_id})
        #     pool.push(product)
        # except BaseException as e:
        #     from eaglet.core.exceptionutil import unicode_full_stack
        #     print(unicode_full_stack())

        try:
            self.__init_base_info(_product, args)
            self.__init_models_info(_product, args)
            self.__init_image_info(_product, args)
            self.__init_postage_info(_product, args)
            self.__init_pay_info(_product, args)

            product = Product()
            product.save(_product)

        except BaseException as e:
            from eaglet.core.exceptionutil import unicode_full_stack
            msg = unicode_full_stack()
            print(msg)
            watchdog.alert(msg)


    # def __init_product(self, product, product_data):
    #     product.owner_id = product_data['owner_id']
    #     product.name = product_data.get('name', '').strip()
    #     product.promotion_title = product_data.get('promotion_title', '').strip()
    #
    #     product.price = float(product_data.get('price', '0.0'))
    #     product.user_code = product_data.get('user_code', '').strip()
    #     product.bar_code = product_data.get('bar_code', '').strip()
    #     product.min_limit = int(product_data.get('min_limit', 0))
    #     product.is_member_product = int(product_data.get('is_member_product', '0'))
    #     product.purchase_price = float(product_data.get('purchase_price', '0.0'))
    #     product.supplier = int(product_data.get('supplier', '0'))
    #     product.weight = float(product_data.get('weight', '0.0'))
    #
    #     product.postage_type = product_data.get('postage_type', '')
    #     product.unified_postage_money = float(product_data.get('unified_postage_money', '0.0'))
    #
    #     swipe_images = json.loads(product_data['swipe_images'])
    #
    #     if swipe_images:
    #         product.thumbnails_url = swipe_images[0]["url"]
    #     else:
    #         product.thumbnails_url = ''
    #
    #     product.is_use_cod_pay_interface = int(product_data.get('is_enable_cod_pay_interface', '0'))
    #     product.is_use_online_pay_interface = int(product_data.get('is_use_online_pay_interface', '0'))
    #     product.is_enable_bill = int(product_data.get('is_enable_bill', '0'))
    #     product.is_delivery = int(product_data.get('is_delivery', '0'))
    #     product.detail = product_data.get('detail', '')
    #
    #     return product
    #
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
    #
    # def __init_product_model(self, product_data):
    #     is_use_custom_models = int(product_data.get("is_use_custom_model", ''))
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
    #             model['properties'] = self.__init_custom_model(model['name'])
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
    #     return standard_model, custom_models
    #
    # def __save_product(self, product):
    #
    #     if product.id:
    #         product_model = mall_models.Product.update(owner=product.owner_id,
    #                                    name=product.name,
    #                                    promotion_title=product.promotion_title,
    #                                    introduction=product.introduction,
    #                                    thumbnails_url=product.thumbnails_url,
    #                                    pic_url=product.pic_url,
    #                                    price=product.price,
    #                                    user_code=product.user_code,
    #                                    bar_code=product.bar_code,
    #                                    is_member_product=product.is_member_product,
    #                                    purchase_price=product.purchase_price,
    #                                    supplier=product.supplier,
    #                                    weight=product.weight,
    #                                    stock_type=product.stock_type,
    #                                    stocks=product.min_limit,
    #                                    postage_type=product.postage_type,
    #                                    unified_postage_money=product.unified_postage_money,
    #                                    is_use_cod_pay_interface=product.is_use_cod_pay_interface,
    #                                    is_use_online_pay_interface=product.is_use_online_pay_interface,
    #                                    is_enable_bill=product.is_enable_bill,
    #                                    is_delivery=product.is_delivery,
    #                                    detail=product.detail
    #                                    ).dj_where(id=product.id).execute()
    #         # todo 优化掉
    #         product_model = mall_models.Product.select().dj_where(id=product.id).first()
    #
    #     else:
    #         product_model = mall_models.Product.create(
    #             owner=product.owner_id,
    #             name=product.name,
    #             promotion_title=product.promotion_title,
    #             thumbnails_url=product.thumbnails_url,
    #             price=product.price,
    #             user_code=product.user_code,
    #             bar_code=product.bar_code,
    #             is_member_product=product.is_member_product,
    #             purchase_price=product.purchase_price,
    #             supplier=product.supplier,
    #             weight=product.weight,
    #
    #             stocks=product.min_limit,
    #             postage_type=product.postage_type,
    #             unified_postage_money=product.unified_postage_money,
    #             is_use_cod_pay_interface=product.is_use_cod_pay_interface,
    #             is_use_online_pay_interface=product.is_use_online_pay_interface,
    #             is_enable_bill=product.is_enable_bill,
    #             is_delivery=product.is_delivery,
    #             detail=product.detail
    #         )
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
    #
    # def __save_db(self, product, product_data):
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
    #
    #     # todo 处理缓存
    #     return product_model


    def __init_base_info(self,product,args):
        """
        初始化基本信息
        @param args: 
        @return: 
        """
        base_info = args['base_info']

        product.owner_id = base_info['owner_id']
        product.name = base_info.get('name', '').strip()
        product.promotion_title = base_info.get('promotion_title', '').strip()
        product.bar_code = base_info.get('bar_code', '').strip()
        product.min_limit = int(base_info.get('min_limit', 0))
        product.is_member_product = int(base_info.get('is_member_product', '0'))
        product.detail = base_info['detail']

        product_category_id = base_info.get('product_category', '')

        product.product_category_id = product_category_id.split(',')

    def __init_models_info(self,product,args):
        models_info = args['models_info']

        if models_info['is_use_custom_models']:
            custom_models_info = models_info['custom_model']
            # 多规格商品创建默认标准规格
            
            custom_models = []
            standard_model = {
                "price": 0.0,
                "weight": 0.0,
                "stock_type": mall_models.PRODUCT_STOCK_TYPE_LIMIT,
                "stocks": 0,
                "user_code": '',
                "is_deleted": True
            }
            
            def __init_custom_model(model_name):

                properties = []
                property_infos = model_name.split('_')
                for property_info in property_infos:
                    items = property_info.split(':')
                    properties.append({
                        'property_id': int(items[0]),
                        'property_value_id': int(items[1])
                    })
                return properties
            
            for model in custom_models_info:

                model['properties'] = __init_custom_model(model['name'])
                if model.get('stocks') and int(model.get('stocks')) == -1:
                    model['stocks'] = 0

                custom_models.append({
                    'name': model['name'],
                    'is_standard': False,
                    'price': model['price'],
                    'weight': model['weight'],
                    'stock_type': model['stock_type'],
                    'stocks': model['stocks'],
                    'user_code': model['user_code'],

                })

        else:
            standard_model = {}
            custom_models = {}
        
        
        
        product.standard_model = standard_model
        product.custom_models = custom_models
        
    def __init_image_info(self, product,args):
        image_info = args['image_info']

        product.swipe_images = json.loads(image_info['swipe_images'])


    def __init_postage_info(self,product,args):
        postage_info = args['postage_info']
        product.postage_type = postage_info.get('postage_type', '')
        product.unified_postage_money = float(postage_info.get('unified_postage_money', '0.0'))
        product.is_delivery = int(postage_info.get('is_delivery', '0'))

    def __init_pay_info(self, product, args):
        pay_info = args['pay_info']

        product.is_use_cod_pay_interface = int(pay_info.get('is_enable_cod_pay_interface', '0'))
        product.is_use_online_pay_interface = int(pay_info.get('is_use_online_pay_interface', '0'))
        product.is_enable_bill = int(pay_info.get('is_enable_bill', '0'))




