# -*- coding: utf-8 -*-

from eaglet.core import watchdog
from eaglet.decorator import param_required

from business import model as business_model
from db.mall import models as mall_models


class WeixinPayV3Config(business_model.Model):
    """
    微信支付信息 v3
    """

    __slots__ = (
        'id',
        'version',
        'app_id',
        'mch_id',
        'api_key',
        'paysign_key'
    )

    def __init__(self, db_model=None):
        business_model.Model.__init__(self)

        self.context['db_model'] = db_model
        if db_model:
            self._init_slot_from_model(db_model)
        self.version = mall_models.WEIXIN_PAY_V3
        self.mch_id = db_model.partner_id
        self.api_key = db_model.partner_key

    @staticmethod
    @param_required(['app_id', 'mch_id', 'api_key', 'paysign_key'])
    def create(args):
        config = mall_models.UserWeixinPayOrderConfig.create(
            owner=corp_id,
            app_id=args.get('app_id', '').strip(),
            pay_version=WEIXIN_PAY_V3,
            partner_id=args.get('mch_id', '').strip(),
            partner_key=args.get('api_key', '').strip(),
            paysign_key=args.get('paysign_key', ''),
        )

        return WeixinPayV2Config(config)
