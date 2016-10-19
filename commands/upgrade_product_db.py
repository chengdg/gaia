# -*- coding: utf-8 -*-
#__author__ = 'robert'
import datetime
import array

from util.command import BaseCommand
from db.mall import models as mall_models

class Command(BaseCommand):
	help = "python manage.py upgrade_product_db"
	args = ''
	
	def handle(self, **options):
		pooled_products = set([pooled_product.product_id for pooled_product in mall_models.ProductPool.select()])
		for product in mall_models.Product.select():
			if not product.id in pooled_products:
				print 'add %s' % product.name
				mall_models.ProductPool.create(
					woid = product.owner_id,
					product_id = product.id,
					status = mall_models.PP_STATUS_ON,
					display_index = 9999999,
					type = mall_models.PP_TYPE_CREATE
				)
		

