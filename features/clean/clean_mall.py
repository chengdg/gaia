# -*- coding: utf-8 -*-
import logging

from db.mall import models as mall_models
from django.db import connection

def clean():
	logging.info('clean database for mall')
	mall_models.UserWeixinPayOrderConfig.delete().execute()
	mall_models.UserAlipayOrderConfig.delete().execute()
	mall_models.PayInterface.delete().execute()

	reserved_ids = [p.id for p in mall_models.PostageConfig.select().dj_where(name=u'免运费')]
	mall_models.FreePostageConfig.delete().dj_where(postage_config_id__notin=reserved_ids).execute()
	mall_models.SpecialPostageConfig.delete().dj_where(postage_config_id__notin=reserved_ids).execute()
	mall_models.PostageConfig.delete().dj_where(name__not=u'免运费').execute()
	mall_models.PostageConfig.update(is_used=True).dj_where(name=u'免运费').execute()
