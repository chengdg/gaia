# -*- coding: utf-8 -*-
import redis
import json
from util.command import BaseCommand
import itertools

from db.mall import models as mall_models
from db.account import models as account_models

import settings


class Command(BaseCommand):
	help = "prepare product redis cache"
	args = ''
	
	def handle(self, **options):
		
		conn = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_CACHES_DB)
		
		pipeline = conn.pipeline()
		effective_products = mall_models.Product.select().dj_where(is_deleted=False)
		# 预热所有有效简单商品信息
		all_effective_simple_products_key = 'all_simple_effective_products'
		pipeline.delete(all_effective_simple_products_key)
		print 'starting prepare product redis----------------------!'
		for product in effective_products:
			if product.id % 100 == 0:
				print 'preparing--------------------------->'
			pipeline.hset(all_effective_simple_products_key, product.id, product.name)
		pipeline.execute()
		print '<-----------prepare products end------------------------!'
		
		# pipeline = conn.pipeline()
		# 预热分组信息(暂未用到)
		categories = mall_models.ProductCategory.select()
		# print 'starting..... prepare..... category!'
		# categories_keys = conn.keys("categories_*")
		# conn.delete(*categories_keys)
		# for category in categories:
		# 	temp_key = 'categories_%s' % category.owner_id
		# 	pipeline.hset(temp_key, category.id, category.name)
		# 	if category.id % 100 == 0:
		# 		print 'loading category.....'
		# pipeline.execute()
		# print '<-----------prepare categories end------------------------!'
		
		# 预热分组有什么上架商品
		
		pipeline = conn.pipeline()
		print '<-----------prepare category_products start------------------------!'
		relations = mall_models.CategoryHasProduct.select().order_by(mall_models.CategoryHasProduct.display_index)
		category_id_2_owner_id = dict([(category.id, category.owner_id) for category in categories])
		group_relations = itertools.groupby(relations, key=lambda k: k.category_id)
		corp_onshelf_product_ids = {}
		for category_id, relations in group_relations:
			corp_id = category_id_2_owner_id.get(category_id)
			temp_key = '{wo:%s}_{co:%s}_pids' % (corp_id, category_id)
			pipeline.delete(temp_key)
			if corp_onshelf_product_ids.get(corp_id) is None:
				on_shelf_product_ids = [pool.product_id for pool in
										mall_models.ProductPool.select().dj_where(woid=corp_id,
																				  status=mall_models.PP_STATUS_ON)]
				corp_onshelf_product_ids[corp_id] = on_shelf_product_ids
			pipeline.lpush(temp_key, *[relation.product_id for relation in relations])
			print 'loading c_p ...'
		pipeline.execute()
		print '<-----------prepare category_products end------------------------!'
		
		# # 预热商品的所在分组
		# print '<-----------prepare product in categories start------------------------!'
		#
		# relations = mall_models.CategoryHasProduct.select()
		# product_2_relations = itertools.groupby(relations, key=lambda k: k.product_id)
		#
		# pipeline = conn.pipeline()
		# for product_id, relations in product_2_relations:
		# 	temp_key = "product:{%s}_in_categories" % product_id
		# 	# [{}, {}]list字符串
		# 	value = [dict(id=relation.category_id,
		# 				  owner_id=relation.category.owner_id) for relation in relations]
		# 	pipeline.set(temp_key, json.dumps(value))
		# 	print '<<', product_id
		# pipeline.execute()
		# print '<-----------prepare product in categories end------------------------!'
		#
		# print '<-----------prepare products end------------------------!'
		#
		# # 预热所有商品列表分组信息
		#
		# self_accounts = account_models.UserProfile.select().dj_where(webapp_type=1)
		# print 'starting..... prepare..... category{0}!'
		# pipeline = conn.pipeline()
		# for account in self_accounts:
		# 	temp_key = '{wo:%s}_{co:%s}_products' % (account.user_id, 0)
		# 	# 所有上架商品id
		# 	on_shelf_product_ids = [pool.product_id for pool in
		# 							mall_models.ProductPool.select().dj_where(woid=account.user_id,
		# 																	  status=mall_models.PP_STATUS_ON)]
		# 	if on_shelf_product_ids:
		# 		pipeline.sadd(temp_key, *on_shelf_product_ids)
		# 	print '>>%s' % account.id
		# pipeline.execute()
		# print '<-----------prepare categories{0} end------------------------!'