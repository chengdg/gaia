# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.core.sendmail import sendmail
from business import model as business_model
from business.mall.order import Order
from business.mall.coupon.coupon import Coupon
from business.member.webapp_user import WebAppUser
from business.mall.express import util as express_util
from business.account.user_profile import UserProfile

from db.account import models as account_models
from db.mall import models as mall_models



class OrderEmilService(business_model.Model):
    """
    订单emailService
    """

    __slots__ = (
        'emails',
        'black_member_ids',
        'status',
        'is_active',
        'user_id'
        
    )

    def __init__(self, model):
        business_model.Model.__init__(self)

        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)
            # self.user_id = models.user_id

    @staticmethod
    @param_required(['webapp_id','status'])
    def from_status(args):
        user_profile = UserProfile.from_webapp_id({
            "webapp_id":  args['webapp_id']
            })

        notify_setting = account_models.UserOrderNotifySettings.select().dj_where(user_id=user_profile.user_id, status=args['status']).first()
        if notify_setting:
            notify_setting = OrderEmilService(notify_setting)
        else:
            notify_setting = None
        return notify_setting

    def send_message(self, order_id):
        order = Order.from_order_id({
            "order_id": order_id
            })

        if not order:
            return 

        webapp_user = WebAppUser.from_id({
            "id": order.webapp_user_id
            })

        if webapp_user:
            member_id = webapp_user.member.id
        else:
            member_id = -1

        if str(member_id) in str(self.black_member_ids).split('|') or self.emails == '':
            return

        coupon = 0
        if order.coupon_id != 0:
            coupon = Coupon.from_id({
                "id": order.coupon_id
                })
            if coupon:
                coupon = str(coupon.coupon_id)+u',￥'+str(order.coupon_money)


        buy_count = ''
        product_name = ''
        pic_address = ''
        for product in order.products:
            buy_count = buy_count+str(product['count'])+','
            product_name = product_name+product['name']+','

            # if product['thumbnails_url'].find('http') < 0:
            #     pic = "http://%s%s" % (settings.DOMAIN, pic)
            pic_address = pic_address+"<img src='%s' width='170px' height='200px'></img>" % (product['thumbnails_url'])

        buy_count = buy_count[:-1]
        product_name = product_name[:-1]

        buyer_address = order.ship_area+u" "+order.ship_address

        express_company_name = order.formated_express_company_name
        express_number = order.express_number


        order_status = mall_models.STATUS2TEXT.get(order.status, -9999)
        
        content_list = []

        content_described = u'微商城-%s-订单' % order_status

        content_list.append(u'商品名称：%s' % product_name)
        content_list.append(pic_address)
        content_list.append(u'订单号：%s' % order_id)
        content_list.append(u'下单时间：%s' % order.created_at)
        if order_status != -9999:
            content_list.append(u'订单状态：<font color="red">%s</font>' % order_status)
        
        if express_company_name:
            content_list.append(u'<font color="red">物流公司：%s</font>' % express_company_name)
        
        if express_number:
            content_list.append(u'<font color="red">物流单号：%s</font>' % express_number)
        
        if buy_count:
            content_list.append(u'订购数量：%s' % buy_count)
        
        content_list.append(u'支付金额：%s' % order.final_price)
        
        content_list.append(u'使用积分：%s' % order.integral)
        
        if coupon:
            content_list.append(u'优惠券：%s' % coupon)
        
        if order.bill:
            content_list.append(u'发票：%s' % order.bill)
        if order.postage:
            content_list.append(u'邮费：%s' % order.postage)
        content_list.append(u'收货人：%s' % order.buyer_name)
        content_list.append(u'收货人电话：%s' % order.ship_tel)
        content_list.append(u'收货人地址：%s' % buyer_address)
        if order.customer_message:
            content_list.append(u'顾客留言：%s' % order.customer_message)
        content = u'<br> '.join(content_list)

        try:
            for email in self.emails.split('|'):
                if email.find('@') > -1:
                    sendmail(email, content_described, content)
        except:
            if order.status == 0:
                notify_message = u"订单状态为已付款时发邮件失败，order_id={}, webapp_id={}, cause:\n{}".format(order_id, self.user_id, unicode_full_stack())
            elif order.status == 3:
                notify_message = u"订单状态为已发货时发邮件失败，order_id:{}，cause:\n{}".format(order_id, unicode_full_stack())
            else:
                notify_message = u"订单状态改变时发邮件失败，cause:\n{}".format(unicode_full_stack())

            watchdog.alert(notify_message)

   
        

        


    
    

