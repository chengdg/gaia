# -*- coding: utf-8 -*-
import json
from bdem import msgutil

from eaglet.core import watchdog
from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource

from business import model as business_model
from business.mall.corporation_factory import CorporationFactory
from db.account import models as account_model
from db.mall import models as mall_models

from business.decorator import cached_context_property
from business.mall.logistics.area_postage_config import AreaPostageConfig
from business.mall.logistics.free_postage_config import FreePostageConfig
from gaia_conf import TOPIC


class PostageConfig(business_model.Model):
	"""
	运费配置
	"""

	__slots__ = (
		'id',
		'name',
		'default_config', #默认运费配置
		'is_enable_added_weight', #是否启用续重
		'is_used',# 是否启用
		'is_system_level_config', # 是否是系统创建的不可修改的配置		
		'is_enable_special_config', # 是否启用特殊地区运费机制
		'_special_configs', #特殊地区运费集合
		'is_enable_free_config', # 是否启用包邮机制		
		'_free_configs' #包邮配置集合
	)

	def __init__(self, model=None):
		business_model.Model.__init__(self)

		if model:
			self._init_slot_from_model(model)
			default_config = AreaPostageConfig(model)
			self.default_config = default_config

		self._special_configs = None
		self._free_configs = None

	def add_special_config(self, area_config):
		"""
		添加特殊地区运费配置
		"""
		if not self._special_configs:
			self._special_configs = []
		self._special_configs.append(area_config)

	@property
	def special_configs(self):
		if not self._special_configs:
			self._special_configs = []
			for special_config_model in mall_models.SpecialPostageConfig.select().dj_where(postage_config_id=self.id):
				self._special_configs.append(AreaPostageConfig(special_config_model))

		return self._special_configs

	def add_free_config(self, free_config):
		"""
		添加包邮运费配置
		"""
		if not self._free_configs:
			self._free_configs = []
		self._free_configs.append(free_config)

	@property
	def free_configs(self):
		"""
		获得FreePostageConfig对象集合
		"""
		if not self._free_configs:
			self._free_configs = []
			for free_config_model in mall_models.FreePostageConfig.select().dj_where(postage_config_id=self.id):
				self._free_configs.append(FreePostageConfig(free_config_model))

		return self._free_configs

	def set_used(self):
		"""
		将当前postage config设置为"使用"
		"""
		mall_models.PostageConfig.update(is_used=False).dj_where(id__not=self.id).execute()
		mall_models.PostageConfig.update(is_used=True).dj_where(id=self.id).execute()
		msgutil.send_message(
			TOPIC['product'],
			'postage_config_set_used',
			{'corp_id': CorporationFactory.get().id, 'postage_config_id': self.id}
		)
