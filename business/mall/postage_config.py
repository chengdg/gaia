# -*- coding: utf-8 -*-
import json

from eaglet.core import watchdog
from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource

from business import model as business_model
from db.account import models as account_model
from db.mall import models as mall_models


class PostageConfig(business_model.Model):
	"""
	订单
	"""

	__slots__ = (
		'id',
		'name',
		'first_weight', #首重
		'first_weight_price', #首重价格
		'is_enable_added_weight', #是否启用续重
		'added_weight', #续重
		'added_weight_price', # 续重价格
		'is_used',# 是否启用
		'is_system_level_config', # 是否是系统创建的不可修改的配置
		
		'is_enable_special_config', # 是否启用特殊地区运费机制
		'special_configs', #特殊地区运费集合

		'is_enable_free_config', # 是否启用包邮机制		
		'free_configs' #包邮配置集合
	)

	def __init__(self, model=None):
		business_model.Model.__init__(self)

		if model:
			self._init_slot_from_model(model)
		self.special_configs = []
		self.free_configs = []

	def add_special_config(self, special_config):
		"""
		添加特殊地区运费配置
		"""
		self.special_configs.append(special_config)

	def add_free_config(self, free_config):
		"""
		添加包邮运费配置
		"""
		self.free_configs.append(free_config)

	@staticmethod
	@param_required(['id', 'owner_id'])
	def from_id(args):
		id = args['id']
		owner_id = args['owner_id']

		postage_config = mall_models.PostageConfig.select().dj_where(id=id, owner_id=owner_id, is_deleted=False).first()

		special_configs = map(lambda x: x.to_dict(),
		                      mall_models.SpecialPostageConfig.select().dj_where(postage_config=postage_config))

		free_configs = map(lambda x: x.to_dict(),
		                   mall_models.FreePostageConfig.select().dj_where(postage_config=postage_config))

		return PostageConfig(owner_id, id, special_configs, free_configs, postage_config.to_dict())

	@staticmethod
	@param_required([])
	def create(args):
		"""

		 创建运费模板

		 Method: POST

		 @param name 运费模板名
		 @param firstWeight  默认运费的首重
		 @param firstWeightPrice  默认运费的首重价格
		 @param addedWeight  默认运费的续重
		 @param addedWeightPrice  默认运费的续重价格
		 @param isEnableSpecialConfig 是否启用“特殊地区运费”
		 @param specialConfigs 特殊地区运费信息的json字符串
		 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.c}
				 [{
						 destination: [上海, 北京, ...],
						 firstWeight: 1.0,
						 firstWeightPrice: 5.5,
						 addedWeight: 0.5,
						 addedWeightPrice: 3.0
				 }, {
						 ......
				 }]
		 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		 @param isEnableFreeConfig 是否启用“特殊地区包邮条件”
		 @param freeConfigs 特殊地区包邮条件的json字符串
		 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.c}
				 [{
						 destination: [上海, 北京, ...],
						 condition: 'count', //count代表数量，price代表价格
						 value: 3 //condition条件需要满足的值
				 }, {
						 ......
				 }]
		 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		 """
		name = args['name']
		first_weight = args['first_weight']
		first_weight_price = args['first_weight_price']
		added_weight = args['added_weight']
		added_weight_price = args['added_weight_price']
		is_enable_special_config = args['is_enable_special_config']
		special_configs = args['special_configs']
		is_enable_free_config = args['is_enable_free_config']
		free_configs = args['free_configs']
		owner_id = args['owner_id']

		# 更新当前被使用的postage config状态
		mall_models.PostageConfig.update(is_used=False).dj_where(owner=owner_id, is_used=True).execute()

		postage_config = mall_models.PostageConfig.create(
			owner=owner_id,
			name=name,
			first_weight=first_weight,
			first_weight_price=first_weight_price,
			added_weight=added_weight,
			added_weight_price=added_weight_price,
			is_enable_special_config=is_enable_special_config,
			is_enable_free_config=is_enable_free_config,
			is_used=True
		)

		if is_enable_special_config:

			for special_config in special_configs:
				special_config = mall_models.SpecialPostageConfig.create(
					owner=owner_id,
					postage_config=postage_config,
					destination=','.join(special_config.get('destination', [])),
					first_weight=round(float(special_config.get('first_weight', 0.0)), 1),
					first_weight_price=round(float(special_config.get('first_weight_price', 0.0)), 2),
					added_weight=round(float(special_config.get('added_weight', 0.0)), 1),
					added_weight_price=round(float(special_config.get('added_weight_price', 0.0)), 2)
				)
		if is_enable_free_config:
			for free_config in free_configs:
				free_config = mall_models.FreePostageConfig.objects.create(
					owner=owner_id,
					postage_config=postage_config,
					destination=','.join(free_config.get('destination', [])),
					condition=free_config.get('condition', 'count'),
					condition_value=free_config.get('value', 1)
				)

	@staticmethod
	@param_required([])
	def delete(args):
		mall_models.PostageConfig.update(is_used=False, is_deleted=True).dj_where(owner_id=args['owner_id'],
		                                                                          id=args['id']).execute()
		mall_models.PostageConfig.update(is_used=True).dj_where(owner_id=args['owner_id'],
		                                                        is_system_level_config=True).execute()

	@staticmethod
	@param_required([])
	def modify(args):
		owner_id = args['owner_id']

		name = args['name']
		first_weight = args['first_weight']
		first_weight_price = args['first_weight_price']
		added_weight = args['added_weight']
		added_weight_price = args['added_weight_price']
		is_enable_special_config = args.get('is_enable_special_config',False)
		special_configs = args['specialConfigs']
		is_enable_free_config = args['is_enable_free_config']
		free_configs = args['free_configs']
		mall_models.PostageConfig.update(
			name=name,
			first_weight=first_weight,
			first_weight_price=first_weight_price,
			added_weight=added_weight,
			added_weight_price=added_weight_price,
			is_enable_special_config=is_enable_special_config,
			is_enable_free_config=is_enable_free_config
		).dj_where(id=id).execute()

		# 更新special config
		if is_enable_special_config:
			special_config_ids = set([config['id'] for config in special_configs])
			existed_special_config_ids = set(
				[config.id
				 for config in
				 mall_models.SpecialPostageConfig.select().dj_where(postage_config_id=id)])
			for special_config in special_configs:
				config_id = special_config['id']
				if config_id < 0:
					special_config = mall_models.SpecialPostageConfig.create(
						owner_id=owner_id,
						postage_config_id=id,
						destination=','.join(special_config.get('destination', [])),
						first_weight=special_config.get('first_weight', 0.0),
						first_weight_price=special_config.get('first_weight_price', 0.0),
						added_weight=special_config.get('added_weight', 0.0),
						added_weight_price=special_config.get('added_weight_price', 0.0)
					)
				else:
					mall_models.SpecialPostageConfig.update(
						destination=','.join(special_config.get('destination', [])),
						first_weight=special_config.get('first_weight', 0.0),
						first_weight_price=special_config.get('first_weight_price', 0.0),
						added_weight=special_config.get('added_weight', 0.0),
						added_weight_price=special_config.get('added_weight_price', 0.0)
					).dj_where(id=config_id).execute()

			ids_to_be_delete = existed_special_config_ids - special_config_ids
			mall_models.SpecialPostageConfig.delete().dj_where(id__in=ids_to_be_delete).execute()

		# 更新free config
		if is_enable_free_config:
			free_config_ids = set([config['id'] for config in free_configs])
			existed_free_config_ids = set(
				[config.id
				 for config in
				 mall_models.FreePostageConfig.select().dj_where(
					 postage_config_id=id)])
			for free_config in free_configs:
				config_id = free_config['id']
				if config_id < 0:
					free_config = mall_models.FreePostageConfig.create(
						owner_id=owner_id,
						postage_config_id=id,
						destination=','.join(free_config.get('destination', [])),
						condition=free_config.get('condition', 'count'),
						condition_value=free_config.get('value', 1)
					)
				else:
					mall_models.FreePostageConfig.update(
						destination=','.join(free_config.get('destination', [])),
						condition=free_config.get('condition', 'count'),
						condition_value=free_config.get('value', 1).dj_where(id=config_id).execute()
					)
			ids_to_be_delete = existed_free_config_ids - free_config_ids
			mall_models.FreePostageConfig.delete().dj_where(id__in=ids_to_be_delete).execute()
