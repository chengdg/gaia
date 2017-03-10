# -*- coding: utf-8 -*-

from business.export.export_job import ExportJob
from business import model as business_model
from db.mall import models as mall_models

class ExportJobRepository(business_model.Service):
	def get_export_job_by_type(self, type):
		db_type = mall_models.WORD2EXPORT_JOB_TYPE[type]

		db_model = mall_models.ExportJob.select().dj_where(woid=self.corp.id, type=db_type, is_download=False).order_by(mall_models.ExportJob.id.desc()).first()

		return ExportJob(db_model)