# -*- coding: utf-8 -*-
#__author__ = 'robert'
import datetime
import array

from util.command import BaseCommand
from db.mall import models as mall_models

class Command(BaseCommand):
	help = "python manage.py upgrade_product_display_index"
	args = ''
	
	def handle(self, **options):
		mall_models.ProductPool.update(display_index=9999999).dj_where(display_index=0).execute()
		print 'success'		

