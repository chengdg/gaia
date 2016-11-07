# -*- coding: utf-8 -*-
import json

from business import model as business_model
from business.order.delivery_item import DeliveryItem
from db.mall import models as mall_models
from gaia_conf import TOPIC
from bdem import msgutil
from datetime import datetime, timedelta


class OrderExportJob(business_model.Model):
	"""
	订单导出任务
	"""

	__slots__ = (
		'id',
		'corp_id',
		'count',
		'processed_count'
	)

	def __init__(self, db_model):
		business_model.Model.__init__(self)
		self.corp_id = db_model.woid
		self.id = db_model.woid
		self.processed_count = db_model.processed_count
		self.count = db_model.count
		self.context['db_model'] = db_model

	@staticmethod
	def create(args):
		db_model = mall_models.ExportJob.objects.create(
			woid=args['corp_id'],
			type=args['type'],
			status=0,
			param=json.dumps(args['filter']),
			created_at=datetime.now(),
			processed_count=0,
			count=0,
		)

		return OrderExportJob(db_model)
