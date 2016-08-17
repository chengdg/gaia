#coding: utf8
"""
检查API检查是否有权限的decorator

"""

#import settings
#from core.jsonresponse import create_response
import logging

from business.auth.access_token import AccessToken


#class AccessTokenError(Exception):
#	pass


def access_token_required(params=None):
	"""
	检查是否有access_token
	"""
	def wrapper(function):
		def inner(data):
			if not data.has_key('access_token'):
				#raise AccessTokenError('Missing or incorrect access_token!')
				return 500, {
					'message': 'Missing or incorrect access_token!'
				}

			try:
				access_token = AccessToken.get(data)
				logging.info('access_token: {}'.format(access_token))
				if access_token:
					# 如果有access_token，在params中增加`app`项
					data['app_id'] = access_token.app.id
					return function(data)
			except Exception as e:
				logging.info("Exception: {}".format(e))
				pass
			return 500, {
				'message': 'Incorrect access_token!'
			}
		return inner
	return wrapper
