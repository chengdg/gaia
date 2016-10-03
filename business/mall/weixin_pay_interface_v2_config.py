# -*- coding: utf-8 -*-

from eaglet.core import watchdog
from eaglet.decorator import param_required

from business import model as business_model
from db.mall import models as mall_models

from business.mall.corporation_factory import CorporationFactory


class WeixinPayV2Config(business_model.Model):
    """
    微信支付信息 v2
    """

    __slots__ = (
        'id',
        'version',
        'app_id',
        'partner_id',
        'partner_key',
        'paysign_key'
    )

    def __init__(self, db_model=None):
        business_model.Model.__init__(self)

        self.context['db_model'] = db_model
        if db_model:
            self._init_slot_from_model(db_model)
        self.version = mall_models.WEIXIN_PAY_V2

    @staticmethod
    @param_required(['app_id', 'partner_id', 'partner_key', 'app_secret', 'paysign_key'])
    def create(args):
        config = mall_models.UserWeixinPayOrderConfig.create(
            owner=CorporationFactory.get().id,
            app_id=args.get('app_id', '').strip(),
            app_secret=args.get('app_secret', '').strip(),
            pay_version=mall_models.WEIXIN_PAY_V2,
            partner_id=args.get('partner_id', '').strip(),
            partner_key=args.get('partner_key', '').strip(),
            paysign_key=args.get('paysign_key', '').strip(),
        )

        return WeixinPayV2Config(config)
        