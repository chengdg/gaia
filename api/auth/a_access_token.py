# -*- coding: utf-8 -*-
"""@package api.auth.access_token
服务演示数据

"""
#import copy
#from datetime import datetime
#import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.auth.access_token import AccessToken
#import json

#from db.account import models as account_models

class AAccessToken(api_resource.ApiResource):
	"""
	优惠券
	"""
	app = 'auth'
	resource = 'access_token'

	@param_required(['app_key', 'app_secret'])
	def get(args):
		"""
		获取access token
		"""
		# 验证app_key和app_secret

		# 生成access token
		access_token = AccessToken.generate(args)
		if access_token:
			return {
				"access_token": access_token.access_token,
				"expire_time": access_token.expire_time,
				#"app_key": access_token.app.app_key
			}
		else:
			return 500,{}
