# -*- coding: utf-8 -*-

from eaglet.core import watchdog
from eaglet.decorator import param_required

from business import model as business_model
from db.mall import models as mall_models

from business.mall.pay.pay_interface import PayInterface
from business.mall.pay.weixin_pay_interface import WeixinPayInterface
from business.mall.pay.ali_pay_interface import AliPayInterface
from business.decorator import cached_context_property
from business.mall.pay.weixin_pay_v2_config import WeixinPayV2Config
from business.mall.pay.ali_pay_config import AliPayConfig


class PayInterfaceRepository(business_model.Service):
	def __make_sure_old_pay_interface_config_exists(self, pay_interface_models):
		"""
		兼容老的数据库数据，老的数据中，对于weixin pay和alipay，存在以下情况
		pay interface存在，但相应的config不存在
		这里统一为pay interface创建默认的config
		"""
		for pay_interface_model in pay_interface_models:
			if pay_interface_model.type == mall_models.PAY_INTERFACE_WEIXIN_PAY:
				if pay_interface_model.related_config_id == 0:
					config = WeixinPayV2Config.create({
						'app_id': '',
						'partner_id': '',
						'partner_key': '',
						'app_secret': '',
						'paysign_key': ''
					})
					mall_models.PayInterface.update(related_config_id = config.id).dj_where(id=pay_interface_model.id).execute()
			elif pay_interface_model.type == mall_models.PAY_INTERFACE_ALIPAY:
				if pay_interface_model.related_config_id == 0:
					config = AliPayConfig.create({
						'partner': '',
						'key': '',
						'private_key': '',
						'ali_public_key': '',
						'seller_email': ''
					})
					mall_models.PayInterface.update(related_config_id = config.id).dj_where(id=pay_interface_model.id).execute()
			else:
				pass

	def __make_sure_all_pay_interfaces_exists(self):
		"""
		创建当前还不存在的支付接口
		TODO: 将这个操作移到command中
		"""
		pay_interface_db_models = mall_models.PayInterface.select().dj_where(owner_id=self.corp.id)
		self.__make_sure_old_pay_interface_config_exists(pay_interface_db_models)

		exist_pay_interface_types = [p.type for p in pay_interface_db_models]

		is_create_pay_interface = False
		for pay_type in mall_models.VALID_PAY_INTERFACES:
			#如果数据库中没有需要的支付接口，创建之
			if pay_type not in exist_pay_interface_types:
				pay_interface_model = mall_models.PayInterface.create(
					owner=self.corp.id,
					type=pay_type,
					description='',
					is_active=False
				)

				config = None
				if pay_type == mall_models.PAY_INTERFACE_WEIXIN_PAY:
					config = WeixinPayV2Config.create({
						'app_id': '',
						'partner_id': '',
						'partner_key': '',
						'app_secret': '',
						'paysign_key': ''
					})
				elif pay_type == mall_models.PAY_INTERFACE_ALIPAY:
					config = AliPayConfig.create({
						'partner': '',
						'key': '',
						'private_key': '',
						'ali_public_key': '',
						'seller_email': ''
					})
				else:
					config = None

				if config:
					pay_interface = PayInterface(pay_interface_model)
					pay_interface.set_config(config)
				is_create_pay_interface = True

		return is_create_pay_interface

	def get_pay_interfaces(self):
		self.__make_sure_all_pay_interfaces_exists()
		pay_interface_db_models = mall_models.PayInterface.select().dj_where(owner_id=self.corp.id)			
		pay_interface_db_models = [model for model in pay_interface_db_models if model.type != mall_models.PAY_INTERFACE_WEIZOOM_COIN]

		pay_interfaces = [PayInterface(db_model) for db_model in pay_interface_db_models]
		return pay_interfaces

	def get_active_pay_interfaces(self):
		pay_interface_db_models = mall_models.PayInterface.select().dj_where(owner_id=self.corp.id, is_active=True)
		pay_interface_db_models = [model for model in pay_interface_db_models if model.type != mall_models.PAY_INTERFACE_WEIZOOM_COIN]

		pay_interfaces = [PayInterface(db_model) for db_model in pay_interface_db_models]
		return pay_interfaces

	def get_pay_interface(self, pay_interface_id):
		"""
		获得特定的pay interface
		"""
		model = mall_models.PayInterface.select().dj_where(owner_id=self.corp.id, id=pay_interface_id).get()

		return PayInterface(model)

	def get_weixin_pay_interface(self):
		"""
		获得特定的微信支付的pay interface
		"""
		model = mall_models.PayInterface.select().dj_where(owner_id=self.corp.id, type=mall_models.PAY_INTERFACE_WEIXIN_PAY).get()

		return WeixinPayInterface(PayInterface(model))

	def get_ali_pay_interface(self):
		"""
		获得特定的支付宝的pay interface
		"""
		model = mall_models.PayInterface.select().dj_where(owner_id=self.corp.id, type=mall_models.PAY_INTERFACE_ALIPAY).get()

		return AliPayInterface(PayInterface(model))
