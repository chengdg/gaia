# -*- coding: utf-8 -*-

import settings
from eaglet.decorator import param_required
from eaglet.core import api_resource
from eaglet.core import watchdog
from business import model as business_model

from business.account.user_profile import UserProfile
from business.member.webapp_user import WebAppUser
from business.market_tools.template_message.template_message import TemplateMessage
from business.mall.order import Order
from business.mall.express import util as express_util
from business.weixin.weixin_service import WeixinService

from db.market_tools.template_message import models as market_tools_model


class OrderTemplageMessageService(TemplateMessage):
    """
    订单模版消息服务
    """
    
    def __init__(self, model):
        TemplateMessage.__init__(self, model)


    @staticmethod
    @param_required(['webapp_id', 'send_point'])
    def from_webapp_id(args):
        webapp_id = args['webapp_id']
        send_point = args['send_point']

        user_profile = UserProfile.from_webapp_id({
            'webapp_id': webapp_id
            })
        user_id = user_profile.user_id

        template_message_model = market_tools_model.MarketToolsTemplateMessage.select().dj_where(send_point=send_point).first()
        print webapp_id,">>>>>>>>>>!!!!!!!1`````111111",template_message_model.id
        if template_message_model:
            db_model =  market_tools_model.MarketToolsTemplateMessageDetail.select().dj_where(owner_id=user_id, template_message=template_message_model).first()
        else:
            db_model = None

        # db_model =  market_tools_model.MarketToolsTemplateMessageDetail.select().join(market_tools_model.MarketToolsTemplateMessage).dj_where(market_tools_model.MarketToolsTemplateMessage.send_point==send_point).first()
        
        if db_model:
            order_template_message_service = OrderTemplageMessageService(db_model)
            return order_template_message_service
        return None

    def send_order_templage_message(self, order_id):
        message = self.__get_order_message_dict(order_id)

        #调用 weixin service  发起模版消息调用
        weixin_service = WeixinService.from_user_id({
            "user_id": self.owner_id
            })
        if weixin_service:
            weixin_service.send_template_message(message)

    def __get_order_message_dict(self, order_id):
        template_data = dict()

        order = Order.from_order_id({
            "order_id": order_id
            })

        webapp_user = WebAppUser.from_id({
            "id": order.webapp_user_id
            })

        #social_account = member_model_api.get_social_account(order.webapp_user_id)
        if webapp_user:
            template_data['touser'] = webapp_user.openid
            template_data['template_id'] = self.template_id
            # if user_profile.host.find('http') > -1:
            #     host ="%s/workbench/jqm/preview/" % user_profile.host
            # else:
            #     host = "http://%s/workbench/jqm/preview/" % user_profile.host
            #rewrite ^/ http://$h5host/mall/order_detail/?woid=$webapp_owner_id&order_id=$arg_order_id&fmt=$arg_fmt? break;
            template_data['url'] = '%small/order_detail/?woid=%s&order_id=%s' % (settings.H5_HOST, self.owner_id, order.order_id)

            template_data['topcolor'] = "#FF0000"
            detail_data = {}
            #template_message_detail = template_message.template_message
            detail_data["first"] = {"value" : self.first_text, "color" : "#000000"}
            detail_data["remark"] = {"value" : self.remark_text, "color" : "#000000"}
            order.express_company_name =  u'%s快递' % express_util.get_name_by_value(order.express_company_name)
            if self.attribute:
                attribute_data_list = self.attribute.split(',')
                for attribute_datas in attribute_data_list:
                    attribute_data = attribute_datas.split(':')
                    key = attribute_data[0].strip()
                    attr = attribute_data[1].strip()
                    if attr == 'final_price' and getattr(order, attr):
                        value = u'￥%s［实际付款］' % getattr(order, attr)
                        detail_data[key] = {"value" : value, "color" : "#173177"}
                    elif hasattr(order, attr):
                        if attr == 'final_price':
                            value = u'￥%s［实际付款］' % getattr(order, attr)
                            detail_data[key] = {"value" : value, "color" : "#173177"}
                        elif attr == 'payment_time':
                            dt = datetime.now()
                            payment_time = dt.strftime('%Y-%m-%d %H:%M:%S')
                            detail_data[key] = {"value" : payment_time, "color" : "#173177"}
                        else:
                            detail_data[key] = {"value" : getattr(order, attr), "color" : "#173177"}
                    else:
                        if 'number' == attr:
                            number = len(order.products)
                            detail_data[key] = {"value" : number, "color" : "#173177"}

                        if 'product_name' == attr:
                            products = order.products
                            product_names =','.join([p['name'] for p in products])
                            detail_data[key] = {"value" : product_names, "color" : "#173177"}
            template_data['data'] = detail_data
        print ">>>>>@>@@>@@>@>>$>$>$>>>>>", template_data
        return template_data