# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource

from business import model as business_model
from db.express import models as express_models
from business.mall.logistics.express_delivery_company import ExpressDeliveryCompany
from business.mall.logistics.express_delivery import ExpressDelivery

COMPANIES = [
	{
		"id": "00001",
		"name": "申通快递",
		"value": "shentong",
		"kdniao_value": "STO"
	},
	{
		"id": "00002",
		"name": "EMS",
		"value": "ems",
		"kdniao_value": "EMS"
	},
	{
		"id": "00003",
		"name": "顺丰速运",
		"value": "shunfeng",
		"kdniao_value": "SF"
	},
	{
		"id": "00004",
		"name": "圆通速递",
		"value": "yuantong",
		"kdniao_value": "YTO"
	},
	{
		"id": "00005",
		"name": "中通速递",
		"value": "zhongtong",
		"kdniao_value": "ZTO"
	},
	{
		"id": "00006",
		"name": "韵达快运",
		"value": "yunda",
		"kdniao_value": "YD"
	},
	{
		"id": "00007",
		"name": "天天快递",
		"value": "tiantian",
		"kdniao_value": "HHTT"
	},
	{
		"id": "00008",
		"name": "百世快递",
		"value": "huitongkuaidi",
		"kdniao_value": "HTKY"
	},
	{
		"id": "00009",
		"name": "全峰快递",
		"value": "quanfengkuaidi",
		"kdniao_value": "QFKD"
	},
	{
		"id": "00010",
		"name": "德邦物流",
		"value": "debangwuliu",
		"kdniao_value": "DBL"
	},
	{
		"id": "00011",
		"name": "宅急送",
		"value": "zhaijisong",
		"kdniao_value": "ZJS"
	},
	{
		"id": "00012",
		"name": "快捷速递",
		"value": "kuaijiesudi",
		"kdniao_value": "FAST"
	},
	{
		"id": "00013",
		"name": "比利时邮政",
		"value": "bpost",
		"kdniao_value": "BEL"
	},
	{
		"id": "00014",
		"name": "速尔快递",
		"value": "suer",
		"kdniao_value": "SURE"
	},
	{
		"id": "00015",
		"name": "国通快递",
		"value": "guotongkuaidi",
		"kdniao_value": "GTO"
	},
  	{
		"id": "00016",
		"name": "如风达",
		"value": "rufengda",
		"kdniao_value": "RFD"
	},
	{
		"id": "00017",
		"name": "邮政包裹/平邮",
		"value": "youzhengguonei",
		"kdniao_value": "YZPY"
	},
	{
		"id": "00018",
		"name": "优速物流",
		"value": "youshuwuliu",
		"kdniao_value": "UC"
	},
	{
		"id": "00019",
		"name": "安能物流",
		"value": "annengwuliu",
		"kdniao_value": "ANE"
	}
]


class ExpressDeliveryRepository(business_model.Service):
	def get_companies(self):
		"""
		获取快递公司集合
		"""
		global COMPANIES
		companies = []
		for company in COMPANIES:
			companies.append(ExpressDeliveryCompany(company['id'], company['name'], company['value'], company['kdniao_value']))

		return companies

	def get_company_by_value(self, value):
		"""
		如果是系统支持的快递公司，则返回名称，否则原样返回
		@param value:
		@return:
		"""
		global COMPANIES
		for company in COMPANIES:
			if company['value'] == value:
				return ExpressDeliveryCompany(company['id'], company['name'], company['value'], company['kdniao_value']).name
		return value


	def get_company(self, id):
		"""
		根据id获取ExpressDeliveryCompany对象
		"""
		global COMPANIES
		for company in COMPANIES:
			if company['id'] == id:
				return ExpressDeliveryCompany(company['id'], company['name'], company['value'], company['kdniao_value'])

		return None

	def get_express_deliveries(self):
		"""
		获得ExpressDelivery对象集合
		"""
		models = express_models.ExpressDelivery.select().dj_where(owner_id=self.corp.id)

		express_deliveries = []
		for model in models:
			express_deliveries.append(ExpressDelivery(model))

		express_deliveries.sort(lambda x,y: cmp(y.display_index, x.display_index))
		return express_deliveries

	def get_express_delivery(self, id):
		"""
		获得指定的ExpressDelivery对象
		"""
		model = express_models.ExpressDelivery.select().dj_where(owner_id=self.corp.id, id=id).get()

		return ExpressDelivery(model)

	def delete_express_delivery(self, id):
		"""
		删除指定的ExpressDelivery对象
		"""
		express_models.ExpressDelivery.delete().dj_where(owner_id=self.corp.id, id=id).execute()		