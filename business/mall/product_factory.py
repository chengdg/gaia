# -*- coding: utf-8 -*-
import json
from business import model as business_model
from business.mall.product import Product
from db.mall import models as mall_models
from eaglet.decorator import param_required

class ProductFactory(business_model.Model):
    """
    商品工厂类
    """
    __slots__ = (
        )

    @staticmethod
    @param_required([])
    def get(args):
        """
        工厂方法，创建ProductFactory对象
        """
        product_factory = ProductFactory()
        return product_factory

    def __init__(self):
        business_model.Model.__init__(self)

    def __init_product(self, product, product_data):
        product.owner_id = product_data.get('owner_id', '')
        product.name = product_data.get('name', '')
        product.promotion_title = product_data.get('promotion_title', '')
        product.price = product_data.get('price', '')
        product.purchase_price = product_dat.get('purchase_price', '')
        product.supplier = product_data.get('supplier', '')
        product.weight = product_data.get('weight', '')
        product.stock_type = product_data.get('stock_type', '')
        product.stocks = product_data.get('stocks', '')
        product.detail = product_data.get('detail', '')

        return product

    def __init_custom_model(self, custom_model_str):
        properties = []
        property_infos = custom_model_str.split('_')
        for property_info in property_infos:
            items = property_info.split(':')
            properties.append({
                'property_id': int(items[0]),
                'property_value_id': int(items[1])
            })
        return properties

    def __init_product_model(self, product_data):
        is_use_custom_models = product_data.get("is_use_custom_model", '') == u'true'

        custom_model_data = json.loads(product_data.get('customModels', '[]'))
        if custom_model_data and is_use_custom_models:
            standard_model = {
                "price": 0.0,
                "weight": 0.0,
                "stock_type": mall_models.PRODUCT_STOCK_TYPE_LIMIT,
                "stocks": 0,
                "user_code": '',
                "is_deleted": True
            }
            custom_models = custom_model_data
            for model in custom_models:
                odel['properties'] = self.__init_custom_model(model['name'])
                if model.get('stocks') and int(model.get('stocks')) == -1:
                    model['stocks'] = 0
        else:
            stock_type = int(product_data.get(
                'stock_type',
                mall_models.PRODUCT_STOCK_TYPE_UNLIMIT)
            )
            stocks = product_data.get('stocks')
            if stocks and int(stocks) == -1:
                stocks = 0
            stocks = int(stocks) if stocks else 0
            standard_model = {
                "price": product_data.get('price', '0.0').strip(),
                "weight": product_data.get('weight', '0.0').strip(),
                "stock_type": stock_type,
                "stocks": stocks,
                "user_code": product_data.get('user_code', '').strip(),
            }
            custom_models = []

        return (standard_model, custom_models)

    def __save_product(self, product):
        product_model = mall_models.Product.create(
            owner=product.owner_id,
            name=product.name,
            promotion_title=product.promotion_title,
            price=product.price,
            purchase_price=product.purchase_price,
            supplier=product.supplier,
            weight=product.weight,
            stock_type=product.stock_type,
            stocks=product.stocks,
            detail=product.detail
        )
        return product_model

    def __save_product_model(self, standard_model, custom_models, product_model):

        mall_models.ProductModel.create(
            owner=product_model.owner,
            product=product_model.id,
            name='standard',
            is_standard=True,
            price=standard_model['price'],
            weight=standard_model['weight'],
            stock_type=standard_model['stock_type'],
            stocks=standard_model['stocks'],
            user_code=standard_model['user_code'],
            is_deleted=standard_model.get('is_deleted', False)
        )

        # 处理custom商品规格
        for custom_model in custom_models:
            product_model = mall_models.ProductModel.create(
                owner=product_model.owner,
                product=product_model.id,
                name=custom_model['name'],
                is_standard=False,
                price=custom_model['price'],
                weight=custom_model['weight'],
                stock_type=custom_model['stock_type'],
                stocks=custom_model['stocks'],
                user_code=custom_model['user_code']
            )

            for property in custom_model['properties']:
                mall_models.ProductModelHasPropertyValue.create(
                    model=product_model,
                    property_id=property['property_id'],
                    property_value_id=property['property_value_id']
                )

    def __save_product_swipe_image(self, product_model, product_data):
        swipe_images = json.loads(product_data.get('swipe_images', '[]'))
        if len(swipe_images) == 0:
            thumbnails_url = ''
        else:
            thumbnails_url = swipe_images[0]["url"]

        for swipe_image in swipe_images:
            if swipe_image['width'] and swipe_image['height']:
                mall_models.ProductSwipeImage.create(
                    product=product_model,
                    url=swipe_image['url'],
                    width=swipe_image['width'],
                    height=swipe_image['height']
                )

        product_model.thumbnails_url = thumbnails_url
        product_model.save()

    def __save_product_category(self, product_model, product_data):
        product_category_id = product_data.get('product_category', -1)
        if product_category_id != -1:
            for category_id in product_category_id.split(','):
                if not category_id.isdigit():
                    continue
                cid = int(category_id)
                mall_models.CategoryHasProduct.create(
                    category_id=cid,
                    product_id=product_model.id)

    def __save_product_property(self, product_model, product_data):
        properties = json.loads(product_model.get('properties', '[]'))
        for property in properties:
            mall_models.ProductProperty.create(
                owner=request.manager,
                product=product,
                name=property['name'],
                value=property['value']
            )

    def create_product(self, product_data):
        product = Product.empty_product()
        product = self.__init_product(product, product_data)
        product_model = self.__save_product(product)
        standard_model, custom_models = self.__save_product_model(product_model, product_data)
        self.__save_product_model(standard_model, custom_models, product_model)
        self.__save_product_swipe_image(product_model, product_data)
        self.__save_product_category(product_model, product_data)
        self.__save_product_property(product_model, product_data)
        return product_model.to_dict()