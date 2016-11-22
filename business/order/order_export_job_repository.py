# -*- coding: utf-8 -*-
from business.order.order_export_job import OrderExportJob
from db.mall import models as mall_models

from business import model as business_model


class OrderExportJobRepository(business_model.Service):
	def get_order_export_job_by_type(self, type):

		db_type = mall_models.WORD2EXPORT_JOB_TYPE[type]

		db_model = mall_models.ExportJob.select().dj_where(woid=self.corp.id, type=db_type, is_download=False).first()

		return OrderExportJob(db_model)