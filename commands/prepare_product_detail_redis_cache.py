# -*- coding: utf-8 -*-
import redis
import itertools
from util.command import BaseCommand

import pickle

from db.mall import models as mall_models
from db.account import models as account_models
from eaglet.core.db import models as eaglet_db

import settings


class Command(BaseCommand):
	help = "prepare product detail redis cache"
	args = ''
	
	def handle(self, *args, **options):
		
		conn = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_CACHES_DB)
		
		pipeline = conn.pipeline()
		print 'start loading....................'
		account = account_models.UserProfile.select().dj_where(webapp_type=2).first()
		
		products = mall_models.Product.select().dj_where(owner_id=account.user_id)
		product_ids = [product.id for product in products]
		
		# product_id_2_product = dict([(product.id, product) for product in products])
		
		sql = """
		 select product_id, min(mall_product_model.price) as display_price
		 from mall_product_model
		 join mall_product on mall_product.id = mall_product_model.product_id
		 where mall_product_model.is_deleted=false
		 and mall_product.is_deleted=false
		 and mall_product.owner_id = %s
		 group by product_id
		""" % account.user_id
		db = eaglet_db.db
		cursor = db.execute_sql(sql, ())
		product_2_price = dict()
		for index, row in enumerate(cursor.fetchall()):
			product_id = row[0]
			display_price = row[1]
			product_2_price[product_id] = display_price
		# print product_2_price
		swipe_images = mall_models.ProductSwipeImage.select().dj_where(product_id__in=product_ids)
		grouped_images = dict(itertools.groupby(swipe_images, key=lambda k: k.product_id))
		
		for product in products:
			print 'start load product:%s' % product.id
			
			product_id = product.id
			product_name = product.name
			thumbnails_url = product.thumbnails_url
			display_price = product_2_price.get(product_id)
			if not display_price:
				continue
			swipe_images = grouped_images.get(product_id)
			if not swipe_images:
				continue
			images = []
			for image in swipe_images:
				data = {
					'url': image.url if 'http:' in image.url else '%s%s' % (settings.IMAGE_HOST, image.url),
					'width': image.width,
					'height': image.height
				}
				images.append(data)
			temp_key = ':1:apiproduct_simple_detail_{pid:%s}' % product_id
			
			value = dict(id=product_id,
						 name=product_name,
						 is_deleted=False,
						 swipe_images=images,
						 is_member_product=False,
						 promotion_js='',
						 categories=[],
						 supplier=0,
						 display_price=display_price,
						 thumbnails_url=thumbnails_url)
			pipeline.set(temp_key, pickle.dumps(value))
			print 'finish loaded product:%s' % product.id
		pipeline.execute()
		print 'finish loaded all products!'
	