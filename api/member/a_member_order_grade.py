# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required


class AMemberOrderGrade(api_resource.ApiResource):
	"""

	"""
	app = 'member'
	resource = 'member_order_grade'

	@param_required(['corp', 'member_id'])
	def post(args):
		member = args['corp'].member_repository.get_member_by_id(args['member_id'])

		member.auto_update_grade()

		return {}
