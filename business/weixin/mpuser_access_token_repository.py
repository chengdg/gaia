# -*- coding: utf-8 -*-
"""
素材
"""
from eaglet.core import paginator
from eaglet.core import watchdog

from eaglet.decorator import cached_context_property
from eaglet.decorator import param_required

from business import model as business_model
from business.weixin.mpuser_access_token import MpuserAccessToken
from business.weixin.weixin_mpuser import WeixinMpuser

from db.weixin import models as weixin_models
from db.account import models as account_models


class MpuserAccessTokenRepository(business_model.Service):

	def get_mpuser_access_token(self, corp_id):
		"""
		获取access_token
		"""
		weixin_mpuser_model = weixin_models.WeixinMpUser.select().dj_where(owner_id=corp_id).first()
		weixin_mpuser = WeixinMpuser(weixin_mpuser_model)
		weixin_mpuser_access_token_model = weixin_models.WeixinMpUserAccessToken.select().dj_where(mpuser_id=weixin_mpuser.id).first()
		return MpuserAccessToken(weixin_mpuser_access_token_model)

