# -*- coding: utf-8 -*-
import json

from eaglet.core import watchdog
from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource

from business import model as business_model
from db.account import models as account_model
from db.mall import models as mall_models

from business.mall.special_postage_config import SpecialPostageConfig
from business.mall.free_postage_config import FreePostageConfig
from business.mall.postage_config import PostageConfig

class PostageConfigRepository(business_model.Service):
	def get_postage_configs(self):
		postage_config_models = mall_models.PostageConfig.select().dj_where(owner_id=self.corp.id, is_deleted=False)

		datas = []
		special_config_enabled_config_ids = []
		free_config_enabled_config_ids = []
		id2config = {}
		for config_model in postage_config_models:
			config = PostageConfig(config_model)
			id2config[config.id] = config
			if config.is_enable_special_config:
				special_config_enabled_config_ids.append(config.id)
			if config.is_enable_free_config:
				free_config_enabled_config_ids.append(config.id)
			datas.append(config)

		for special_config_model in mall_models.SpecialPostageConfig.select().dj_where(postage_config_id__in=special_config_enabled_config_ids):
			config_id = special_config_model.postage_config_id
			id2config[config_id].add_special_config(SpecialPostageConfig(special_config_model))

		for free_config_model in mall_models.FreePostageConfig.select().dj_where(postage_config_id__in=free_config_enabled_config_ids):
			config_id = free_config_model.postage_config_id
			id2config[config_id].add_free_config(FreePostageConfig(free_config_model))

		return datas