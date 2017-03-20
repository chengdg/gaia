# -*- coding: utf-8 -*-
import json
from datetime import datetime

from db.account.models import User, UserProfile
from behave import *
from features.util import bdd_util
from db.mall import models as mall_models
from db.mall import promotion_models as promotion_models
from db.account import models as account_models
from db.member import models as member_models
from eaglet.utils.string_util import hex_to_byte, byte_to_hex


NAME2REALNAME = {
    'zhouxun': u'周迅',
    'yangmi': u'杨幂',
    'yaochen': u'姚晨',
    'bigs': u'大S',
    'zhaowei': u'赵薇',
    'mayun': u'马云',
    'leijun': u'雷军',
    'liyanhong': u'李彦宏',
    'dinglei': u'丁磊',
    'mahuateng': u'马化腾'
}


@Given(u"{user}成为'{mp_user_name}'的会员")
def step_impl(context, user, mp_user_name):
    weixin_user_name = user
    mp_user = User.get(username=mp_user_name)
    mp_user_profile = UserProfile.get(user=mp_user.id)

    source = u'直接关注'
    if context.text:
        source = json.loads(context.text)['source']
    if source == u'直接关注':
        source = member_models.SOURCE_SELF_SUB
    elif source == u'推广扫码':
        source = member_models.SOURCE_MEMBER_QRCODE
    elif source == u'会员分享':
        source = member_models.SOURCE_BY_URL

    if member_models.Member.select().dj_where(webapp_id=mp_user_profile.webapp_id, remarks_name=weixin_user_name).count() > 0:
        #print 'member [%s] already exists' % weixin_user_name
        return

    member_grade = member_models.MemberGrade.get(webapp_id=mp_user_profile.webapp_id, is_default_grade=True)
    member_tag = member_models.MemberTag.get(webapp_id=mp_user_profile.webapp_id, name=u'未分组')

    #create new member
    social_account = member_models.SocialAccount.create(
        webapp_id = mp_user_profile.webapp_id,
        token = 'sa_%s_token' % weixin_user_name,
        access_token = 'sa_%s_access_token' % weixin_user_name,
        openid = '%s_%s' % (weixin_user_name, mp_user_name)
    )

    member = member_models.Member.create(
        webapp_id = mp_user_profile.webapp_id,
        token = 'm_%s_token' % weixin_user_name,
        grade = member_grade.id,
        integral = 0,
        is_subscribed = True,
        username_hexstr = byte_to_hex(weixin_user_name),
        remarks_name = weixin_user_name,
        source = source,
        user_icon = 'http://weapp.weizoom.com/static/img/user-1.jpg'
    )

    member_models.WebAppUser.create(
        token = 'wu_%s_token' % weixin_user_name,
        webapp_id = mp_user_profile.webapp_id,
        member_id = member.id
    )

    member_models.MemberInfo.create(
        member = member.id,
        name = NAME2REALNAME[weixin_user_name],
        weibo_nickname = '',
        binding_time = datetime.now()
    )

    member_models.MemberHasSocialAccount.create(
        member = member.id,
        account = social_account.id,
        webapp_id = mp_user_profile.webapp_id
    )

    member_models.MemberHasTag.create(
        member = member.id,
        member_tag = member_tag.id
    )


@When(u"{user}改变会员'{member_name}'的分组为")
def step_impl(context, user, member_name):
    member = bdd_util.get_member_for(member_name, context.corp.webapp_id)

    data = {
        'corp_id': context.corp.id,
        'member_id': member.id
    }
    member_group_ids = []
    member_tag_names = json.loads(context.text)
    for tag_name in member_tag_names:
        member_tag = member_models.MemberTag.select().dj_where(name=tag_name).get()
        member_group_ids.append(member_tag.id)
    data['member_group_ids'] = json.dumps(member_group_ids)

    response = context.client.put('/member/group_memberships/', data)
    bdd_util.assert_api_call_success(response)


@When(u"{user}批量调整会员的等级为'{member_grade_name}'")
def step_impl(context, user, member_grade_name):
    member_names = json.loads(context.text)
    member_ids = []
    for member_name in member_names:
        member = bdd_util.get_member_for(member_name, context.corp.webapp_id)
        member_ids.append(member.id)

    member_grade = member_models.MemberGrade.select().dj_where(name=member_grade_name).get()

    data = {
        'corp_id': context.corp.id,
        'member_ids': json.dumps(member_ids),
        'member_grade_id': member_grade.id
    }

    response = context.client.post('/member/grade_memberships/', data)
    bdd_util.assert_api_call_success(response)


@When(u"{user}为会员'{member_name}'增加积分'{integral}'")
def step_impl(context, user, member_name, integral):
    reason = ''
    if context.text:
        reason = json.loads(context.text)['reason']

    member = bdd_util.get_member_for(member_name, context.corp.webapp_id)

    data = {
        'corp_id': context.corp.id,
        'member_id': member.id,
        'integral_increment': integral,
        'reason': reason
    }

    response = context.client.put('/member/integral_increment/', data)
    bdd_util.assert_api_call_success(response)


@When(u"{user}为会员每人发放'{count_per_member}'张优惠券'{coupon_rule_name}'")
def step_impl(context, user, count_per_member, coupon_rule_name):
    #sleep一会儿，让优惠券发送的时间有差别，保证测试的排序结果
    import time
    time.sleep(1)
    coupon_rule = promotion_models.CouponRule.select().dj_where(name=coupon_rule_name).get()

    member_names = json.loads(context.text)
    member_ids = []
    for member_name in member_names:
        member = bdd_util.get_member_for(member_name, context.corp.webapp_id)
        member_ids.append(member.id)

    data = {
        'corp_id': context.corp.id,
        'member_ids': json.dumps(member_ids),
        'count_per_member': count_per_member,
        'coupon_rule_id': coupon_rule.id
    }

    response = context.client.put('/member/coupons/', data)
    bdd_util.assert_api_call_success(response)


@Then(u"{user}能获得会员'{member_name}'的积分日志")
def step_impl(context, user, member_name):
    member = bdd_util.get_member_for(member_name, context.corp.webapp_id)
    url = '/member/integral_logs/?corp_id=%s&member_id=%s' % (context.corp.id, member.id)

    response = context.client.get(url)
    data = response.data
    actual = []
    for integral_log in data['integral_logs']:
        actual.append({
            'id': integral_log['id'],
            'event': integral_log['event'],
            'integral_increment': integral_log['integral_increment'],
            'reason': integral_log['reason'],
            'actor': integral_log['actor'],
            'current_integral': integral_log['current_integral']
        })

    expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual)


@Then(u"{user}能获得会员'{member_name}'的优惠券集合")
def step_impl(context, user, member_name):
    member = bdd_util.get_member_for(member_name, context.corp.webapp_id)
    url = '/member/coupons/?corp_id=%s&member_id=%s' % (context.corp.id, member.id)

    response = context.client.get(url)
    data = response.data
    actual = []
    for coupon in data['coupons']:
        actual.append({
            'id': coupon['id'],
            'money': coupon['money'],
            'name': coupon['name'],
            'is_for_specific_products': coupon['using_limit']['is_for_specific_products'],
            'status': coupon['status']
        })

    expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual)


def __extract_member_info(data):
    """
    获取member数据
    """
    consume_info = data['consume_info']

    source2str = {
        'self_subscribe': u'直接关注',
        'member_qrcode': u'推广扫码',
        'share_url': u'会员分享'
    }
    subscribe_info = data['subscribe_info']
    source = source2str[subscribe_info['source']]

    result = {
        'name': data['name'],
        'grade': data['grade'],
        'integral': consume_info['integral'],
        'source': source
    }
    result['groups'] = dict([(group['name'], 1) for group in data['groups']])

    return result


@Then(u"{user}能获得会员'{member_name}'的信息")
def step_impl(context, user, member_name):
    member = bdd_util.get_member_for(member_name, context.corp.webapp_id)
    url = '/member/member/?corp_id=%s&id=%s' % (context.corp.id, member.id)

    response = context.client.get(url)
    data = response.data
    actual = __extract_member_info(data)

    expected = json.loads(context.text)
    if 'groups' in expected:
        expected['groups'] = dict([(group, 1) for group in expected['groups']])
    bdd_util.assert_dict(expected, actual)


@When(u"{user}能获得会员列表")
def step_impl(context, user):
    url = '/member/members/?corp_id=%s' % context.corp.id

    response = context.client.get(url)
    actual = []
    for member_data in response.data['members']:
        actual.append(__extract_member_info(member_data))

    expected = json.loads(context.text)
    for item in expected:
        if 'groups' in item:
            item['groups'] = dict([(group, 1) for group in item['groups']])
    bdd_util.assert_list(expected, actual)