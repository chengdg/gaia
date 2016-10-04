# -*- coding: utf-8 -*-

from eaglet.core import watchdog
from eaglet.decorator import param_required

from business import model as business_model
from db.mall import models as mall_models

from business.mall.corporation_factory import CorporationFactory
from business.decorator import cached_context_property
from business.mall.pay.ali_pay_config import AliPayConfig

class AliPayInterface(business_model.Model):
	"""
	支付宝的支付接口
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
		加载支付宝的具体配置
		"""
		config = self.context.get('__config', None)
		if not config:
			config_id = self.context['db_model'].related_config_id
			config = mall_models.UserAlipayOrderConfig.select().dj_where(id=config_id).get()
			self.context['__config'] = config

		return config

	@cached_context_property
	def version(self):
		config = self.__load_related_config()
		return 'v5' if config.pay_version == mall_models.ALI_PAY_V5 else 'v2'

	def is_v5_alipay(self):
		return self.version == 'v5'

	def is_v2_alipay(self):
		return self.version == 'v2'

	@cached_context_property
	def config(self):
		config = self.__load_related_config()
		return AliPayConfig(config)

	def update_config(self, args):
		"""
		更新微信支付具体配置
		"""
		corp_id = CorporationFactory.get().id

		version = args['version']
		if version == 'v2':
			version = mall_models.ALI_PAY_V2
		else:
			version = mall_models.ALI_PAY_V5
		
		mall_models.UserAlipayOrderConfig.update(
			pay_version=version,
			partner=args.get('partner', ''),
			key=args.get('key', ''),
			private_key=args.get('private_key', ''),
			ali_public_key=args.get('ali_public_key', ''),
			seller_email=args.get('seller_email', '')
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
