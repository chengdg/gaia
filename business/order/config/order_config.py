# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models

from db.member import models as member_models
from db.account import models as account_models
from db.weixin import models as weixin_models
from db.mall import promotion_models
from business.mall.corporation_factory import CorporationFactory


class OrderConfig(business_model.Model):
	"""
	订单设置
	"""
	__slots__ = (
		'order_expired_day',
		"is_share_page",
		"background_image",
		"share_image",
		"share_describe",
		"news_id",
		"material_id",
		"title"
	)

	def __init__(self, config_model=None, share_config_model=None, news_model=None):
		business_model.Model.__init__(self)

		self.context['db_model'] = {
			'config_model': config_model,
			'share_config_model': share_config_model,
			'news_model': news_model
		}
		if config_model:
			self.order_expired_day = config_model.order_expired_day
		if share_config_model:
			self.is_share_page = share_config_model.is_share_page
			self.background_image = share_config_model.background_image
			self.share_image = share_config_model.share_image
			self.share_describe = share_config_model.share_describe
			self.material_id = share_config_model.material_id
		if news_model:
			self.title = news_model.title

	def update(self, update_params):
		"""
		更新订单设置
		"""
		corp = CorporationFactory.get()
		self.order_expired_day = update_params['order_expired_day']
		self.is_share_page = update_params['is_share_page']
		if update_params['is_share_page']:
			self.background_image = update_params['background_image']
			self.share_image = update_params['share_image']
			self.share_describe = update_params['share_describe']

			photo_message = weixin_models.News.select().dj_where(
				material_id=update_params['material_id']).first()
			if photo_message:
				self.news_id = photo_message.id
				self.material_id = photo_message.material_id
				self.title = photo_message.title
			else:
				self.material_id = None
				self.title = None
		self.__save()

	def __save(self):
		"""
		持久化修改的数据
		@return:
		"""
		db_config_model = self.context['db_model']['config_model']
		db_share_config_model = self.context['db_model']['share_config_model']
		if db_config_model:
			db_config_model.order_expired_day = self.order_expired_day
			db_config_model.save()
		if db_share_config_model:
			db_share_config_model.is_share_page = self.is_share_page
			if self.is_share_page:
				db_share_config_model.background_image = self.background_image
				db_share_config_model.share_image = self.share_image
				db_share_config_model.share_describe = self.share_describe
				if self.news_id:
					db_share_config_model.news_id = self.news_id
					db_share_config_model.material_id = self.material_id
			db_share_config_model.save()