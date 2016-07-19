# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from db.member import models as member_models
from business import model as business_model
from business.member.member import Member
from business.member.member_tags import MemberTag

class MemberHasTag(business_model.Model):
    '''
    会员分组
    '''
    __slots__ = (
        'id',
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
        return Member(self.context['db_model'].member)
        
    @property
    def member_tag(self):
        return MemberTag(self.context['db_model'].member_tag)

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

    @staticmethod
    @param_required(['member','member_tag'])
    def from_member_membertag(args):
        member_has_tag = member_models.MemberHasTag.select().dj_where(member=member.context['db_model'], member_tag=member_tag.context['db_model'])
        if member_has_tag:
            return MemberHasTag(member_has_tag)
        else:
            return None
    @staticmethod
    @param_required(['member'])
    def from_member(args):
        member_has_tags = member_models.MemberHasTag.select().dj_where(member=args['member'].context['db_model'])
        if member_has_tags:
            return [MemberHasTag(member_has_tag) for member_has_tag in member_has_tags]
        else:
            return []
    @staticmethod
    @param_required(['member_tags'])
    def from_member_tags(args):
        member_tags = [member_tag.context['db_model'] for member_tag in args['member_tags']]
        member_has_tags = member_models.MemberHasTag.select().dj_where(member_tag__in=member_tags)
        if member_has_tags:
            return [MemberHasTag(member_has_tag) for member_has_tag in member_has_tags]
        else:
            return []

    def delete_from_ids(self, member_has_tag_ids):
        return member_models.MemberHasTag.delete().dj_where(id__in=member_has_tag_ids).execute()        

