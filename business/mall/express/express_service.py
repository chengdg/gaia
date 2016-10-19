# -*- coding: utf-8 -*-
from eaglet.decorator import param_required

from db.mall import models as mall_models
from db.express import models as express_models
from business import model as business_model

from business.mall.express.express_poll import ExpressPoll
from business.mall.express.kdniao_express_poll import KdniaoExpressPoll

class ExpressService(business_model.Model):
    __slots__ = (
        'id',
        'name',
        'value',
        'express_poll'
    )

    def __init__(self, delivery_item):
        business_model.Model.__init__(self)
        model = express_models.ExpressServiceConfig.select().dj_where(value=1).first()
        if model:
            self.context['db_model'] = model
            self._init_slot_from_model(model)
            if self.name == u"快递鸟":
                self.express_poll = KdniaoExpressPoll(delivery_item)
            elif self.name == u"快递100":
                self.express_poll = ExpressPoll(delivery_item)
        else:
            self.express_poll = ExpressPoll(delivery_item)

    def get_express_poll(self):
        return self.express_poll.get_express_poll()
