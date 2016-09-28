# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.express import models as express_models
from eaglet.core import paginator


class ExpressDelivery(business_model.Model):
	"""
	物流
	"""
	__slots__ = (
		'id',
		'owner_id',
		'name',
		'remark',
		'created_at',
		'express_number',
		'express_value',
		'display_index',
		'created_at',
	)

	def __init__(self, model=None):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)

	@staticmethod
	@param_required(['owner_id', 'id'])
	def from_id(args):
		express_delivery = express_models.ExpressDelivery.select().dj_where(owner_id=args['owner_id'], id=args['id'])
		if express_delivery:
			return ExpressDelivery(express_delivery.first())
		else:
			return None

	@staticmethod
	@param_required(['owner_id'])
	def from_owner_id(args):
		express_deliverys = express_models.ExpressDelivery.select().dj_where(owner_id=args['owner_id']).order_by(express_models.ExpressDelivery.display_index.desc())
		if 'cur_page' in args:
			pageinfo, express_deliverys = paginator.paginate(express_deliverys, args['cur_page'], args['count_per_page'], query_string=args.get('query_string', None))
			return pageinfo, [ExpressDelivery(express_delivery) for express_delivery in express_deliverys]
		else:
			return [ExpressDelivery(express_delivery).to_dict() for express_delivery in express_deliverys]

	@staticmethod
	@param_required(['db_model'])
	def from_model(args):
		return ExpressDelivery(args['db_model'])

	@staticmethod
	@param_required([])
	def create(args):
		express_deliverys = express_models.ExpressDelivery.select().dj_where(owner_id=args['owner_id']).order_by(express_models.ExpressDelivery.display_index.desc())
		if express_deliverys.count() > 0:
			display_index = express_deliverys[0].display_index + 1
		else:
			display_index = 1

		express_delivery = express_models.ExpressDelivery.create(
			owner=args['owner_id'],
			name=args['name'],
			express_number=args['express_number'],
			express_value=args['express_value'],
			display_index=display_index,
			remark=args.get('remark', ' ')
		)
		return ExpressDelivery(express_delivery)

	def update(self, name, express_number, express_value, remark=""):
		self.context['db_model'].name = name
		self.context['db_model'].express_number = express_number
		self.context['db_model'].express_value = express_value
		self.context['db_model'].remark = remark
		self.context['db_model'].save()

	def update_display_index(self, owner_id, dst_id, src_id):
		dst_id = int(dst_id)
		src_id = int(src_id)
		if dst_id == 0:
			# dst_id = 0, 将src_product的display_index设置得比第一个product的display_index大即可
			first_delivery = express_models.ExpressDelivery.select().dj_where(owner_id=owner_id).order_by(express_models.ExpressDelivery.display_index)[0]
			if first_delivery.id != src_id:
				express_models.ExpressDelivery.dj_where(id=src_id).update(display_index=first_delivery.display_index + 1).execute()
		else:
			# dst_id不为0，交换src_product, dst_product的display_index
			id2delivery = dict([(p.id, p) for p in express_models.ExpressDelivery.select().dj_where(id__in=[src_id, dst_id])])
			express_models.ExpressDelivery.update(display_index=id2delivery[dst_id].display_index).dj_where(id=src_id).execute()
			express_models.ExpressDelivery.update(display_index=id2delivery[src_id].display_index).dj_where(id=dst_id).execute()


	def delete(self):
		self.context['db_model'].delete_instance()