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
	help = "prepare community change price cache"
	args = ''
	
	def handle(self, *args, **options):
		
		conn = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_CACHES_DB)
		
		pipeline = conn.pipeline()
		print 'start loading....................'
		# account = account_models.UserProfile.select().dj_where(webapp_type=2).first()
		
		cus_models = mall_models.ProductCustomizedPrice.select()
		for model in cus_models:
			tmp_key = ":1:apicustomized_price_{wo:%s}_{pid:%s}" % (model.corp_id, model.product_id)
			pipeline.set(tmp_key, pickle.dumps(model.price))
			print 'loading%s' % model.product_id
		pipeline.execute()
		print 'finished!'
		