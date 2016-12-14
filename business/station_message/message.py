# -*- coding: utf-8 -*-
"""@package business.station_message.message
站内消息
"""
from eaglet.decorator import param_required

from business import model as business_model
from business.mall.corporation_factory import CorporationFactory
from db.station_message import models as message_models


class Message(business_model.Model):
	__slots__ = (
		'id',
		'title',
		'content',
		'file_url',
		'created_at'
	)

	def __init__(self, model):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)

	def update(self, title, content, file_url):
		"""
		更新站内消息
		"""
		message_models.Message.update(title=title, content=content, file_url=file_url).dj_where(id=self.id).execute()

	@staticmethod
	@param_required(['title', 'content', 'file_url'])
	def create(args):
		"""
		创建站内消息
		"""
		corp = CorporationFactory.get()

		model = message_models.Message.create(
			# todo: corp就是User了么？
			owner=corp,
			title=args.get('title').strip(),
			content=args.get('content').strip(),
			file_url=args.get('file_url', '').strip(),
		)
		return Message(model)
