# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.weixin_certificate import WeixinCertificate

class AWeixinCertificate(api_resource.ApiResource):
	app = 'mall'
	resource = 'weixin_certificate'

	@param_required(['owner_id'])
	def get(args):
		owner_id = args['owner_id']
		weixin_certificate = WeixinCertificate.from_owner_id({'owner_id': owner_id})
		cert_name = u'  (apiclient_cert.pem)' if weixin_certificate.cert_path != '' else ''
		key_name = u'  (apiclient_key.pem)' if weixin_certificate.key_path != '' else ''
		return {'cert_name': cert_name, 'key_name': key_name}


	@param_required(['owner_id', 'file_cat', 'file_path', 'up_file_path'])
	def post(args):
		"""
		@param file_cat: 文件类型（cert文件或者key文件）
		@param file_path: 文件服务器地址
		@param up_file_path: 文件又拍云地址
		@return:
		"""
		owner_id = args['owner_id']
		file_cat = args['file_cat']
		file_path = args['file_path']
		up_file_path = args['up_file_path']
		weixin_certificate = WeixinCertificate.from_owner_id({'owner_id': owner_id})
		try:
			weixin_certificate.update_weixin_certificate(file_cat, file_path, up_file_path)
			return {'msg': "upload success"}
		except:
			return {'msg': "upload failed"}

