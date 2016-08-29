# -*- coding: utf-8 -*-

from eaglet.core import watchdog
from eaglet.decorator import param_required

from business import model as business_model
from db.weixin import models as weixin_models

class ComponentAuthedAppidInfo(business_model.Model):
    """
    委托授权帐号详细信息
    """
    __slots__ = (
        'auth_appid',
        'nick_name',
        'head_img',
        'service_type_info',
        'verify_type_info',
        'user_name',
        'alias',
        'qrcode_url',
        'appid',
        'func_info',
        'created_at'
    )

    def __init__(self, model):
        business_model.Model.__init__(self)

        self.context['db_model'] = db_model
        if db_model:
            self._init_slot_from_model(db_model)

    @staticmethod
    @param_required(['owner_id'])
    def get_auth_appid_by_owner_id(args):
        owner_id = args['owner_id']

        component_basic_info_model = weixin_models.ComponentAuthedAppid.select().dj_where(user_id=owner_id).first()
        component_detail_info_model = weixin_models.ComponentAuthedAppidInfo.select().dj_where(
                                            id=component_basic_info_model.component_info_id).first()
        return component_detail_info_model.appid