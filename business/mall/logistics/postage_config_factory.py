# -*- coding: utf-8 -*-
import json
from bdem import msgutil

from eaglet.core import watchdog
from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource

from business import model as business_model
from db.account import models as account_model
from db.mall import models as mall_models
from gaia_conf import TOPIC


class PostageConfigFactory(object):
	"""
	订单
	"""
	def __init__(self, corp):
		self.corp = corp

	@staticmethod
	def get(corp):
		return PostageConfigFactory(corp)

	def create(self, args):
		name = args['name']
		default_config = args['default_config']
		is_enable_special_config = args.get('is_enable_special_config',False)
		special_configs = args['special_configs']
		is_enable_free_config = args['is_enable_free_config']
		free_configs = args['free_configs']	
		corp_id = self.corp.id

		postage_config = mall_models.PostageConfig.create(
			owner=corp_id,
			name=name,
			first_weight=default_config['first_weight'],
			first_weight_price=default_config['first_weight_price'],
			added_weight=default_config['added_weight'],
			added_weight_price=default_config['added_weight_price'],
			is_enable_special_config=args['is_enable_special_config'],
			is_enable_free_config=args['is_enable_free_config'],
			is_used=False
		)

		if is_enable_special_config:
			for special_config in special_configs:
				special_config = mall_models.SpecialPostageConfig.create(
					owner=corp_id,
					postage_config=postage_config,
					destination=special_config.get('destinations', ''),
					first_weight=round(float(special_config.get('first_weight', 0.0)), 1),
					first_weight_price=round(float(special_config.get('first_weight_price', 0.0)), 2),
					added_weight=round(float(special_config.get('added_weight', 0.0)), 1),
					added_weight_price=round(float(special_config.get('added_weight_price', 0.0)), 2)
				)
				
		if is_enable_free_config:
			for free_config in free_configs:
				free_config = mall_models.FreePostageConfig.create(
					owner=corp_id,
					postage_config=postage_config,
					destination=free_config.get('destinations', ''),
					condition=free_config.get('condition', 'count'),
					condition_value=free_config.get('value', '')
				)
		# 发送更新缓存的消息
		msgutil.send_message(TOPIC['product'], 'postage_config_updated', {'corp_id': corp_id})
		return postage_config

	def make_sure_default_postage_config_exists(self):
		"""
		确保默认的免运费的运费配置存在
		"""
		if mall_models.PostageConfig.select().dj_where(owner_id=self.corp.id, name=u'免运费').count() == 0:
			#创建默认的“免运费”配置
			mall_models.PostageConfig.create(
				owner = self.corp.id,
				name = u'免运费',
				added_weight = "0.0",
				is_enable_added_weight = False,
				is_enable_special_config = False,
				is_enable_free_config = False,
				is_used = True,
				is_system_level_config = True
			)

	def update(self, args):
		id = args['id']
		name = args['name']
		default_config = args['default_config']
		is_enable_special_config = args['is_enable_special_config']
		special_configs = args['special_configs']
		is_enable_free_config = args['is_enable_free_config']
		free_configs = args['free_configs']	
		corp_id = self.corp.id

		mall_models.PostageConfig.update(
			name=name,
			first_weight=default_config['first_weight'],
			first_weight_price=default_config['first_weight_price'],
			added_weight=default_config['added_weight'],
			added_weight_price=default_config['added_weight_price'],
			is_enable_special_config=args['is_enable_special_config'],
			is_enable_free_config=args['is_enable_free_config']
		).dj_where(owner_id=corp_id, id=id).execute()

		mall_models.SpecialPostageConfig.delete().dj_where(owner_id=corp_id, postage_config_id=id).execute()
		if is_enable_special_config:
			for special_config in special_configs:
				special_config = mall_models.SpecialPostageConfig.create(
					owner=corp_id,
					postage_config=id,
					destination=special_config.get('destinations', ''),
					first_weight=round(float(special_config.get('first_weight', 0.0)), 1),
					first_weight_price=round(float(special_config.get('first_weight_price', 0.0)), 2),
					added_weight=round(float(special_config.get('added_weight', 0.0)), 1),
					added_weight_price=round(float(special_config.get('added_weight_price', 0.0)), 2)
				)
				
		mall_models.FreePostageConfig.delete().dj_where(owner_id=corp_id, postage_config_id=id).execute()
		if is_enable_free_config:
			for free_config in free_configs:
				free_config = mall_models.FreePostageConfig.create(
					owner=corp_id,
					postage_config=id,
					destination=free_config.get('destinations', ''),
					condition=free_config.get('condition', 'count'),
					condition_value=free_config.get('value', '')
				)
		# 发送更新缓存的消息
		msgutil.send_message(TOPIC['product'], 'postage_config_updated', {'corp_id': corp_id})