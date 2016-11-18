# -*- coding: utf-8 -*-
import json

from business import model as business_model
from business.order.delivery_item import DeliveryItem
from db.mall import models as mall_models
from gaia_conf import TOPIC
from bdem import msgutil
from datetime import datetime, timedelta
from business.mall.corporation_factory import CorporationFactory


class OrderExportJob(business_model.Model):
	"""
	订单导出任务
	"""

	__slots__ = (
		'id',
		'corp_id',
		'percentage',
		'is_finished',
		'is_valid',
		'file_path',
		'is_download'
	)

	def __init__(self, db_model):
		business_model.Model.__init__(self)
		self.context['db_model'] = db_model

		if db_model:
			self.corp_id = db_model.woid
			self.id = db_model.id
			if db_model.count == 0:
				self.percentage = 0
			else:
				self.percentage = db_model.processed_count * 100 / db_model.count
			self.is_finished = db_model.status
			self.is_valid = True
			self.context['db_model'] = db_model
			self.file_path = db_model.file_path
			self.is_download = db_model.is_download
		else:
			self.is_valid = False

	@staticmethod
	def create(args):
		db_model = mall_models.ExportJob.create(
			woid=args['corp_id'],
			type=args['type'],
			status=False,
			param=args['filters'],
			created_at=datetime.now(),
			processed_count=0,
			count=0,
		)
		topic_name = TOPIC['order']
		data = {
			"job_id": db_model.id
		}
		msgutil.send_message(topic_name, "order_export_job_created", data)

		return OrderExportJob(db_model)

	def update(self, is_download):
		corp = CorporationFactory.get()
		self.is_download = is_download
		self.__save()

	def __save(self):
		"""
		持久化修改的数据
		@return:
		"""
		db_model = self.context['db_model']
		db_model.is_download = self.is_download
		db_share_config_model.save()
