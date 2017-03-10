# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.export.export_job import ExportJob


class AExportJob(api_resource.ApiResource):
	app = 'export'
	resource = 'export_job'

	@param_required(['corp_id', 'type'])
	def put(args):
		filters = args.get('filters', '')

		corp = args['corp']

		export_job = ExportJob.create({
			'corp_id': corp.id,
			'type': args['type'],
			'filters': filters
		})

		return {
			"job_id": export_job.id
		}

	@param_required(['corp', 'type'])
	def get(args):
		corp = args['corp']
		type = args['type']

		job = corp.export_job_repository.get_export_job_by_type(type)

		if job.is_valid:
			return {
				'is_existent': True,
				'is_finished': job.is_finished,
				'percentage': job.percentage,
				'file_path': job.file_path
			}

		else:
			return {
				'is_existent': False,
				'is_finished': '',
				'percentage': 0,
				'file_path': ''

			}

	@param_required(['corp', 'type'])
	def delete(args):
		corp = args['corp']
		type = args['type']
		job = corp.export_job_repository.get_export_job_by_type(type)
		job.update({"is_download":True})
		return {}
