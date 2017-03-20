# -*- coding: utf-8 -*-
import json
from datetime import datetime

from behave import *
from features.util import bdd_util
from db.mall import models as mall_models
from db.account import models as account_models


BUY_PRODUCT_CMD = u"""
When %s购买%s的商品::apiserver
    \"\"\"
    %s
    \"\"\"
"""


def __buy_product_in_apiserver(corp_name, purchase_info, context):
    webapp_user_name = purchase_info['consumer']
    # if webapp_user_name[0] == u'-':
    #     webapp_user_name = webapp_user_name[1:]
    #     #先关注再取消关注，模拟非会员购买  duhao  20160407
    #     context.execute_steps(u"When %s关注%s的公众号" % (webapp_user_name, webapp_owner_name))
    #     context.execute_steps(u"When %s取消关注%s的公众号" % (webapp_user_name, webapp_owner_name))
    #     openid = "%s_%s" %(webapp_user_name, webapp_owner_name)
    #     soucial_account_id = SocialAccount.objects.get(openid=openid).id
    #     member_id = MemberHasSocialAccount.objects.get(account_id=soucial_account_id).member_id
    #     Member.objects.filter(id=member_id).update(status=2)

    #     #clear last member's info in cookie and context
    #     context.execute_steps(u"When 清空浏览器")
    # else:
    #     context.execute_steps(u"When 清空浏览器")
    #     context.execute_steps(u"When %s访问%s的webapp" % (webapp_user_name, webapp_owner_name))
    context.execute_steps(u"When %s访问%s的webapp::apiserver" % (webapp_user_name, corp_name))

    #获得商品信息
    #product格式为: ${product_name},${model},${count}，比如'东坡肘子,大份,3'，其中model为可选
    product_infos = purchase_info['product'].strip().split(',')
    model = None
    if len(product_infos) == 2:
        product, count = product_infos
    elif len(product_infos) == 3:
        product, model, count = product_infos
    data = {
        "products": [{
            "name": product,
            "count": count,
            "model": model
        }]
    }
    if hasattr(context, 'ship_address'):
        data.update(context.ship_address)

    #获得使用的积分
    if purchase_info.get('integral', None):
        tmp = 0
        try:
            tmp = int(purchase_info['integral'])
        except:
            pass

        # if tmp > 0:
        if tmp > 0 and purchase_info.get('integral', None):  #duhao 20150929 消费积分不能依赖于现获取积分,让integral列可以不填
            # 先为会员赋予积分,再使用积分
            # TODO 修改成jobs修改bill积分
            context.execute_steps(u"When %s获得%s的%s会员积分" % (webapp_user_name, webapp_owner_name, purchase_info['integral']))
        data['products'][0]['integral'] = tmp

    #获得优惠券
    if purchase_info.get('coupon', '') != '':
        if ',' in purchase_info['coupon']:
            coupon_name, coupon_id = purchase_info['coupon'].strip().split(',')
            coupon_dict = {}
            coupon_dict['name'] = coupon_name
            coupon_dict['coupon_ids'] = [ coupon_id ]
            coupon_list = [ coupon_dict ]
            context.coupon_list = coupon_list
            context.execute_steps(u"when %s领取%s的优惠券" % (webapp_user_name, webapp_owner_name))
        else:
            coupon_id = purchase_info['coupon'].strip()
        data['coupon'] = coupon_id

    #获得微众卡
    if purchase_info.get('weizoom_card', None) and ',' in purchase_info['weizoom_card']:
        card_name, card_pass = purchase_info['weizoom_card'].strip().split(',')
        card_dict = {}
        card_dict['card_name'] = card_name
        card_dict['card_pass'] = card_pass
        data['weizoom_card'] = [ card_dict ]

    if purchase_info.get('integral', '') != '':
        data['integral'] = int(purchase_info.get('integral'))
    if purchase_info.get('date') != '':
        data['date'] = purchase_info.get('date')
    if purchase_info.get('order_id', '') != '':
        data['order_id'] = purchase_info.get('order_id')

    print("SUB STEP: to buy products, param: {}".format(data))
    buy_product_cmd = BUY_PRODUCT_CMD % (webapp_user_name, corp_name, json.dumps(data))
    context.execute_steps(buy_product_cmd)

    #获得最新生成的订单（非出货单）
    order = mall_models.Order.select().dj_where(origin_order_id=-1).order_by(-mall_models.Order.id).first()
    return order


def __pay_order_in_apiserver(order, corp_name, pay_info, context):
    """
    支付订单

    payment的格式为 ${pay_type},${paytime}
    pay_type: 货到付款、优惠抵扣、支付宝、微信支付、微众卡支付
    paytime: 2天前，1月前，或2017-01-01 00:00
    """
    items = pay_info['payment'].split(',')
    pay_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    pay_type = items[0].strip()
    if len(items) == 2:
        pay_time = bdd_util.get_date(items[1])


    webapp_user_name = pay_info['consumer']
    context.execute_steps(u"when %s使用支付方式'%s'进行支付订单'%s'于%s::apiserver" % (webapp_user_name, pay_type, order.order_id, pay_time))


def __do_post_action_for_order_in_apiserver(order, corp_name, actor, action, context):
    """
    在apiserver中执行针对订单的操作
    """
    action2step = {
        u'完成': u"When %(webapp_user_name)s确认收货订单'%(order_bid)s'::apiserver",
        u'取消': u"When %(webapp_user_name)s取消订单'%(order_bid)s'::apiserver"
    }

    if action == u'完成':
        #apiserver要求订单处于ORDER_STATUS_PAYED_SHIPED才能进行finish操作
        mall_models.Order.update(status=mall_models.ORDER_STATUS_PAYED_SHIPED).dj_where(order_id=order.order_id).execute()

    step = action2step[action] % {
        'webapp_user_name': actor,
        'order_bid': order.order_id
    }
    context.execute_steps(step)


def __do_post_action_for_order_in_gaia(order, corp_name, actor, action, context):
    """
    在gaia中执行针对订单的操作
    """
    assert False, 'not implemented'
    

def __do_post_action_for_order(order, corp_name, action_info, context):
    """
    执行订单后操作

    action的格式为: ${actor},${action}
    actor: 操作人员，可以是微信用户，也可以是社群商城
    action: 操作人员进行的操作
    """
    webapp_user_name = action_info['consumer']
    actor, action = action_info['action'].split(',')
    if actor == webapp_user_name:
        __do_post_action_for_order_in_apiserver(order, corp_name, actor, action, context)
    elif actor == corp_name:
        __do_post_action_for_order_in_gaia(order, corp_name, actor, action, context)


@when(u"微信用户批量消费{corp_name}的商品")
def step_impl(context, corp_name):
    for row in context.table:
        order = __buy_product_in_apiserver(corp_name, row, context)

        #支付订单
        payment = row.get('payment', '').strip()
        if payment:
            __pay_order_in_apiserver(order, corp_name, row, context)

        #操作订单
        action = row.get('action', '').strip()
        if action:
            __do_post_action_for_order(order, corp_name, row, context)


OPERATION2STEPID = {
    u'支付': u"When %s'支付'最新订单",
    u'发货': u"When %s对最新订单进行发货",
    u'完成': u"When %s'完成'最新订单",
    u'退款': u"When %s'退款'最新订单",
    u'完成退款': u"When %s'完成退款'最新订单",
    u'取消': u"When %s'取消'最新订单",
}

@when(u"微信用户批量消费'{corp_name}'的商品_bak")
def step_impl(context, corp_name):
    for row in context.table:
        webapp_user_name = row['consumer']
        if webapp_user_name[0] == u'-':
            webapp_user_name = webapp_user_name[1:]
            #先关注再取消关注，模拟非会员购买  duhao  20160407
            context.execute_steps(u"When %s关注%s的公众号" % (webapp_user_name, webapp_owner_name))
            context.execute_steps(u"When %s取消关注%s的公众号" % (webapp_user_name, webapp_owner_name))
            openid = "%s_%s" %(webapp_user_name, webapp_owner_name)
            soucial_account_id = SocialAccount.objects.get(openid=openid).id
            member_id = MemberHasSocialAccount.objects.get(account_id=soucial_account_id).member_id
            Member.objects.filter(id=member_id).update(status=2)

            #clear last member's info in cookie and context
            context.execute_steps(u"When 清空浏览器")
        else:
            context.execute_steps(u"When 清空浏览器")
            context.execute_steps(u"When %s访问%s的webapp" % (webapp_user_name, webapp_owner_name))

        #购买商品
        product_infos = row['product'].strip().split(',')
        model = None
        if len(product_infos) == 2:
            product, count = product_infos
        elif len(product_infos) == 3:
            product, model, count = product_infos
        data = {
            "date": row['date'].strip(),
            "products": [{
                "name": product,
                "count": count,
                "model": model
            }]
        }
        if hasattr(context, 'ship_address'):
            data.update(context.ship_address)

        # TODO 统计BDD使用，需要删掉
        # purchase_type = u'测试购买' if row['type'] == u'测试' else None
        # if purchase_type:
        #   data['type'] = purchase_type
        # TODO 统计BDD使用，需要删掉
        # data['ship_name'] = webapp_user_name
        if row.get('integral', None):
            tmp = 0
            try:
                tmp = int(row['integral'])
            except:
                pass

            # if tmp > 0:
            if tmp > 0 and row.get('integral', None):  #duhao 20150929 消费积分不能依赖于现获取积分,让integral列可以不填
                # 先为会员赋予积分,再使用积分
                # TODO 修改成jobs修改bill积分
                context.execute_steps(u"When %s获得%s的%s会员积分" % (webapp_user_name, webapp_owner_name, row['integral']))
            data['products'][0]['integral'] = tmp

        if row.get('coupon', '') != '':
            if ',' in row['coupon']:
                coupon_name, coupon_id = row['coupon'].strip().split(',')
                coupon_dict = {}
                coupon_dict['name'] = coupon_name
                coupon_dict['coupon_ids'] = [ coupon_id ]
                coupon_list = [ coupon_dict ]
                context.coupon_list = coupon_list
                context.execute_steps(u"when %s领取%s的优惠券" % (webapp_user_name, webapp_owner_name))
            else:
                coupon_id = row['coupon'].strip()
            data['coupon'] = coupon_id

        if row.get('weizoom_card', None) and ',' in row['weizoom_card']:
            card_name, card_pass = row['weizoom_card'].strip().split(',')
            card_dict = {}
            card_dict['card_name'] = card_name
            card_dict['card_pass'] = card_pass
            data['weizoom_card'] = [ card_dict ]

        if row.get('integral', '') != '':
            data['integral'] = int(row.get('integral'))
        if row.get('date') != '':
            data['date'] = row.get('date')
        if row.get('order_id', '') != '':
            data['order_id'] = row.get('order_id')


        if row.get('pay_type', '') != '':
            data['pay_type'] = row.get('pay_type')


        print("SUB STEP: to buy products, param: {}".format(data))
        context.caller_step_purchase_info = data
        context.execute_steps(u"when %s购买%s的商品" % (webapp_user_name, webapp_owner_name))
        order = Order.objects.all().order_by('-id')[0]
        #支付订单

        if row.get('payment_time', '') != '' or row.get('payment', '') == u'支付':
            pay_type = row.get('pay_type', u'货到付款')
            if pay_type != '' != u'优惠抵扣':
                if 'order_id' in data:
                    context.created_order_id = data['order_id']
                context.execute_steps(u"when %s使用支付方式'%s'进行支付" % (webapp_user_name, pay_type))
            if row.get('payment_time', '') != '':
                Order.objects.filter(id=order.id).update(
                    payment_time=bdd_util.get_datetime_str(row['payment_time']))

        # 操作订单
        action = row['action'].strip()
        if action:
            actor, operation = action.split(',')
            context.execute_steps(u"given %s登录系统" % actor)
            if row.get('delivery_time') or operation == u'完成':
                step_id = OPERATION2STEPID.get(u'发货', None)
                context.latest_order_id = order.id
                context.execute_steps(step_id % actor)
            if row.get('delivery_time'):
                log = OrderOperationLog.objects.filter(
                order_id=order.order_id, action='订单发货').get()
                log.created_at =  bdd_util.get_date(row.get('delivery_time'))
                log.save()
            # if operation == u'取消' or operation == u'退款' or operation == u'完成退款':
            if operation == u'完成退款':  # 完成退款的前提是要进行退款操作
                step_id = OPERATION2STEPID.get(u'发货', None)
                context.latest_order_id = order.id
                context.execute_steps(step_id % actor)

                step_id = OPERATION2STEPID.get(u'完成', None)
                context.latest_order_id = order.id
                context.execute_steps(step_id % actor)
                step_id = OPERATION2STEPID.get(u'退款', None)
                context.latest_order_id = order.id
                context.execute_steps(step_id % actor)
            # if operation == u'退款':  # 完成退款的前提是要进行发货和完成操作
            #   step_id = OPERATION2STEPID.get(u'发货', None)
            #   context.latest_order_id = order.id
            #   context.execute_steps(step_id % actor)

            #   step_id = OPERATION2STEPID.get(u'完成', None)
            #   context.latest_order_id = order.id
            #   context.execute_steps(step_id % actor)

            step_id = OPERATION2STEPID.get(operation, None)
            if step_id:
                context.latest_order_id = order.id
                context.execute_steps(step_id % actor)
            elif operation == u'无操作':
                # 为了兼容之前默认为取消操作所做的处理
                pass
            else:
                raise
    context.caller_step_purchase_info = None
