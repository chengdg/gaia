# -*- coding: utf-8 -*-
import json
from datetime import datetime

from db.account.models import User, UserProfile
from behave import *
from features.util import bdd_util
from db.mall import models as mall_models
from db.account import models as account_models
from db.member import models as member_models
from eaglet.utils.string_util import hex_to_byte, byte_to_hex


@Given(u"{user}成为'{mp_user_name}'的会员")
def step_impl(context, user, mp_user_name):
    weixin_user_name = user
    mp_user = User.get(username=mp_user_name)
    mp_user_profile = UserProfile.get(user=mp_user.id)

    member_grade = member_models.MemberGrade.get(webapp_id=mp_user_profile.webapp_id, is_default_grade=True)

    if member_models.Member.select().dj_where(webapp_id=mp_user_profile.webapp_id, username_hexstr=weixin_user_name).count() > 0:
        print 'member [%s] already exists' % weixin_user_name
        return

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
        user_icon = ''
    )

    member_models.WebAppUser.create(
        token = 'wu_%s_token' % weixin_user_name,
        webapp_id = mp_user_profile.webapp_id,
        member_id = member.id
    )

    member_models.MemberInfo.create(
        member = member.id,
        name = weixin_user_name,
        weibo_nickname = '',
        binding_time = datetime.now()
    )

    member_models.MemberHasSocialAccount.create(
        member = member.id,
        account = social_account.id,
        webapp_id = mp_user_profile.webapp_id
    )


@Then(u"{user}能获得会员'{member_name}'的信息")
def step_impl(context, user, member_name):
    member = bdd_util.get_member_for(member_name, context.corp.webapp_id)
    url = '/member/member/?corp_id=%s&id=%s' % (context.corp.id, member.id)


    response = context.client.get(url)
    data = response.data
    actual = {
        'name': data['name']
    }

    expected = json.loads(context.text)
    bdd_util.assert_dict(expected, actual)

