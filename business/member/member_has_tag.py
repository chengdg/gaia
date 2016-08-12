# -*- coding: utf-8 -*-
"""@package business.member
会员分组
"""
from business import model as business_model

from eaglet.decorator import param_required

from db.member import models as member_models

class MemberHasTag(business_model.Model):
    """
    会员分组
    """
    __slots__ = (
        'memeber_id',
        'tag_id'
    )

    def __init__(self, model):
        business_model.Model.__init__(self)

        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

    @staticmethod
    @param_required(['member_id'])
    def get_member_tags(args):
        member_id = args['member_id']
        member_has_tag_models = member_models.MemberHasTag.select().dj_where(member_id=member_id)
        member_tag_ids = [model.member_tag_id for model in member_has_tag_models]
        if member_tag_ids:
            member_tag_models = member_models.MemberTag.select().dj_where(id__in=member_tag_ids)
            return [{'id': model.id, 'name': model.name} for model in member_tag_models]
        else:
            return []