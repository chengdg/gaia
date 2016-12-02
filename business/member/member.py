# -*- coding: utf-8 -*-
"""@package business.account.member
会员
"""

import re
import json
import math
import logging
from bs4 import BeautifulSoup
from datetime import datetime

from eaglet.decorator import param_required
from eaglet.decorator import cached_context_property
from eaglet.utils.string_util import hex_to_byte, byte_to_hex
from eaglet.core import watchdog
from eaglet.core.cache import utils as cache_util

import settings
from business.account.integral import Integral
from util import emojicons_util
from db.member import models as member_models
from business import model as business_model
from business.member.member_has_tag import MemberHasTag



class Member(business_model.Model):
    """
    会员
    """
    __slots__ = (
        'id',
        'grade_id',
        'username_hexstr',
        #'webapp_user',
        'is_subscribed',
        'created_at',
        'token',
        'webapp_id',
        'pay_money',
        'update_time',
        'status',
        'experience',
        'remarks_name',
        'remarks_extra',
        'last_visit_time',
        'session_id',
        'is_subscribed',
        'friend_count',
        'factor',
        'source',
        'integral',
        'update_time',
        'pay_times',
        'last_pay_time',
        'unit_price',
        'city',
        'province',
        'country',
        'sex',
        'purchase_frequency',
        'cancel_subscribe_time',
        'fans_count'
    )


    @staticmethod
    @param_required(['models'])
    def from_models(args):
        """
        工厂对象，根据member model获取Member业务对象

        @param[in] model: member model

        @return Member业务对象
        """
        models = args['models']
        corp = args['corp']
        members = []
        for model in models:

            member = Member(model)
            member.context['corp'] = corp
            member.context['db_model'] = model
            members.append(member)
        return members

    def __init__(self, model):
        business_model.Model.__init__(self)

        #self.context['webapp_owner'] = webapp_owner
        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

    def increase_integral_after_finish_order(self, order):

        Integral.increase_after_order_payed_finsh({
            'member': self,
            'order': order,
            'corp': self.context['corp']
        })


    def update_pay_info(self,order,from_status,to_status):
        # todo order搜索完成后使用order_repository
        from db.mall import models as mall_models

        db_model = self.context['db_model']
        if to_status == 'paid':
            db_model.last_pay_time = order.payment_time

        webapp_user_id = order.webapp_user_id

        pay_money = 0
        pay_times = 0

        user_orders = mall_models.Order.select().dj_where(webapp_user_id=webapp_user_id)

        if user_orders.dj_where(status__gte=mall_models.ORDER_STATUS_PAYED_SUCCESSED).count() > 0:
            payment_time = user_orders.order_by(mall_models.Order.payment_time)[0].payment_time
            db_model.last_pay_time = payment_time

        for user_order in user_orders:
            user_order.final_price = user_order.final_price + user_order.weizoom_card_money
            if user_order.status == mall_models.ORDER_STATUS_SUCCESSED:
                pay_money += user_order.final_price
                pay_times += 1

        db_model.pay_times = pay_times
        db_model.pay_money = pay_money

        if pay_times > 0:
            db_model.unit_price = pay_money / pay_times
        else:
            db_model.unit_price = 0

        db_model.save()


    @cached_context_property
    def __grade(self):
        """
        [property] 会员等级信息
        """
        member_model = self.context['db_model']

        if not member_model:
            return None

        return member_model.grade

    @property
    def discount(self):
        """
        [property] 会员折扣

        @return 返回二元组(grade_id, 折扣百分数)
        """
        member_model = self.context['db_model']
        if not member_model:
            return -1, 100

        member_grade = self.__grade
        if member_grade:
            return member_model.grade_id, member_grade.shop_discount
        else:
            return member_model.grade_id, 100

    @property
    def grade(self):
        """
        [property] 会员等级
        """
        return self.__grade

    @property
    def grade_name(self):
        """
        [property] 会员等级名称
        """
        return self.__grade.name

    @cached_context_property
    def __tags(self):
        """
        [property] 会员分组信息
        """
        member_model = self.context['db_model']

        if not member_model:
            return None
        member_tags = MemberHasTag.get_member_tags({'member_id': member_model.id})
        return member_tags


    @property
    def tags(self):
        """
        [property] 会员分组信息列表
        """
        return self.__tags

    @cached_context_property
    def __info(self):
        """
        [property] 与会员对应的MemberInfo model对象
        """
        member_model = self.context['db_model']
        if not member_model:
            return None

        try:
            member_info = member_models.MemberInfo.get(member=member_model)
        except:
            member_info = member_models.MemberInfo()
            member_info.member = member_model
            member_info.name = ''
            member_info.weibo_name = ''
            member_info.phone_number = ''
            member_info.sex = member_models.SEX_TYPE_UNKOWN
            member_info.is_binded = False
            member_info.weibo_nickname = ''
            member_info.phone_number = ''
            member_info.save()

        if member_info.phone_number and len(member_info.phone_number) > 10:
            member_info.phone =  '%s****%s' % (member_info.phone_number[:3], member_info.phone_number[-4:])
        else:
            member_info.phone = ''

        return member_info

    @property
    def phone(self):
        """
        [property] 会员绑定的手机号码加密
        """

        return self.__info.phone

    @cached_context_property
    def phone_number(self):
        """
        [property] 会员绑定的手机号码
        """

        return self.__info.phone_number


    @cached_context_property
    def captcha(self):
        """
        [property] 手机验证码
        """
        return self.__info.captcha

    @cached_context_property
    def captcha_session_id(self):
        """
        [property] 手机验证码
        """
        return self.__info.session_id

    @property
    def name(self):
        """
        [property] 会员名
        """

        return self.__info.name

    @property
    def is_binded(self):
        """
        [property] 会员是否进行了绑定
        """
        return self.__info.is_binded

    @cached_context_property
    def user_icon(self):
        """
        [property] 会员头像
        """
        return self.context['db_model'].user_icon

    @cached_context_property
    def username_for_html(self):
        """
        [property] 兼容html显示的会员名
        """
        if (self.username_hexstr is not None) and (len(self.username_hexstr) > 0):
            username = emojicons_util.encode_emojicons_for_html(self.username_hexstr, is_hex_str=True)
        else:
            username = emojicons_util.encode_emojicons_for_html(self.username)

        try:
            username.decode('utf-8')
        except:
            username = self.username_hexstr

        return username

    @cached_context_property
    def market_tools(self):
        """
        [property] 会员参与的营销工具集合
        """
        #TODO2: 实现营销工具集合
        print u'TODO2: 实现营销工具集合'
        return []

    @staticmethod
    def empty_member():
        """工厂方法，创建空的member对象

        @return Member对象
        """
        member = Member(None, None)
        return member


    @property
    def username(self):
        return hex_to_byte(self.username_hexstr)

    @cached_context_property
    def username_size_ten(self):
        try:
            username = unicode(self.username_for_html, 'utf8')
            _username = re.sub('<[^<]+?><[^<]+?>', ' ', username)
            if len(_username) <= 10:
                return username
            else:
                name_str = username
                span_list = re.findall(r'<[^<]+?><[^<]+?>', name_str) #保存表情符

                output_str = ""
                count = 0

                if not span_list:
                    return u'%s...' % name_str[:10]

                for span in span_list:
                    length = len(span)
                    while not span == name_str[:length]:
                        output_str += name_str[0]
                        count += 1
                        name_str = name_str[1:]
                        if count == 10:
                            break
                    else:
                        output_str += span
                        count += 1
                        name_str = name_str[length:]
                        if count == 10:
                            break
                    if count == 10:
                        break
                return u'%s...' % output_str
        except:
            return self.username_for_html[:10]



