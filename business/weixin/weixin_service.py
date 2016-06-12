# -*- coding: utf-8 -*-

import settings
from eaglet.decorator import param_required
from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.core.wxapi import get_weixin_api
from business import model as business_model

from business.account.user_profile import UserProfile

from db.weixin import models as weixin_models


class WeixinService(business_model.Model):
    """
    微信service
    """
    __slots__ = (
        'id',
        'authorizer_appid',
        'authorizer_access_token',
        'user_id',
        'access_token',
        'weixin_api'
    )

    
    def __init__(self, model):
        business_model.Model.__init__(self)

        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)
            self.access_token = model.authorizer_access_token
            self.weixin_api = get_weixin_api(self)

    @staticmethod
    @param_required(['user_id'])
    def from_user_id(args):
        user_id = args['user_id']
        db_model = weixin_models.ComponentAuthedAppid.select().dj_where(user_id=user_id).first()

        if db_model:
            weixin_service = WeixinService(db_model)
            return weixin_service
        return None

    def send_template_message(self, message):
        result = self.weixin_api.send_template_message(message)
        watchdog.info(result)
