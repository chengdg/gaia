# -*- coding: utf-8 -*-
import json

from behave import *
from features.util import bdd_util
from db.mall import models as mall_models
from db.account import models as account_models

def __get_boolean(product, field, default=False):
    return 'true' if product.get(field, default) == True else 'false'


def __parse_model_name(context, model_name):
    """
    解析model name（黑色 M），生成
    1. 标准model_name: 2:5_3:6
    2. model properties: [{property_id:2, property_value_id:5}, {property_id:3, property_value_id:6}]
    """
    properties = list(mall_models.ProductModelProperty.select().dj_where(owner_id=context.corp.id))
    property_ids = [property.id for property in properties]
    property_values = list(mall_models.ProductModelPropertyValue.select().dj_where(property_id__in=property_ids))

    name2value = {}
    for property_value in property_values:
        name = property_value.name
        name2value[name] = property_value

    #从显示用的model_name(黑色 M)构造标准model_name(2:5_3:6)
    normalized_model_name_items = []
    #从model_name(黑色 M)获得model properties
    model_properties = []
    for property_value_name in model_name.split(' '):
        #property_value_name: '黒'' 或是 'M'
        property_value = name2value[property_value_name]
        normalized_model_name_item = '%d:%d' % (property_value.property_id, property_value.id)
        normalized_model_name_items.append(normalized_model_name_item)
        model_properties.append({
            'property_id': property_value.property_id,
            'property_value_id': property_value.id
        })
    normalized_model_name = '_'.join(normalized_model_name_items)

    return normalized_model_name, model_properties


def __format_product_models_info(context, product):
    #规格信息
    models_info = {
        'is_use_custom_model': 'false', #是否使用定制规格
        'standard_model': {},
        'custom_models': []
    }
    for model_name, model in product['model']['models'].items():
        is_unlimit_stock = (model.get('stock_type', u'无限') == u'无限')
        data = {
            "price": model.get('price', 1.0),
            "weight": model.get('weight', 2.0),
            "stock_type": 'unlimit' if is_unlimit_stock else 'limit',
            "stocks": -1 if is_unlimit_stock else model.get('stocks', 10),
            "user_code": model.get('user_code', 'user_code_%s' % model_name)
        }
        if model_name == 'standard':
            data['name'] = 'standard'
            models_info['standard_model'] = data
        else:
            normalized_model_name, model_properties = __parse_model_name(context, model_name)
            data['name'] = normalized_model_name
            data['properties'] = model_properties

            #在数据库中查询是否已存在该model，如果存在，则是更新；否则，为创建
            try:
                existed_product_model = mall_models.ProductModel.select().dj_where(owner_id=context.corp.id, name=normalized_model_name, is_deleted=False).get()
            except:
                existed_product_model = None
            if existed_product_model:
                data['id'] = existed_product_model.id
            else:
                data['id'] = normalized_model_name

            models_info['custom_models'].append(data)
    if len(models_info['custom_models']) > 0:
        models_info['is_use_custom_model'] = 'true'

    return models_info


def __format_product_post_data(context, product):
    """
    构造用于提交的product数据
    """
    #基本信息
    base_info = {
        'name': product['name'], #商品名
        'type': product.get('type', 'object'),
        'bar_code': product.get('bar_code', 'bar_code_default_value'), #商品条码
        'min_limit': product.get('min_limit', '1'), #起购数量
        'promotion_title': product.get('promotion_title', 'promotion_title_default_value'), #促销标题
        'is_enable_bill': __get_boolean(product, 'is_enable_bill'), #是否使用发票
        'detail': product.get('detail', u'商品的详情'), #详情
        'is_member_product': __get_boolean(product, 'is_member_product'), #是否参与会员折扣
    }

    #规格信息
    models_info = __format_product_models_info(context, product)

    #支付信息
    pay_info = {
        'is_use_online_pay_interface': __get_boolean(product, 'is_use_online_pay_interface', True),
        'is_use_cod_pay_interface': __get_boolean(product, 'is_use_cod_pay_interface')
    }

    #运费信息
    postage_type = 'unified_postage_type' if (product.get('postage', u'统一运费') == u'统一运费') else 'custom_postage_type'
    postage_info = {
        'unified_postage_money': product.get('unified_postage_money', '0.0'), #统一运费金额
        'postage_type': postage_type, #运费类型
    }

    #图片信息
    image_info = {
        'images': product.get('swipe_images', []),
        'thumbnails_url': ''
    }
    if len(image_info['images']) > 0:
        image_info['thumbnails_url'] = image_info['images'][0]['url']
    for image in image_info['images']:
        image['width'] = 100
        image['height'] = 100

    #分组信息
    categories = []
    category_names = product.get('categories', None)
    if category_names:
        category_names = category_names.split(',')
        for category_name in category_names:
            db_category = mall_models.ProductCategory.select().dj_where(
                owner_id = context.corp.id, 
                name = category_name
            ).get()
            categories.append(db_category.id)

    data = {
        'corp_id': context.corp.id,
        'base_info': json.dumps(base_info),
        'models_info': json.dumps(models_info),
        'pay_info': json.dumps(pay_info),
        'postage_info': json.dumps(postage_info),
        'image_info': json.dumps(image_info),
        #分组
        'categories': json.dumps(categories),
        #属性
        'properties': product.get('properties', '[]'),        
    }

    return data

def __create_product(context, product):
    data = __format_product_post_data(context, product)

    response = context.client.put('/product/product/', data)
    bdd_util.assert_api_call_success(response)


def __get_product(context, name):
    product_model = mall_models.Product.select().dj_where(owner_id=context.corp.id, name=name).get()
    data = {
        "corp_id": context.corp.id,
        "id": product_model.id
    }

    response = context.client.get('/product/product/', data)
    bdd_util.assert_api_call_success(response)

    resp_data = response.data
    base_info = resp_data['base_info']
    product = {
        "id": resp_data['id'],
        "name": base_info['name'],
        "bar_code": base_info['bar_code'],
        "min_limit": base_info['min_limit'],
        "promotion_title": base_info['promotion_title'],
        "detail": base_info['detail']
    }

    #处理category
    categories = [category['name'] for category in resp_data['categories']]
    product['categories'] = u','.join(categories)

    #处理图片信息
    image_info = resp_data['image_info']
    product['swipe_images'] = image_info['images']
    product['thumbnails_url'] = image_info['thumbnails_url']

    #处理规格信息
    product['model'] = {
        'models': {}
    }
    resp_models_info = resp_data['models_info']
    product['is_use_custom_model'] = u'是' if resp_models_info['is_use_custom_model'] else u'否'
    if resp_models_info['is_use_custom_model']:
        for model in resp_models_info['custom_models']:
            model_name_items = []
            for property_value in model['property_values']:
                model_name_items.append(property_value['name'])
            model_name = ' '.join(model_name_items)
            product['model']['models'][model_name] = {
                "price": model['price'],
                "weight": model['weight'],
                "stock_type": u'无限' if model['stock_type'] == 'unlimit' else u'有限',
                "stocks": model['stocks']
            }
    else:
        model = resp_models_info['standard_model']
        model_name = model['name']
        product['model']['models'][model_name] = {
            "price": model['price'],
            "weight": model['weight'],
            "stock_type": u'无限' if model['stock_type'] == 'unlimit' else u'有限',
            "stocks": model['stocks']
        }

    return product


def __get_products(context, type_name=u'在售'):
    TYPE2URL = {
      u'待售': '/product/offshelf_products/?corp_id=%d' % context.corp.id,
      u'在售': '/product/onshelf_products/?corp_id=%d' % context.corp.id
    }
    url = TYPE2URL[type_name]
    response = context.client.get(url)
    bdd_util.assert_api_call_success(response)
    
    # if hasattr(context, 'query_param'):
    #     for key in context.query_param.keys():
    #         url += '&%s=%s' % (key, context.query_param[key])

    products = []
    for product in response.data["products"]:
        data = {}
        data['name'] = product['name']
        data['bar_code'] = product['bar_code']
        data['price'] = product['price']
        data['categories'] = ','.join([category['name'] for category in product['categories']])
        data['stocks'] = u'无限' if product['stock_type'] == 'unlimit' else product['stocks']
        data['image'] = product['image']
        data['sales'] = product['sales']
        products.append(data)

    return products


@when(u"{user}添加商品")
def step_add_property(context, user):
    products = json.loads(context.text)
    for product in products:
        __create_product(context, product)


@given(u"{user}已添加商品")
def step_add_property(context, user):
    products = json.loads(context.text)
    for product in products:
        __create_product(context, product)


@then(u"{user}能获取商品'{product_name}'")
def step_add_property(context, user, product_name):
    expected = json.loads(context.text)

    actual = __get_product(context, product_name)

    bdd_util.assert_dict(expected, actual)


@then(u"{user}能获得'{type_name}'商品列表")
def step_impl(context, user, type_name):
    actual = __get_products(context, type_name)
    context.products = actual

    if hasattr(context, 'caller_step_text'):
        expected = json.loads(context.caller_step_text)
        delattr(context, 'caller_step_text')
    else:
        if context.table:
            expected = []
            for product in context.table:
                product = product.as_dict()
                if 'barCode' in product:
                    product['bar_code'] = product['barCode']
                    del product['barCode']
                product['categories'] = product['categories'].split(',')
                # 处理空字符串分割问题
                if product['categories'][0] == '':
                    product['categories'] = []
                # 处理table中没有验证库存的行
                if 'stocks' in product and product['stocks'] == '':
                    del product['stocks']
                # 处理table中没有验证条码的行
                if 'bar_code' in product and product['bar_code'] == '':
                    del product['bar_code']
                expected.append(product)
        else:
            expected = json.loads(context.text)

    bdd_util.assert_list(expected, actual)


@when(u"{user}更新商品'{product_name}'")
def step_impl(context, user, product_name):
    product = __get_product(context, product_name)

    update_data = json.loads(context.text)
    for key, value in update_data.items():
        product[key] = value
    data = __format_product_post_data(context, product)
    data['id'] = product['id']

    response = context.client.post('/product/product/', data)
    bdd_util.assert_api_call_success(response)