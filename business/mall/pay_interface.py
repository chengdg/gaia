# -*- coding: utf-8 -*-
import json

from eaglet.core import watchdog
from eaglet.decorator import param_required

from business import model as business_model
from db.account import models as account_model
from db.mall import models as mall_models


class PayInterface(business_model.Model):
	"""
	支付信息
	"""

	__slots__ = (
		'id',
		'owner_id',
		'type',
		'description',
		'is_active',
		'related_config_id',
		'name',
		'should_create_related_config'
	)

	def __init__(self, db_model=None):
		business_model.Model.__init__(self)

		self.context['db_model'] = db_model
		if db_model:
			self._init_slot_from_model(db_model)

	@staticmethod
	@param_required(['owner_id'])
	def from_owner_id(args):
		owner_id = args['owner_id']

		pay_interface_db_models = mall_models.PayInterface.select().dj_where(owner_id=owner_id)

		exist_pay_interface_types = [p.type for p in pay_interface_db_models]

		for pay_type in mall_models.VALID_PAY_INTERFACES:
			if pay_type not in exist_pay_interface_types:
				mall_models.PayInterface.create(
					owner=owner_id,
					type=pay_type,
					description='',
					is_active=False
				)

		pay_interface_db_models = mall_models.PayInterface.select().dj_where(
										owner=owner_id,
										type__not_in=[mall_models.PAY_INTERFACE_WEIZOOM_COIN]
									)

		pay_interfaces = [PayInterface(db_model) for db_model in pay_interface_db_models]
		for pay_interface in pay_interfaces:
			pay_interface.name = mall_models.PAYTYPE2NAME[pay_interface.type]
			if pay_interface.type in [mall_models.PAY_INTERFACE_WEIXIN_PAY,
									  mall_models.PAY_INTERFACE_ALIPAY] and pay_interface.related_config_id == 0:
				pay_interface.should_create_related_config = True
			else:
				pay_interface.should_create_related_config = False
		return pay_interfaces

	@property
	def configs(self):
		# 获取接口对应的配置项
		if self.type == mall_models.PAY_INTERFACE_WEIXIN_PAY and self.related_config_id != 0:
			related_config = mall_models.UserWeixinPayOrderConfig.select().dj_where(
				owner=self.owner_id, id=self.related_config_id).first()

			if related_config.pay_version == 0:
				configs = {
						"pay_version": "v2",
						"app_id": related_config.app_id,
						"partner_id": related_config.partner_id,
						"partner_key": related_config.partner_key,
						"paysign_key": related_config.paysign_key
				}
				# [{
				# 	"name": u"接口版本", "value": "v2"
				# }, {
				# 	"name": u"AppID", "value": related_config.app_id
				# }, {
				# 	"name": u"合作商户ID", "value": related_config.partner_id
				# }, {
				# 	"name": u"合作商户密钥", "value": related_config.partner_key
				# }, {
				# 	"name": u"支付专用签名串", "value": related_config.paysign_key
				# }]
			else:
				configs = {
					"pay_version": "v3",
					"app_id": related_config.app_id,
					"partner_id": related_config.partner_id,
					"partner_key": related_config.partner_key
				}
				# [{
				# 	"name": u"接口版本", "value": "v3"
				# }, {
				# 	"name": u"AppID", "value": related_config.app_id
				# }, {
				# 	"name": u"商户号MCHID", "value": related_config.partner_id
				# }, {
				# 	"name": u"APIKEY密钥", "value": related_config.partner_key
				# }]
			self.context['configs'] = configs
			return self.context['configs']

		elif self.type == mall_models.PAY_INTERFACE_ALIPAY and self.related_config_id != 0:
			related_config = mall_models.UserAlipayOrderConfig.select().dj_where(
				owner=self.owner_id,
				id=self.related_config_id).first()
			configs = {
				"pay_version": 'v2' if related_config.pay_version == '0' else 'v5',
				"partner_id": related_config.partner,
				"key": related_config.key,
				"ali_public_key": related_config.ali_public_key,
				"private_key": related_config.private_key,
				"seller_email": related_config.seller_email
			}
			# [
			# 	{
			# 		"name": u"接口版本", "value": 'v2' if related_config.pay_version == '0' else 'v5'
			# 	},
			# 	{
			# 		"name": u"合作者身份ID", "value": related_config.partner
			# 	}, {
			# 		"name": u"交易安全检验码", "value": related_config.key
			# 	}, {
			# 		"name": u"支付宝公钥", "value": related_config.ali_public_key
			# 	}, {
			# 		"name": u"商户私钥", "value": related_config.private_key
			# 	}, {
			# 		"name": u"邮箱", "value": related_config.seller_email
			# 	}]
			self.context['configs'] = configs
			return self.context['configs']
		else:
			self.context['configs'] = None
			return self.context['configs']

	@staticmethod
	@param_required(['id'])
	def from_id(args):
		id = args['id']
		model = mall_models.PayInterface.select().dj_where(id=id).first()
		return PayInterface(model)

	def update_status(self, is_enable):
		mall_models.PayInterface.update(is_active=is_enable).dj_where(id=self.id).execute()