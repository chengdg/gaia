# -*- coding: utf-8 -*-
import logging

from db.mall import models as mall_models
from db.mall import promotion_models
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

	#促销
	promotion_models.ProductHasPromotion.delete().execute()
	promotion_models.PremiumSaleProduct.delete().execute()

	# 订单
	mall_models.OrderHasProduct.delete().execute()
	mall_models.OrderHasPromotion.delete().execute()
	mall_models.OrderHasGroup.delete().execute()
	mall_models.OrderHasRefund.delete().execute()
	mall_models.OrderCardInfo.delete().execute()
	mall_models.Order.delete().execute()

	#供应商
	mall_models.SupplierPostageConfig.delete().execute()
	mall_models.SupplierDivideRebateInfo.delete().execute()
	mall_models.SupplierRetailRebateInfo.delete().execute()
	mall_models.Supplier.delete().execute()

	#商品
	mall_models.ClassificationHasProduct.delete().execute()
	mall_models.Classification.delete().execute()
	mall_models.ProductModelHasPropertyValue.delete().execute()
	mall_models.ProductModel.delete().execute()
	mall_models.ProductSwipeImage.delete().execute()
	mall_models.ProductSales.delete().execute()
	mall_models.Product.delete().execute()
	mall_models.ProductPool.delete().execute()
