# -*- coding: utf-8 -*-
import json

from eaglet.decorator import param_required
from eaglet.core.cache import utils as cache_util
from db.mall import models as mall_models
from eaglet.core import watchdog

from business import model as business_model

class OrderHasGroup(business_model.Model):
    """
    团购订单的关系
    """

    __slots__ = (
        'id',
        'order_id', #订单编号
        'group_id',
        'activity_id',
        'group_status',
        'webapp_user_id',
        'webapp_id'
    )

    def __init__(self, model):
        business_model.Model.__init__(self)

        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

    @staticmethod
    @param_required(['db_model'])
    def from_model(args):
        model = args['db_model']
        order_has_group = OrderHasGroup(model)
        return order_has_group

    @staticmethod
    @param_required(['group_id'])
    def from_group_id(args):
        """
        更具订单获取团购订单对象
        """
        order_has_group_models = mall_models.OrderHasGroup.select().dj_where(
                                    group_id=args['group_id'])
        relations = []
        for model in order_has_group_models:
            relations.append(OrderHasGroup(model))
        return relations

    @staticmethod
    @param_required(['group_id'])
    def get_group_order_ids(args):
        relations = OrderHasGroup.from_group_id({'group_id': args['group_id']})
        return [r.order_id for r in relations]

    @staticmethod
    @param_required(['order_ids'])
    def from_order_ids(args):
        """
        更具订单获取团购订单对象
        """
        order_has_group_models = mall_models.OrderHasGroup.select().dj_where(
                                    order_id__in=args['order_ids'])
        relations = []
        for model in order_has_group_models:
            relations.append(OrderHasGroup(model))
        return relations

    @staticmethod
    def update(group_id, status):
        mall_models.OrderHasGroup.update(
                group_status=status
            ).dj_where(group_id=group_id).execute()

    @staticmethod
    @param_required(['webapp_id'])
    def from_webapp_id(args):
        order_has_groups = mall_models.OrderHasGroup.select().dj_where(webapp_id=args['webapp_id'])
        if order_has_groups.count() !=0:
            return [x  for x in order_has_groups]
        else:
            return None