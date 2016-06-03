# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.tools import models as tools_models

class ExpressDetail(business_model.Model):
    """
    订单物流详情
    """
    __slots__ = (
        'order_id',
        'express_id',
        'context',
        'status',
        'time',
        'ftime',
        'display_index',
        'created_at'
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
        express_detail = ExpressDetail(model)
        return express_detail

    @staticmethod
    @param_required(['express_number', 'express_company_name'])
    def from_express_info(args):
        details = []
        relations = tools_models.ExpressHasOrderPushStatus.select().dj_where(
                express_company_name=args['express_company_name'],
                express_number=args['express_number']
            )
        if relations.count() == 0:
            return details
        else:
            relation = relations.first()
        express_id = relation.id
        express_details = tools_models.ExpressDetail.select().dj_where(express_id=express_id)
        for detail in express_details:
            express_detail = ExpressDetail(detail)
            details.append(express_detail)

        return details