# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.logistics.express_bill_account import ExpressBillAccount


class AExpressBillAccounts(api_resource.ApiResource):
	"""
	获取电子面单账号列表
	"""
	app = 'mall'
	resource = 'express_bill_accounts'

	@param_required(['corp_id'])
	def get(args):
		corp = args['corp']

		express_bill_accounts = corp.express_bill_account_repository.get_express_bill_accounts()

		datas = []
		for express_bill_account in express_bill_accounts:
			data = {
				'id': express_bill_account.id,
				'express_name': express_bill_account.express_name,
				'customer_name': express_bill_account.customer_name,
				'customer_pwd': express_bill_account.customer_pwd,
				'logistics_number': express_bill_account.logistics_number,
				'sendsite': express_bill_account.sendsite,
				'remark': express_bill_account.remark,
			}
			datas.append(data)

		return { 'express_bill_accounts': datas }