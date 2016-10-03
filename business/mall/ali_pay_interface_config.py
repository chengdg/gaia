# -*- coding: utf-8 -*-

from eaglet.core import watchdog
from eaglet.decorator import param_required

from business import model as business_model
from db.mall import models as mall_models

from business.mall.corporation_factory import CorporationFactory


class AliPayConfig(business_model.Model):
    """
    支付宝支付配置信息
    """
    __slots__ = (
        'id',
        'partner',
        'key',
        'private_key',
        'ali_public_key',
        'seller_email',
        'pay_version'
    )

    def __init__(self, db_model=None):
        business_model.Model.__init__(self)

        self.context['db_model'] = db_model
        if db_model:
            self._init_slot_from_model(db_model)

    @staticmethod
    @param_required(['partner', 'key', 'private_key', 'ali_public_key', 'seller_email'])
    def create(args):
        config = mall_models.UserAlipayOrderConfig.create(
            owner=CorporationFactory.get().id,
            partner=args.get('partner', ''),
            key=args.get('key', ''),
            private_key=args.get('private_key', ''),
            ali_public_key=args.get('ali_public_key', ''),
            seller_email=args.get('seller_email', ''),
            pay_version=mall_models.ALI_PAY_V5
        )
        return AliPayConfig(config)