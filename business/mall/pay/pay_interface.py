# -*- coding: utf-8 -*-

from eaglet.core import watchdog
from eaglet.decorator import param_required

from business import model as business_model
from db.mall import models as mall_models

from business.mall.corporation_factory import CorporationFactory

NEED_RELATED_CONFIG_TYPES = [mall_models.PAY_INTERFACE_WEIXIN_PAY, mall_models.PAY_INTERFACE_ALIPAY]

class PayInterface(business_model.Model):
	"""
	支付接口
	"""
	__slots__ = (
		'id',
		'type',
		'is_active',
		'name',
		'related_config_id'
	)

	def __init__(self, db_model=None):
		business_model.Model.__init__(self)

		self.context['db_model'] = db_model
		if db_model:
			self._init_slot_from_model(db_model)

		self.name = mall_models.PAYTYPE2NAME[self.type]

	@property
	def str_type(self):
		return mall_models.PAYTYPE2STR[self.type]

	def set_config(self, config):
		"""
		设置支付接口的具体配置
		"""
		mall_models.PayInterface.update(related_config_id=config.id).dj_where(id=self.id).execute()

	def is_weixin_pay(self):
		"""
		判断是否是微信支付
		"""
		return self.type == mall_models.PAY_INTERFACE_WEIXIN_PAY

	def is_ali_pay(self):
		"""
		判断是否是支付宝支付
		"""
		return self.type == mall_models.PAY_INTERFACE_ALIPAY

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
