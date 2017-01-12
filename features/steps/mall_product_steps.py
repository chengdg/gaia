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
        'is_use_custom_model': False, #是否使用定制规格
        'standard_model': {},
        'custom_models': []
    }
    if 'model' in product:
        for model_name, model in product['model']['models'].items():
            is_unlimit_stock = (model.get('stock_type', u'无限') == u'无限')
            data = {
                "price": model.get('price', 1.0),
                "purchase_price": model.get('purchase_price', 1.0),
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
    else:
        models_info['standard_model'] = {
            "name": "standard",
            "price": 1.0,
            "purchase_price": 1.0,
            "weight": 2.0,
            "stock_type": 'unlimit',
            "stocks": -1,
            "user_code": 'user_code'
        }
    if len(models_info['custom_models']) > 0:
        models_info['is_use_custom_model'] = True

    return models_info


def __format_product_post_data(context, product):
    """
    构造用于提交的product数据
    """
    LIMIT_ZONE_TYPE = {
        u'不限制': 0,
        u'禁售': 1,
        u'仅售': 2
    }
    #基本信息
    if product.get('supplier', None):
        # supplier = mall_models.Supplier.select().dj_where(owner_id=context.corp.id, name=product['supplier']).get()

        supplier = mall_models.Supplier.select().dj_where(name=product['supplier']).get()
        supplier_id = supplier.id
    else:
        supplier_id = 0

    if product.get('classification', None):
        classification = mall_models.Classification.select().dj_where(name=product['classification']).get()
        classification_id = classification.id
    else:
        classification_id = 0

    base_info = {
        'name': product['name'], #商品名
        'type': product.get('type', 'object'),
        'bar_code': product.get('bar_code', 'bar_code_default_value'), #商品条码
        'min_limit': product.get('min_limit', '1'), #起购数量
        'promotion_title': product.get('promotion_title', 'promotion_title_default_value'), #促销标题
        'is_enable_bill': product.get('is_enable_bill', False), #是否使用发票
        'detail': product.get('detail', u'商品的详情'), #详情
        'is_member_product': product.get('is_member_product', False), #是否参与会员折扣
        'supplier_id': supplier_id,
        'classification_id': classification_id
    }

    #规格信息
    models_info = __format_product_models_info(context, product)

    #支付信息
    pay_info = {
        'is_use_online_pay_interface': __get_boolean(product, 'is_use_online_pay_interface', True),
        'is_use_cod_pay_interface': __get_boolean(product, 'is_use_cod_pay_interface')
    }

    #运费信息
    postage_type = 'unified_postage_type' if (product.get('postage_type', u'统一运费') == u'统一运费') else 'custom_postage_type'
    limit_zone_type = LIMIT_ZONE_TYPE[product.get('limit_zone_type', u'不限制')]
    limit_zone_name = product.get('limit_zone_name', u'')
    if limit_zone_name:
        limit_zone_id = mall_models.ProductLimitZoneTemplate.select().dj_where(owner=context.corp.id, name=limit_zone_name).first().id
    else:
        limit_zone_id = 0
    logistics_info = {
        'unified_postage_money': product.get('unified_postage_money', '0.0'), #统一运费金额
        'postage_type': postage_type, #运费类型
        'limit_zone_type': limit_zone_type,
        'limit_zone_id': limit_zone_id
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
        'logistics_info': json.dumps(logistics_info),
        'image_info': json.dumps(image_info),
        'categories': json.dumps(categories),
        'properties': json.dumps(product.get('properties', [])),
    }

    return data

def __create_product(context, product):
    data = __format_product_post_data(context, product)

    response = context.client.put('/product/product/', data)
    bdd_util.assert_api_call_success(response)


def __get_product(context, name):
    LIMIT_ZONE_TYPE_NUMBER2STR = {
        0: u'不限制',
        1: u'禁售',
        2: u'仅售'
    }
    product_model = mall_models.Product.select().dj_where(name=name).get()
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
        "create_type": base_info['create_type'],
        "bar_code": base_info['bar_code'],
        "min_limit": base_info['min_limit'],
        "promotion_title": base_info['promotion_title'],
        "detail": base_info['detail'],
        "is_member_product": base_info['is_member_product'],
        "is_enable_bill": base_info['is_enable_bill'],
        "properties": resp_data['properties'],
        "supplier": resp_data['supplier']['name'] if resp_data['supplier'] else ""
    }

    #处理category
    product['categories'] = [category['name'] for category in resp_data['categories']]

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
                "purchase_price": model['purchase_price'],
                "weight": model['weight'],
                "stock_type": u'无限' if model['stock_type'] == 'unlimit' else u'有限',
                "stocks": model['stocks']
            }
    else:
        model = resp_models_info['standard_model']
        model_name = model['name']
        product['model']['models'][model_name] = {
            "price": model['price'],
            "purchase_price": model['purchase_price'],
            "weight": model['weight'],
            "stock_type": u'无限' if model['stock_type'] == 'unlimit' else u'有限',
            "stocks": model['stocks']
        }

    #处理物流信息
    logistics_info = resp_data['logistics_info']
    product['postage_type'] = u'统一运费' if logistics_info['postage_type'] == 'unified_postage_type' else u'运费模板'
    product['unified_postage_money'] = logistics_info['unified_postage_money']
    product['limit_zone_type'] = LIMIT_ZONE_TYPE_NUMBER2STR[logistics_info['limit_zone_type']]
    product['limit_zone_name'] = mall_models.ProductLimitZoneTemplate.select().dj_where(id=logistics_info['limit_zone_id']).first().name if logistics_info['limit_zone_id'] else ''
    #处理商品分类信息
    if len(resp_data['classifications']) == 0:
        product['classification'] = ''
    else:
        items = []
        for classification in resp_data['classifications']:
            items.append(classification['name'])
        product['classification'] = '-'.join(items)

    return product

def __create_promote(promotes, context, user):
    for promote in promotes:
        product = mall_models.Product.select().dj_where(name=promote.get('product_name')).first()

        if product:

            corp_id = context.corp.id
            data = {
                'corp_id': corp_id,
                'product_id': product.id,
                'money': promote.get('promote_money'),
                'stock': promote.get('promote_stock'),
                'time_from': promote.get('promote_time_from'),
                'time_to': promote.get('promote_time_to'),
            }
            response = context.client.put('/product/cps_promoted_product/', data)
            bdd_util.assert_api_call_success(response)


def __create_consignment_product(product_names, user, context):
    user = mall_models.User.select().dj_where(username=user).first()
    for product_name in product_names:
        product = mall_models.Product.select().dj_where(name=product_name).first()

        if product:

            corp_id = user.id
            data = {
                'corp_id': corp_id,
                'product_id': product.id,

            }
            response = context.client.put('/product/consignment_product/', data)

            bdd_util.assert_api_call_success(response)

def __get_products(context, corp_name, type_name=u'在售'):
    TYPE2URL = {
      u'待售': '/product/offshelf_products/?corp_id=%d' % context.corp.id,
      u'在售': '/product/onshelf_products/?corp_id=%d' % context.corp.id,
      u'same_corp_tmpl': '/product/unshelf_pooled_products/?corp_id=%d',
      u'different_corp_tmpl': '/product/pooled_products/?corp_id=%d',
      u'待销': '/product/unshelf_consignment_products/?corp_id=%d' % context.corp.id,
    }

    if u'商品池' in type_name:
        other_corp_name = type_name[:-3]
        other_corp_id = bdd_util.get_user_id_for(other_corp_name)
        if corp_name == other_corp_name:
            url = TYPE2URL['same_corp_tmpl'] % other_corp_id
        else:
            url = TYPE2URL['different_corp_tmpl'] % other_corp_id
    else:
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
        data['create_type'] = product['create_type']
        data['bar_code'] = product['bar_code']        

        #分类
        if 'categories' in product:
            data['categories'] = ','.join([category['name'] for category in product['categories']])

        #规格
        if 'models_info' in product:
            models_info = product['models_info']
            if not models_info['is_use_custom_model']:
                model = models_info['standard_model']
                data['price'] = model['price']
                data['stocks'] = u'无限' if model['stock_type'] == 'unlimit' else model['stocks']
                data['gross_profit'] = model['price'] - model['purchase_price']
            else:
                price_items = []
                gross_profit_items = []
                for model in models_info['custom_models']:
                    price_items.append(model['price'])
                    gross_profit_items.append(model['price'] - model['purchase_price'])

                price_items.sort()
                gross_profit_items.sort()
                data['price'] = '%.2f~%.2f' % (price_items[0], price_items[-1])
                data['gross_profit'] = '%.2f~%.2f' % (gross_profit_items[0], gross_profit_items[-1])
                data['stocks'] = ""

        data['image'] = product['image']
        data['sales'] = product.get('sales', 0)
        data['display_index'] = product['display_index']

        #供应商
        data['supplier'] = ""
        data['supplier_type'] = ""
        if product['supplier']:
            data["supplier"] = product['supplier']['name']
            supplier_type = product['supplier']['type']
            if supplier_type == 'fixed':
                data['supplier_type'] = u'固定低价'
            elif supplier_type == 'divide':
                divide_info = product['supplier']['divide_type_info']
                data['supplier_type'] = u'首月55分成(%s%%)' % divide_info['basic_rebate']
            elif supplier_type == 'retail':
                data['supplier_type'] = u'零售返点'

        #商品分类信息
        if len(product['classifications']) == 0:
            data['classification'] = ''
        else:
            items = []
            for classification in product['classifications']:
                items.append(classification['name'])
            data['classification'] = '-'.join(items)

        products.append(data)

    return products


def __create_supplier(username):
    owner_id = bdd_util.get_user_id_for(username)
    supplier = mall_models.Supplier.create(
        owner=bdd_util.get_user_id_for(username),
        name=username,
        responsible_person=username,
        supplier_tel='10086',
        supplier_address=u'火星',
        remark='aaaaaa'

    )
    return supplier


def __get_supplier_name(username):
    supplier = mall_models.Supplier.select().dj_where(name=username).first()
    if supplier:
        return supplier.name
    else:
        supplier = __create_supplier(username)
        return supplier.name


@when(u"{user}添加商品")
def step_add_property(context, user):
    products = json.loads(context.text)
    if isinstance(products, dict):
        products = [products]
    for product in products:

        if 'supplier' not in product:
            # 填充默认供货商为自己
            product['supplier'] = __get_supplier_name(user)
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
    actual = __get_products(context, user, type_name)
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

    product['supplier'] = product['supplier'].name if product['supplier'] else None

    update_data = json.loads(context.text)
    for key, value in update_data.items():
        product[key] = value
    data = __format_product_post_data(context, product)
    data['id'] = product['id']

    response = context.client.post('/product/product/', data)
    bdd_util.assert_api_call_success(response)


@when(u"{user}修改商品'{product_name}'的价格为")
def step_impl(context, user, product_name):
    product = mall_models.Product.select().dj_where(owner_id=context.corp.id, name=product_name).get()

    update_data = json.loads(context.text)
    price_infos = []
    for model_name, price in update_data.items():
        if model_name == 'standard':
            pass
        else:
            model_name, _ = __parse_model_name(context, model_name)

        product_model = mall_models.ProductModel.select().dj_where(owner_id=context.corp.id, product_id=product.id, name=model_name).get()

        price_infos.append({
            "model_id": product_model.id,
            "price": price
        })

    data = {
        "corp_id": context.corp.id,
        "id": product.id,
        "price_infos": json.dumps(price_infos)
    }

    response = context.client.post('/product/product_price/', data)
    bdd_util.assert_api_call_success(response)


@when(u"{user}修改商品'{product_name}'的库存为")
def step_impl(context, user, product_name):
    product = mall_models.Product.select().dj_where(owner_id=context.corp.id, name=product_name).get()

    update_data = json.loads(context.text)
    stock_infos = []
    for model_name, stock_info in update_data.items():
        if model_name == 'standard':
            pass
        else:
            model_name, _ = __parse_model_name(context, model_name)

        product_model = mall_models.ProductModel.select().dj_where(owner_id=context.corp.id, product_id=product.id, name=model_name).get()

        stock_type = stock_info['stock_type']
        stock_infos.append({
            "model_id": product_model.id,
            "stock_type": 'unlimit' if stock_type == u'无限' else 'limit',
            "stocks": -1 if stock_type == u'无限' else stock_info['stocks']
        })

    data = {
        "corp_id": context.corp.id,
        "id": product.id,
        "stock_infos": json.dumps(stock_infos)
    }

    response = context.client.post('/product/product_stock/', data)
    bdd_util.assert_api_call_success(response)


@when(u"{user}修改商品'{product_name}'的显示排序为'{position}'")
def step_impl(context, user, product_name, position):
    db_product = mall_models.Product.select().dj_where(owner_id=context.corp.id, name=product_name).get()

    data = {
        "corp_id": context.corp.id,
        "id": db_product.id,
        "position": position
    }

    response = context.client.post('/product/product_position/', data)
    bdd_util.assert_api_call_success(response)


@when(u"{user}添加代售商品")
def step_impl(context, user):
    products = json.loads(context.text)
    for product in products:
        db_product = mall_models.Product.select().dj_where(name=product['name']).get()

        data = {
            "corp_id": context.corp.id,
            "product_id": db_product.id
        }

        response = context.client.put('/product/consignment_product/', data)
        bdd_util.assert_api_call_success(response)

@when(u"{user}将商品加入CPS推广")
def step_impl(context, user):

    promotes = json.loads(context.text)
    if isinstance(promotes, dict):
        promotes = [promotes]

    __create_promote(promotes, context, user)


@when(u"{user}添加代销商品")
def step_impl(context, user):

    product_names = json.loads(context.text)

    for product_name in product_names:
        db_product = mall_models.Product.select().dj_where(name=product_name).get()

        data = {
            "corp_id": context.corp.id,
            "product_id": db_product.id
        }

        response = context.client.put('/product/consignment_product/', data)
        bdd_util.assert_api_call_success(response)


@when(u"{user}将商品移动到'{shelf_name}'货架")
def step_impl(context, user, shelf_name):
    product_names = json.loads(context.text)
    product_ids = []
    for product_name in product_names:
        db_product = mall_models.Product.select().dj_where(name=product_name).get()
        product_ids.append(db_product.id)

    if shelf_name == u'在售':
        data = {
            'corp_id': context.corp.id,
            'product_ids': json.dumps(product_ids)
        }

        response = context.client.put('/product/onshelf_products/', data)
        bdd_util.assert_api_call_success(response)
    elif shelf_name == u'待售':
        data = {
            'corp_id': context.corp.id,
            'product_ids': json.dumps(product_ids)
        }

        response = context.client.put('/product/offshelf_products/', data)
        bdd_util.assert_api_call_success(response)


@when(u"{user}从商品池删除商品")
def step_impl(context, user):
    product_names = json.loads(context.text)
    product_ids = []
    for product_name in product_names:
        db_product = mall_models.Product.select().dj_where(name=product_name).get()
        product_ids.append(db_product.id)

    data = {
        'corp_id': context.corp.id,
        'product_ids': json.dumps(product_ids)
    }

    response = context.client.put('/product/deleted_products/', data)
    bdd_util.assert_api_call_success(response)


@when(u"{user}从货架删除商品")
def step_impl(context, user):
    product_names = json.loads(context.text)
    product_ids = []
    for product_name in product_names:
        db_product = mall_models.Product.select().dj_where(name=product_name).get()
        product_ids.append(db_product.id)

    data = {
        'corp_id': context.corp.id,
        'product_ids': json.dumps(product_ids)
    }

    response = context.client.put('/product/unshelf_pooled_products/', data)
    bdd_util.assert_api_call_success(response)


@when(u"{user}可以获得代销商品列表")
def step_impl(context, user):

    promotes = json.loads(context.text)
    if isinstance(promotes, dict):
        promotes = [promotes]

    __create_promote(promotes, context, user)