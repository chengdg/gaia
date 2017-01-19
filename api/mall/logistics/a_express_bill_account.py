# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.logistics.express_bill_account import ExpressBillAccount


class AExpressBillAccount(api_resource.ApiResource):
	"""
	获取电子面单账号
	"""
	app = 'mall'
	resource = 'express_bill_account'

	@param_required(['corp_id', 'id'])
	def get(args):
		corp = args['corp']

		express_bill_account = corp.express_bill_account_repository.get_express_bill_account(args['id'])

		data = {
				'id': express_bill_account.id,
				'express_name': express_bill_account.express_name,
				'customer_name': express_bill_account.customer_name,
				'customer_pwd': express_bill_account.customer_pwd,
				'logistics_number': express_bill_account.logistics_number,
				'sendsite': express_bill_account.sendsite,
				'remark': express_bill_account.remark,
			}

		return { 'express_bill_account': data }

	@param_required(['corp_id','express_name','customer_name','customer_pwd','logistics_number','sendsite','remark'])
	def put(args):

		express_bill_account = ExpressBillAccount.create({
			'express_name' : args['express_name'],
			'customer_name' : args['customer_name'],
			'customer_pwd' : args['customer_pwd'],
			'logistics_number' : args['logistics_number'],
			'sendsite' : args['sendsite'],
			'remark' : args['remark'],
		})
		return {}

	@param_required(['corp_id','id','express_name','customer_name','customer_pwd','logistics_number','sendsite','remark'])
	def post(args):
		corp = args['corp']

		express_bill_account = corp.express_bill_account_repository.get_express_bill_account(args['id'])
		express_bill_account.update(args['express_name'],args['customer_name'],args['customer_pwd'],args['logistics_number'],args['sendsite'],args['remark']
		)
		return {}

	@param_required(['corp', 'id'])
	def delete(args):
		corp = args['corp']
		express_bill_account = corp.express_bill_account_repository.delete_express_bill_account(args['id'])