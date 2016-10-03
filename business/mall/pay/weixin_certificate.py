# -*- coding: utf-8 -*-
from eaglet.decorator import param_required

from db.mall import models as mall_models
from business import model as business_model


class WeixinCertificate(business_model.Model):

	__slots__ = (
		'id',
		'owner_id',
		'cert_path',
		'up_cert_path',
		'key_path',
		'up_key_path'
	)

	def __init__(self, model):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)

	@staticmethod
	@param_required(['db_model'])
	def from_model(args):
		model = args['db_model']
		weixin_certificate = WeixinCertificate(model)
		return weixin_certificate

	@staticmethod
	@param_required(['owner_id'])
	def from_owner_id(args):
		owner_id = args['owner_id']
		weixin_certificate_model = mall_models.WxCertSettings.select().dj_where(owner_id=owner_id).first()
		if weixin_certificate_model:
			weixin_certificate = WeixinCertificate(weixin_certificate_model)
			return weixin_certificate
		else:
			weixin_certificate_model =  mall_models.WxCertSettings.create(owner=owner_id)
			weixin_certificate = WeixinCertificate(weixin_certificate_model)
			return weixin_certificate


	def update_weixin_certificate(self, file_cat, file_path, up_file_path):
		if 'cert_file' == file_cat:
			mall_models.WxCertSettings.update(
				cert_path=file_path,
				up_cert_path=up_file_path).dj_where(id=self.id).execute()
		elif 'key_file' == file_cat:
			mall_models.WxCertSettings.update(
				key_path=file_path,
				up_key_path=up_file_path).dj_where(id=self.id).execute()

