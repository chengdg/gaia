# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from db.member import models as member_models
from business import model as business_model

class MemberHasTag(business_model.Model):
    '''
    会员分组
    '''
    __slots__ = (
    )

    def __init__(self,model):
        business_model.Model.__init__(self)

        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

    @staticmethod
    def empty_member_has_tag(model=None):
        return MemberHasTag(model)

    @property
    def member(self):
        pass
        
    @property
    def member_tag(self):
        pass

    def create(self, member, member_tag):
        opt = {
            'member': member.context['db_model'],
            'member_tag': member_tag.context['db_model']
        }
        member_has_tag = member_models.MemberHasTag.get_or_create(**opt)
        return MemberHasTag(member_has_tag)

    @staticmethod
    @param_required(['member'])
    def delete_member_has_tags(args):
        member_has_tag = member_models.MemberHasTag.delete().dj_where(member=args['member'].context['db_model']).execute()
        return member_has_tag

