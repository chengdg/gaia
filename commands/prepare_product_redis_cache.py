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
		effective_products = mall_models.Product.select().dj_where(is_deleted=False)
		# effective_product_models = mall_models.ProductModel.select().dj_where(is_deleted=False)
		# g_p = itertools.groupby(effective_product_models, key=lambda k: k.product_id)
		# g_p_dict = dict(g_p)
			
		# 预热所有有效简单商品信息
		# all_effective_simple_products_key = 'all_simple_products_%s'
		all_effective_simple_products_key = 'all_simple_effective_products'
		print 'starting prepare product redis----------------------!'
		pipeline = conn.pipeline()
		
		for product in effective_products:
			
			# models = g_p_dict.get(product.id)
			# thumbnails_url = product.thumbnails_url
			# name = product.name
			# if models is not None and len(list(models)) > 0:
			# 	temp_list = [model.price for model in models]
			# 	display_price = min(temp_list) if temp_list else 0
			# else:
			# 	display_price = 0
			#
			# temp_data = {
			# 	"id": product.id,
			# 	"name": name,
			# 	"display_price": display_price,
			# 	"thumbnails_url": thumbnails_url,
			# }
			# 暂时不做分集合存储
			# hash_key = product.id % 10
			if product.id % 100 == 0:
				print 'prepareing--------------------------->'
			
			# pipeline.hset(all_effective_simple_products_key % hash_key, product.id, json.dumps(temp_data))
			pipeline.hset(all_effective_simple_products_key, product.id, product.name)
		print '<-----------prepare products end------------------------!'
		
		# 预热分组信息
		
		categories = mall_models.ProductCategory.select()
		print 'starting..... prepare..... category!'
		for category in categories:
			temp_key = 'categories_%s' % category.owner_id
			pipeline.hset(temp_key, category.id, category.name)
			print '>>%s' % category.id
		pipeline.execute()
		print '<-----------prepare categories end------------------------!'
		
		# 预热分组有什么上架商品
		#
		# pipeline = conn.pipeline()
		# print '<-----------prepare category_products start------------------------!'
		# relations = mall_models.CategoryHasProduct.select().order_by(mall_models.CategoryHasProduct.display_index)
		# category_id_2_owner_id = dict([(category.id, category.owner_id) for category in categories])
		# group_relations = itertools.groupby(relations, key=lambda k: k.category_id)
		# pipeline = conn.pipeline()
		#
		# for category_id, relations in group_relations:
		# 	corp_id = category_id_2_owner_id.get(category_id)
		# 	temp_key = 'category:{%s}_products' % category_id
		# 	pipeline.lpush(temp_key, *[relation.product_id for relation in relations])
		# 	print '<<'
		# pipeline.execute()
		# print '<-----------prepare category_products end------------------------!'
		
		
		
		
		# 预热商品的所在分组
		relations = mall_models.CategoryHasProduct.select()
		product_2_relations = itertools.groupby(relations, key=lambda k: k.product_id)
		print '<-----------prepare product in categories start------------------------!'
		pipeline = conn.pipeline()
		for product_id, relations in product_2_relations:
			temp_key = "product:{%s}_in_categories" % product_id
			# [{}, {}]list字符串
			value = [dict(id=relation.category_id,
						  owner_id=relation.category.owner_id) for relation in relations]
			pipeline.set(temp_key, json.dumps(value))
			print '<<', product_id
		pipeline.execute()
		print '<-----------prepare product in categories end------------------------!'

		