# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from db.member import models as member_models
from business import model as business_model


class MemberTag(business_model.Model):
    '''
    设置会员分组
    '''
    __slots__ = (
        'id',
        'webapp_id',
        'name',
        'created_at'
    )

    def __init__(self,model):
        business_model.Model.__init__(self)

        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

    @staticmethod
    def empty_member_tags(model=None):
        return MemberTag(model)

    def update_member_tag_name(self, member_tag_id, name):
        '''
        修改会员分组名称
        '''
        return member_models.MemberTag.update(name=name).dj_where(id=member_tag_id).execute()

    def create(self, webapp_id, name, id=None):
        opt = {
            'webapp_id': webapp_id,
            'name': name
        }
        if id:
            opt.update({'id': id})
        member_tag = member_models.MemberTag.create(**opt)
        return MemberTag(member_tag)

    @staticmethod
    @param_required(['member_tag_id'])
    def from_id(args):
        member_tag = member_models.MemberTag.select().dj_where(id=args['member_tag_id']).first()
        if member_tag:
            return MemberTag(member_tag)
        else:
            return None

    @staticmethod
    @param_required(['webapp_id'])
    def from_webapp_id(args):
        '''
        通过weapp_id找未分组对象
        '''
        member_tag = member_models.MemberTag.select().dj_where(webapp_id=args['webapp_id'], name='未分组').first()
        if member_tag:
            return MemberTag(member_tag)
        else:
            return None

    def delete_from_ids(self, member_tag_ids):
        '''
        通过会员分组id删除分组
        '''
        return member_models.MemberTag.delete().dj_where(id__in=member_tag_ids).execute()


