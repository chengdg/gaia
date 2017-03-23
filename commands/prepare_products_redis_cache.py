# -*- coding: utf-8 -*-
import redis
from util.command import BaseCommand

from eaglet.core.db import models as eaglet_db

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
		
		# 预热分组信息
		self_accounts = account_models.UserProfile.select().dj_where(webapp_type=1)
		self_account_ids = [account.user_id for account in self_accounts]
		categories = mall_models.ProductCategory.select().dj_where(owner_id__in=self_account_ids)
		# print 'starting..... prepare..... category!'
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
		sql = """
			select p.category_id as category_id, p.product_id as product_id, a.user_id from mall_category_has_product   p
			join mall_product_category as c on c.id = p.category_id
			join account_user_profile as a on a.user_id = c.owner_id
			join product_pool as pool on pool.product_id = p.product_id and pool.woid = c.owner_id
			where a.webapp_type = 1
			and pool.status =1
			order by p.category_id, p.display_index, p.created_at desc
		"""
		db = eaglet_db.db
		cursor = db.execute_sql(sql, ())
		category_id_2_product_ids = {}
		category_id_2_owner_id = {}
		for index, row in enumerate(cursor.fetchall()):
			category_id_2_product_ids.setdefault(row[0], []).append(row[1])
			category_id_2_owner_id[row[0]] = row[2]
		# 社群所有上架商品id
		for category_id, product_ids in category_id_2_product_ids.items():
			
			corp_id = category_id_2_owner_id.get(category_id)
			
			temp_key = '{wo:%s}_{co:%s}_pids' % (corp_id, category_id)
			pipeline.delete(temp_key)
			# 该社群所有上架商品id
			if not product_ids:
				pipeline.rpush(temp_key, *['NONE'])
			else:
				pipeline.rpush(temp_key, *product_ids)
			print 'loading c_p ...%s' % category_id, corp_id
		# 社群"所有商品"分组
		for self_account_id in self_account_ids:
			print 'loading ...00%s' % self_account_id
			pools = mall_models.ProductPool.select().dj_where(status=1,
															  woid=self_account_id)\
				.order_by(mall_models.ProductPool.display_index,
						  mall_models.ProductPool.sync_at.desc(),
						  mall_models.ProductPool.id)
			temp_key = '{wo:%s}_{co:%s}_pids' % (self_account_id, 0)
			product_ids = [pool.product_id for pool in pools]
			if product_ids:
				pipeline.rpush(temp_key, *product_ids)
		
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