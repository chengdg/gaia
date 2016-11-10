# -*- coding: utf-8 -*-
import json
from bdem import msgutil

from eaglet.core import watchdog
from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource

from business import model as business_model
from db.account import models as account_model
from db.mall import models as mall_models

from business.mall.logistics.area_postage_config import AreaPostageConfig
from business.mall.logistics.free_postage_config import FreePostageConfig
from business.mall.logistics.postage_config import PostageConfig
from gaia_conf import TOPIC


class PostageConfigRepository(business_model.Service):
	def get_postage_configs(self):
		"""
		获得corp中所有的PostageConfig对象集合
		"""
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
			id2config[config_id].add_special_config(AreaPostageConfig(special_config_model))

		for free_config_model in mall_models.FreePostageConfig.select().dj_where(postage_config_id__in=free_config_enabled_config_ids):
			config_id = free_config_model.postage_config_id
			id2config[config_id].add_free_config(FreePostageConfig(free_config_model))

		return datas

	def get_postage_config(self, postage_config_id):
		"""
		获得指定的postage config
		"""
		postage_config_model = mall_models.PostageConfig.select().dj_where(owner_id=self.corp.id, id=postage_config_id).get()

		config = PostageConfig(postage_config_model)
		return config

	def get_corp_used_postage_config(self):
		"""
		获取正在使用运费模板
		"""
		postage_config_model = mall_models.PostageConfig.select().dj_where(owner_id=self.corp.id, is_used=True).first()

		config = PostageConfig(postage_config_model)
		return config

	def delete_postage_config(self, postage_config_id):
		"""
		删除指定的postage config
		"""
		mall_models.PostageConfig.update(is_deleted=True).dj_where(id=postage_config_id, owner_id=self.corp.id).execute()
		msgutil.send_message(
			TOPIC['product'],
			'postage_config_updated',
			{'corp_id': self.corp.id, 'postage_config_id': postage_config_id})


	def get_supplier_used_postage_config(self, supplier_id):
		"""
		获取正在使用运费模板
		"""
		postage_config_model = mall_models.PostageConfig.select().dj_where(supplier_id=supplier_id, is_used=True,
																		   owner_id=self.corp.id).first()

		config = PostageConfig(postage_config_model)
		return config
