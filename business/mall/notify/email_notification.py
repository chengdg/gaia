# -*- coding: utf-8 -*-

from eaglet.decorator import param_required

from business import model as business_model
from db.mall import models as mall_models

from business.mall.corporation_factory import CorporationFactory


class EmailNotification(business_model.Model):
	"""
	邮件通知
	"""
	__slots__ = (
		'id',
		'email_addresses',  #收件人地址，'|'分割
		'black_member_ids',  #需要过滤的会员id，'|'分割，会员id
		'type',
		'is_active',
		'created_at'  # 添加时间
	)

	AFTER_CREATE_ORDER = mall_models.PLACE_ORDER  # 下单后
	AFTER_PAY_ORDER = mall_models.PAY_ORDER  # 付款后
	AFTER_SHIP_ORDER = mall_models.SHIP_ORDER  # 发货后
	AFTER_FINISH_ORDER = mall_models.SUCCESSED_ORDER  # 完成订单后
	AFTER_CANCEL_ORDER = mall_models.CANCEL_ORDER  # 取消订单后

	def __init__(self, db_model=None):
		business_model.Model.__init__(self)

		if db_model:
			self._init_slot_from_model(db_model)

			if db_model.status == mall_models.PLACE_ORDER:
				self.type = 'after_create_order'
			elif db_model.status == mall_models.PAY_ORDER:
				self.type = 'after_pay_order'
			elif db_model.status == mall_models.SHIP_ORDER:
				self.type = 'after_ship_order'
			elif db_model.status == mall_models.SUCCESSED_ORDER:
				self.type = 'after_finish_order'
			elif db_model.status == mall_models.CANCEL_ORDER:
				self.type = 'after_cancel_order'
			else:
				self.type = 'unknown'

			self.email_addresses = [] if len(db_model.emails) == 0 else db_model.emails.split('|')
			self.black_member_ids = [] if len(db_model.black_member_ids) == 0 else db_model.black_member_ids.split('|')

	def enable(self):
		"""
		启用
		"""
		self.is_active = True
		mall_models.UserOrderNotifySettings.update(is_active=True).dj_where(id=self.id).execute()

	def disable(self):
		"""
		禁用
		"""
		self.is_active = False
		mall_models.UserOrderNotifySettings.update(is_active=False).dj_where(id=self.id).execute()

	def update(self, email_addresses, black_member_ids):
		"""
		"""
		email_addresses = '|'.join(email_addresses)
		black_member_ids = '|'.join(black_member_ids)

		corp_id = CorporationFactory.get().id
		mall_models.UserOrderNotifySettings.update(emails=email_addresses, black_member_ids=black_member_ids).dj_where(user_id=corp_id, id=self.id).execute()
