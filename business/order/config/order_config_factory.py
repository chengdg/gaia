# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource

from db.mall import models as mall_models
from db.member import models as member_models
from db.account import models as account_models
from db.mall import promotion_models

from business.order.config.order_config import OrderConfig
from business import model as business_model

class OrderConfigFactory(business_model.Service):

	def create_default_order_config(self, mall_config=None, share_page_config=None, is_share_page=False):
		"""
		创建默认的OrderConfig对象
		"""
		if mall_config:
			if is_share_page and not share_page_config:
				share_page_config = mall_models.MallShareOrderPageConfig.create(
					owner=self.corp.id, is_share_page=False
				)
		else:
			if is_share_page and not share_page_config:
				mall_config = mall_models.MallConfig.create(
					owner_id=self.corp.webapp_id, order_expired_day=24
				)
				share_page_config = mall_models.MallShareOrderPageConfig.create(
					owner=self.corp.id, is_share_page=False
				)
			else:
				mall_config = mall_models.MallConfig.create(
					owner_id=self.corp.webapp_id, order_expired_day=24
				)
		return OrderConfig(mall_config, share_page_config, None)