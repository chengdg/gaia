# -*- coding: utf-8 -*-

from eaglet.core import watchdog
from eaglet.decorator import param_required

from business import model as business_model
from db.mall import models as mall_models

from business.mall.pay_interface import PayInterface
from business.decorator import cached_context_property


class PayInterfaceRepository(business_model.Service):
	"""
	支付信息
	"""
	def get_pay_interfaces(self):
		pay_interface_db_models = mall_models.PayInterface.select().dj_where(owner_id=self.corp.id)

		exist_pay_interface_types = [p.type for p in pay_interface_db_models]

		for pay_type in mall_models.VALID_PAY_INTERFACES:
			#如果数据库中没有需要的支付接口，创建之
			if pay_type not in exist_pay_interface_types:
				mall_models.PayInterface.create(
					owner=owner_id,
					type=pay_type,
					description='',
					is_active=False
				)

		pay_interface_db_models = [model for model in pay_interface_db_models if model.type != mall_models.PAY_INTERFACE_WEIZOOM_COIN]

		pay_interfaces = [PayInterface(db_model) for db_model in pay_interface_db_models]
		return pay_interfaces

	def get_active_pay_interfaces(self):
		pay_interface_db_models = mall_models.PayInterface.select().dj_where(owner_id=self.corp.id, is_active=True)
		pay_interface_db_models = [model for model in pay_interface_db_models if model.type != mall_models.PAY_INTERFACE_WEIZOOM_COIN]

		pay_interfaces = [PayInterface(db_model) for db_model in pay_interface_db_models]
		return pay_interfaces
