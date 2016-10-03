# -*- coding: utf-8 -*-
import logging

from db.mall import models as mall_models
from django.db import connection

def clean():
	logging.info('clean database for mall')
	mall_models.UserWeixinPayOrderConfig.delete().execute()
	mall_models.UserAlipayOrderConfig.delete().execute()
	mall_models.PayInterface.delete().execute()
