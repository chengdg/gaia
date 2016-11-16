# -*- coding: utf-8 -*-
#__author__ = 'robert'
import datetime
import array

from util.command import BaseCommand
from db.mall import models as mall_models
from eaglet.core.db import models as eaglet_db

class Command(BaseCommand):
	help = "python manage.py sync_category_product_count"
	args = ''
	
	def handle(self, **options):
		categories = mall_models.ProductCategory.select()
		for category in categories:
			sql = """
				update mall_product_category 
				set product_count = (select count(*) from mall_category_has_product where category_id = %d) 
				where id = %d;
				""" % (category.id, category.id)

			db = eaglet_db.db
			cursor = db.execute_sql(sql, ())
			print 'process ', category.id
		print 'success'		

