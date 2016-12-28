# -*- coding: utf-8 -*-
# __author__ = 'robert'
import datetime
import array

from util.command import BaseCommand
from db.mall import models as mall_models


class Command(BaseCommand):
	help = "python manage.py upgrade_product_db"
	args = ''

	def handle(self, **options):
		pooled_products = set([pooled_product.product_id for pooled_product in mall_models.ProductPool.select()])
		for product in mall_models.Product.select().dj_where(is_deleted=False):
			if not product.id in pooled_products:
				print 'add %s' % product.name
				# 0:下架（待售） 1:上架（在售） 2:回收站
				if product.shelve_type == 0:
					status = mall_models.PP_STATUS_OFF
				elif product.shelve_type == 1:
					status = mall_models.PP_STATUS_ON
				elif product.shelve_type == 2:
					status = mall_models.PP_STATUS_DELETE
				else:
					status = mall_models.PP_STATUS_ON_POOL
				mall_models.ProductPool.create(
					woid=product.owner_id,
					product_id=product.id,
					status=status,
					display_index=9999999,
					type=mall_models.PP_TYPE_CREATE
				)


