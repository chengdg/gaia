# -*- coding: utf-8 -*-
import json

from bdem import msgutil
from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required

from business.common.page_info import PageInfo
from business.order.order_export_job import OrderExportJob
from gaia_conf import TOPIC


class AOrderExportResult(api_resource.ApiResource):
	app = 'order'
	resource = 'order_export_result'

	@param_required(['corp', 'type'])
	def put(args):
		filters = json.loads(args.get('filters', '{}'))

		corp = args['corp']

		order_export_job = OrderExportJob.create({
			'corp_id': corp.id,
			'type': args['type'],
			'filters': args['filters']
		})

		topic_name = TOPIC['order']
		data = {
			"job_id": order_export_job.id
		}

		msgutil.send_message(topic_name, "order_export_job_created", data)

		return {
			"job_id": order_export_job.id
		}

	@param_required(['corp', 'type'])
	def get(args):
		corp = args['corp']
		type = args['type']

		job = corp.order_export_job_repository.get_order_export_job_by_type(type)

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
				'file_url': ''

			}

	@param_required(['corp', 'job_id'])
	def delete(args):
		pass
