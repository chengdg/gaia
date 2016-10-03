# -*- coding: utf-8 -*-

from eaglet.core import watchdog
from eaglet.decorator import param_required

from business import model as business_model
from db.mall import models as mall_models

from business.mall.corporation_factory import CorporationFactory
from business.decorator import cached_context_property
from business.mall.weixin_pay_interface_v2_config import WeixinPayV2Config
from business.mall.weixin_pay_interface_v3_config import WeixinPayV3Config

class WeixinPayInterface(business_model.Model):
	"""
	微信支付的支付接口
	"""
	__slots__ = (
		'id',
		'type',
		'is_active',
		'name'
	)

	def __init__(self, db_model=None):
		business_model.Model.__init__(self)

		self.context['db_model'] = db_model
		if db_model:
			self._init_slot_from_model(db_model)

		self.name = mall_models.PAYTYPE2NAME[self.type]

	def __load_related_config(self):
		"""
		加载微信支付的具体配置
		"""
		config = self.context.get('__config', None)
		if not config:
			config_id = self.context['db_model'].related_config_id
			config = mall_models.UserWeixinPayOrderConfig.select().dj_where(id=config_id).get()
			self.context['__config'] = config

		return config

	@cached_context_property
	def version(self):
		config = self.__load_related_config()
		return 'v2' if config.pay_version == mall_models.WEIXIN_PAY_V2 else 'v3'

	def is_v2_weixin_pay(self):
		return self.version == 'v2'

	def is_v3_weixin_pay(self):
		return self.version == 'v3'

	@cached_context_property
	def config(self):
		config = self.__load_related_config()
		if config.pay_version == mall_models.WEIXIN_PAY_V2:
			return WeixinPayV2Config(config)
		else:
			return WeixinPayV3Config(config)

	def update_config(self, args):
		"""
		更新微信支付具体配置
		"""
		corp_id = CorporationFactory.get().id
		version = args.get('pay_version', 'v2')
		if version == 'v2':
			version = mall_models.WEIXIN_PAY_V2
		else:
			version = mall_models.WEIXIN_PAY_V3

		if args.get('pay_version', 'v2') == 'v2':
			#更新微信支付v2配置
			mall_models.UserWeixinPayOrderConfig.update(
				app_id=args.get('app_id', '').strip(),
				pay_version=version,
				partner_id=args.get('partner_id', '').strip(),
				partner_key=args.get('partner_key', '').strip(),
				paysign_key=args.get('paysign_key', '').strip(),
			).dj_where(owner=corp_id).execute()
		else:
			#更新微信支付v3配置

			mall_models.UserWeixinPayOrderConfig.update(
				app_id=args.get('app_id', '').strip(),
				pay_version=version,
				partner_id=args.get('mch_id', '').strip(),
				partner_key=args.get('api_key', '').strip(),
				paysign_key=args.get('paysign_key', ''),
			).dj_where(owner=corp_id).execute()

	def enable(self):
		"""
		启用支付接口
		"""
		corp_id = CorporationFactory.get().id
		mall_models.PayInterface.update(is_active=True).dj_where(owner_id=corp_id, id=self.id).execute()

	def disable(self):
		"""
		禁用支付接口
		"""
		corp_id = CorporationFactory.get().id
		mall_models.PayInterface.update(is_active=False).dj_where(owner_id=corp_id, id=self.id).execute()
