# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from db.member import models as member_models
from business.member.member_tags import  MemberTag
from business import model as business_model
from db.account import models as account_models



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
        return member_tag.create(args['webapp_id'], args['name'])