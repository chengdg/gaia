# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.account import models as account_models

class UserProfile(business_model.Model):
    """
    用户详情
    """
    __slots__ = (
        'id',
        'user_id',
        'webapp_id',
        'webapp_type',
        'app_display_name',
        'is_active',
        'note',
        'status',
        'is_mp_registered',
        'mp_token',
        'mp_url',
        'new_message_count',
        'webapp_template',
        'is_customed',
        'is_under_previewed',
        'expire_date_day',
        'force_logout_date',
        'host_name',
        'logout_redirect_to',
        'system_name',
        'system_version',
        'homepage_template_name',
        'backend_template_name',
        'homepage_workspace_id',
        'account_type',
        'is_oauth',
        'sub_account_count',
        'is_use_wepage',
        'store_name'
    )

    def __init__(self, model):
        business_model.Model.__init__(self)

        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

    @staticmethod
    @param_required(['webapp_ids'])
    def from_webapp_ids(args):
        user_profiles = []
        user_profiles_models = list(account_models.UserProfile.select().dj_where(webapp_id__in=args['webapp_ids']))

        for profile_model in user_profiles_models:
            user_profile = UserProfile(profile_model)
            user_profiles.append(user_profile)

        return user_profiles