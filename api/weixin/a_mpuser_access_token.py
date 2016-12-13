# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required

from business.common.page_info import PageInfo


class AMpuserAccessToken(api_resource.ApiResource):
	"""
	微信用户token
	"""
	app = 'weixin'
	resource = 'mpuser_access_token'

	@param_required(['corp'])
	def get(args):
		corp = args['corp']

		# 获取mpuser_access_token
		access_token = corp.mpuser_access_token_repository.get_mpuser_access_token(corp.id)
		print access_token.access_token,'=================='
		return {
            'access_token': access_token
        }
