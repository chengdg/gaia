# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy
from bdem import msgutil

from eaglet.decorator import param_required
from eaglet.core import api_resource

from db.mall import models as mall_models
from db.member import models as member_models
from db.account import models as account_models
from db.mall import promotion_models

from business.mall.config.integral_strategy import IntegralStrategy
from business.mall.config.webapp_config import WebappConfig
from business import model as business_model
from gaia_conf import TOPIC


class MallConfigFactory(business_model.Service):
	def create_default_integral_strategy(self):
		"""
		创建默认的IntegralStrategy对象
		"""
		integral_strategy_settings = member_models.IntegralStrategySettings.create(
			webapp_id=self.corp.webapp_id
		)
		return IntegralStrategy(integral_strategy_settings)

	def create_default_webapp_config(self):
		"""
		创建默认的WebappConfig对象
		"""
		mall_config = mall_models.MallConfig.create(owner=self.corp.id, order_expired_day=24)
		msgutil.send_message(TOPIC['product'], 'mall_config_created', {'corp_id': self.corp.id})
		return WebappConfig(mall_config)

