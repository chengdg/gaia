# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models

from db.member import models as member_models
from db.account import models as account_models
from db.mall import promotion_models

from business.mall.config.integral_strategy import IntegralStrategy


class MallConfigFactory(business_model.Service):
	def create_default_integral_strategy(self):
		"""
		创建默认的IntegralStrategy对象
		"""
		integral_strategy_settings = member_models.IntegralStrategySettings.create(
			webapp_id=self.corp.webapp_id
		)
		return IntegralStrategy(integral_strategy_settings)

