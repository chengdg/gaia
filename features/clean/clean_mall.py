# -*- coding: utf-8 -*-
import logging

from db.mall import models as mall_models
from django.db import connection

def clean():
	logging.info('clean database for mall')
	#支付接口配置
	mall_models.UserWeixinPayOrderConfig.delete().execute()
	mall_models.UserAlipayOrderConfig.delete().execute()
	mall_models.PayInterface.delete().execute()

	#运费配置
	reserved_ids = [p.id for p in mall_models.PostageConfig.select().dj_where(name=u'免运费')]
	mall_models.FreePostageConfig.delete().dj_where(postage_config_id__notin=reserved_ids).execute()
	mall_models.SpecialPostageConfig.delete().dj_where(postage_config_id__notin=reserved_ids).execute()
	mall_models.PostageConfig.delete().dj_where(name__not=u'免运费').execute()
	mall_models.PostageConfig.update(is_used=True).dj_where(name=u'免运费').execute()

	#图片分组
	mall_models.Image.delete().execute()
	mall_models.ImageGroup.delete().execute()

	#商品属性模板
	mall_models.ProductProperty.delete().execute()
	mall_models.TemplateProperty.delete().execute()
	mall_models.ProductPropertyTemplate.delete().execute()

	#商品规格属性
	mall_models.ProductModelPropertyValue.delete().execute()
	mall_models.ProductModelProperty.delete().execute()

	#商品分类
	mall_models.CategoryHasProduct.delete().execute()
	mall_models.ProductCategory.delete().execute()
