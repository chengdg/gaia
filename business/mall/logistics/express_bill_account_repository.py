# -*- coding: utf-8 -*-
import json
from bdem import msgutil

from eaglet.core import watchdog
from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource

from business import model as business_model
from db.account import models as account_model
from db.mall import models as mall_models

from business.mall.logistics.express_bill_account import ExpressBillAccount
from gaia_conf import TOPIC

class ExpressBillAccountRepository(business_model.Service):

	def get_express_bill_account(self,express_bill_account_id):
		"""
		获得指定的电子面单账号
		"""
		express_bill_account_model = mall_models.ExpressBillAccount.select().dj_where(owner_id=self.corp.id, id=express_bill_account_id).get()

		express_bill_account = ExpressBillAccount(express_bill_account_model)
		return express_bill_account

	def delete_express_bill_account(self, express_bill_account_id):
		"""
		删除指定的电子面单账号
		"""
		mall_models.ExpressBillAccount.delete().dj_where(owner_id=self.corp.id, id=express_bill_account_id).execute()

	def get_express_bill_accounts(self):
		"""
		获取corp中所有的电子面单账号
		"""
		express_bill_account_models = mall_models.ExpressBillAccount.select().dj_where(owner_id=self.corp.id,is_deleted=False).order_by(mall_models.ExpressBillAccount.created_at)
		datas = []
		for model in express_bill_account_models:
			express_bill_account = ExpressBillAccount(model)
			datas.append(express_bill_account)
		return datas