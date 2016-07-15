# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from db.member import models as member_models
from business.member.member_tag import  MemberTag


class MemberTagFactory(business_model.Model):
    '''
    @会员分组  @@@@工厂方法
    '''
    __slots__ = (
    )

    def __init__(self):
        business_model.Model.__init__(self)

    @staticmethod
    @param_required(['webapp_id', 'name'])
     def save(args):
        '''
        '''
        member_tag = MemberTag.empty_member_tags()
        opt = {
            'webapp_id': webapp_id,
            'name': name
        }
        return member_tag.create(opt)