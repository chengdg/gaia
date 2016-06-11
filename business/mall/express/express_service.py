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

    def __init__(self, order):
        # express_configs = ExpressServiceConfig.objects.filter(value=1)
        # if express_configs.count() > 0:
        #     express_config = express_configs[0]
        #     if express_config.name == u"快递鸟":
        #         from tools.express.kdniao_express_poll import KdniaoExpressPoll
        #         is_success = KdniaoExpressPoll(order).get_express_poll()
        #     elif express_config.name == u"快递100":
        #         from tools.express.express_poll import ExpressPoll
        #         is_success = ExpressPoll(order).get_express_poll()
        # else:
        #     from tools.express.express_poll import ExpressPoll
        #     is_success = ExpressPoll(order).get_express_poll()
        # print u'----------- send_request_to_kuaidi: {}'.format(is_success)
        business_model.Model.__init__(self)
        model = express_models.ExpressServiceConfig.select().dj_where(value=1).first()
        if model:
            self.context['db_model'] = model
            self._init_slot_from_model(model)
            if self.name == u"快递鸟":
                self.express_poll = KdniaoExpressPoll(order).get_express_poll()
            elif self.name == u"快递100":
                self.express_poll = ExpressPoll(order)
        else:
            self.express_poll = ExpressPoll(order)

    def get_express_poll(self):
        return self.express_poll.get_express_poll()

    # @staticmethod
    # @param_required([''])
    # def from_model(args):
    #     model = args['db_model']
    #     product = Product(model)
    #     return product

    # @staticmethod
    # @param_required(['value'])
    # def from_value(args):
    #     db_model = express_models.ExpressServiceConfig.select().dj_where(value=args['value']).first()
    #     if db_model:
            
    #     return Supplier(supplier_db_model)