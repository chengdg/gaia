# -*- coding: utf-8 -*-
"""
会员
"""
from eaglet.core import paginator
from eaglet.core import watchdog

from business.common.page_info import PageInfo
from eaglet.decorator import cached_context_property
from eaglet.decorator import param_required

from business import model as business_model
from business.member.social_account import SocialAccount

from db.member import models as member_models


class SocialAccountRepository(business_model.Service):

    def get_social_account(self, member_id):
        member_model = member_models.MemberHasSocialAccount.select().dj_where(member_id=member_id).first()
        account_model = member_models.SocialAccount.select().dj_where(id=member_model.account_id).first()
        return SocialAccount(account_model)