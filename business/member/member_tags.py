# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from db.member import models as member_models
from business import model as business_model


class MemberTag(business_model.Model):
    '''
    设置会员分组
    '''
    __slots__ = (
        'webapp_id',
        'name',
        'created_at'
    )

    def __init__(self,model):
        business_model.Model.__init__(self)

        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

    def update_member_tag_name(self, member_tag_id, name):
        '''
        修改会员分组名称
        '''
        return member_models.MemberTag.update(name=name).dj_where(id=member_tag_id).execute()

    def create(self, webapp_id, name):
        opt = {
            'webapp_id': webapp_id,
            'name': name
        }
        member_tag = member_models.MemberTag.create(**opt)
        return MemberTag(member_tag)
