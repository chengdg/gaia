# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource

from db.mall import models as mall_models
from db.member import models as member_models
from db.account import models as account_models
from db.mall import promotion_models

from business import model as business_model
from business.mall.corporation_factory import CorporationFactory
from business.mall.config.integral_strategy import IntegralStrategy
from business.mall.config.webapp_config import WebappConfig
from business.mall.config.mall_config_factory import MallConfigFactory


class MallConfigRepository(business_model.Service):
	def get_integral_strategy(self):
		"""
		获得积分策略
		"""
		# has_a_integral_strategy = promotion_models.Promotion.select().dj_where(
		# 	owner_id=args['owner_id'],
		# 	status=promotion_models.PROMOTION_STATUS_STARTED,
		# 	type=promotion_models.PROMOTION_TYPE_INTEGRAL_SALE
		# ).exists()
		integral_strategy_settings = member_models.IntegralStrategySettings.select().dj_where(webapp_id=self.corp.webapp_id).first()
		return IntegralStrategy(integral_strategy_settings)

	def get_webapp_config(self):
		"""
		获得WebappConfig对象
		"""
		mall_config = mall_models.MallConfig.select().dj_where(owner_id=self.corp.id).first()
		if not mall_config:
			return MallConfigFactory.create_default_webapp_config()
		else:
			return WebappConfig(mall_config)

