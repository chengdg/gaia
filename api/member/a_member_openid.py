# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required

from business.member.social_account import SocialAccount
from business.member.member import Member

class AMemberOpenId(api_resource.ApiResource):
    """
    通过会员ID获取openid
    """
    app = "member"
    resource = "member_openid"

    @param_required(['member_id'])
    def get(args):
		corp = args['corp']
		memeber_id = args['member_id']
		# 获取social_account
		social_account = corp.social_account_repository.get_social_account(memeber_id)
        social_account_dic = {
            'id':social_account.id,
            'openid':social_account.openid,
            'webapp_id':social_account.webapp_id,
            'token':social_account.token
        }
		return {
            'social_account': social_account_dic
        }