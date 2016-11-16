# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource

from db.mall import models as mall_models
from db.member import models as member_models
from db.account import models as account_models
from db.weixin import models as weixin_models
from db.mall import promotion_models

from business import model as business_model
from business.mall.corporation_factory import CorporationFactory
from business.order.config.order_config_factory import OrderConfigFactory

from business.order.config.order_config import OrderConfig

class OrderConfigRepository(business_model.Service):

	def get_order_config(self, is_share_page=None):
		"""
		获取订单设置
		"""
		mall_config = mall_models.MallConfig.select().dj_where(owner_id=self.corp.id).first()
		share_page_config = mall_models.MallShareOrderPageConfig.select().dj_where(owner_id=self.corp.id).first()
		photo_message = None
		if share_page_config:
			photo_message = weixin_models.News.select().dj_where(material_id=share_page_config.material_id).first()

		if mall_config and share_page_config:
			return OrderConfig(mall_config, share_page_config, photo_message)
		else:
			return OrderConfigFactory.get(self.corp).create_default_order_config(mall_config, share_page_config, is_share_page)