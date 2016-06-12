# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model

from business.account.user_profile import UserProfile

from db.market_tools.template_message import models as market_tools_model


class TemplateMessage(business_model.Model):
    """
    用户详情
    """
    __slots__ = (
        'id',
        'owner_id',
        'industry',
        'template_id',
        'first_text',
        'remark_text',
        'type',
        'status',
        'created_at'
    )

    def __init__(self, model):
        business_model.Model.__init__(self)

        self.context['db_model'] = model
        # self.context['user_profile'] = user_profile
        if model:
            self._init_slot_from_model(model)
            self.owner_id = model.owner_id

    @property
    def title(self):
        return self.context['db_model'].template_message.title

    @property
    def send_point(self):
       return self.context['db_model'].template_message.send_point

    @property
    def attribute(self):
       return self.context['db_model'].template_message.attribute