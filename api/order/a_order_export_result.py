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

		topic_name = TOPIC['order']
		data = {
			"corp_id": corp.id,
			"filters": filters,
			# "job_id": ""
		}

		order_export_job = OrderExportJob.create({
			'corp_id': corp.id,
			'filters': filters,
			'type': args['type']
		})

		msgutil.send_message(topic_name, "export_order", data)

		return {
			"job_id": order_export_job.id
		}

	@param_required(['corp', 'type'])
	def get(self):
		return {
			'is_finished': '',
			'percentage': 0,
			'file_url': '',
			'job_id': 0

		}

	@param_required(['corp', 'job_id'])
	def delete(self):
		pass
