# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.express import models as express_models
from eaglet.core import paginator

from business.mall.corporation_factory import CorporationFactory

class ExpressDelivery(business_model.Model):
	"""
	物流
	"""
	__slots__ = (
		'id',
		'name',
		'remark',
		'express_number',
		'express_value',
		'display_index'
	)

	def __init__(self, model=None):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)

	@staticmethod
	@param_required(['company_id', 'remark'])
	def create(args):
		from business.mall.logistics.express_delivery_repository import ExpressDeliveryRepository
		company = ExpressDeliveryRepository.get().get_company(args['company_id'])

		corp_id = CorporationFactory.get().id

		#确定display_index
		express_deliverys = list(express_models.ExpressDelivery.select().dj_where(owner_id=corp_id).order_by(express_models.ExpressDelivery.display_index.desc()))
		if len(express_deliverys) > 0:
			display_index = express_deliverys[0].display_index + 1
		else:
			display_index = 1

		#创建ExpressDelivery对象
		express_delivery = express_models.ExpressDelivery.create(
			owner=corp_id,
			name=company.name,
			express_number=company.company_id,
			express_value=company.value,
			display_index=display_index,
			remark=args.get('remark', ' ')
		)
		return ExpressDelivery(express_delivery)

	def update(self, company_id, remark=""):
		"""
		更新快递公司信息和备注信息
		"""
		from business.mall.logistics.express_delivery_repository import ExpressDeliveryRepository
		company = ExpressDeliveryRepository.get().get_company(company_id)

		express_models.ExpressDelivery.update(
			name=company.name,
			express_number=company.company_id,
			express_value=company.value,
			remark=remark
		).dj_where(id=self.id).execute()

	def update_display_index(self, direction):
		"""
		更新display index
		"""
		corp_id = CorporationFactory.get().id
		models = list(express_models.ExpressDelivery.select().dj_where(owner_id=corp_id))
		models.sort(lambda x,y: cmp(y.display_index, x.display_index))

		src_index = -1
		for index, model in enumerate(models):
			if model.id == self.id:
				src_index = index
				break

		if direction == 'up':
			dst_index = src_index - 1
		else:
			dst_index = src_index + 1

		#交换两个数据的display index
		src_id = models[src_index].id
		src_display_index = models[src_index].display_index
		dst_id = models[dst_index].id
		dst_display_index = models[dst_index].display_index
		express_models.ExpressDelivery.update(display_index=dst_display_index).dj_where(id=src_id).execute()
		express_models.ExpressDelivery.update(display_index=src_display_index).dj_where(id=dst_id).execute()
