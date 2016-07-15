# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from db.member import models as member_models
from business.member.member_has_tag import MemberHasTag


class MemberTagFactory(business_model.Model):
    '''
    @会员分组  @@@@工厂方法
    '''
    __slots__ = (
    )

    def __init__(self):
        business_model.Model.__init__(self)

    @staticmethod
    @param_required(['member', 'member_tag'])
     def save(args):
        '''
        '''
        member_tag = MemberHasTag.empty_member_tags()
        opt = {
            'webapp_id': webapp_id,
            'name': name
        }
        return member_tag.create(opt)