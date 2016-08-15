# -*- coding: utf-8 -*-

from eaglet.decorator import param_required

from business import model as business_model
from db.account import models as account_models


class EmailNotify(business_model.Model):
	"""
	商城配置
	"""

	__slots__ = (
		'user_id',  # 通用设置，商品销量
		'emails',  # '|'分割
		'black_member_ids',  # '|'分割，会员id
		'status',
		'is_active',
		'created_at'  # 添加时间
	)

	def __init__(self, db_model):
		business_model.Model.__init__(self)
		self._init_slot_from_model(db_model)

	@staticmethod
	@param_required(['owner_id', 'status'])
	def get(args):
		db_model = account_models.UserOrderNotifySettings.select().dj_where(user_id=args['owner_id'],
		                                                                    status=args['status']).first()
		email_notify = EmailNotify(db_model)
		email_notify.context['db_model'] = db_model
		return email_notify

	def enable(self):
		self.is_active = True
		db_model = self.context['db_model']
		db_model.is_active = True
		db_model.save()

	def disable(self):
		self.is_active = False
		db_model = self.context['db_model']
		db_model.is_active = False
		db_model.save()

	@staticmethod
	@param_required(['owner_id', 'status', 'member_ids', 'emails'])
	def modify(args):
		owner_id = args['owner_id']
		status = args['status']
		member_ids = args['member_ids']
		emails = args['emails']

		if account_models.UserOrderNotifySettings.select().dj_where(user=owner_id, status=status).count() > 0:
			account_models.UserOrderNotifySettings.select().dj_where(user=owner_id, status=status).update(emails=emails,
			                                                                                              black_member_ids=member_ids).execute()
		else:
			account_models.UserOrderNotifySettings.create(status=status, black_member_ids=member_ids, emails=emails,
			                                              user=owner_id)

	@staticmethod
	@param_required(['owner_id'])
	def get_from_owner_id(args):
		db_models = account_models.UserOrderNotifySettings.select().dj_where(user_id=args['owner_id'])
		return map(lambda x: EmailNotify(x), db_models)
