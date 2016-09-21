# -*- coding: utf-8 -*-
from datetime import datetime
import json
from bdem import msgutil

from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource

from business.mall.product_pool import ProductPool
from db.mall import models as mall_models
from db.mall import promotion_models
from db.account import models as account_models
from business.account.user_profile import UserProfile
from business import model as business_model
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
from settings import PANDA_IMAGE_DOMAIN
from services.product_service.task import clear_sync_product_cache

from core import paginator


class Product(business_model.Model):
	__slots__ = (
		'id',
		'owner_id',
		'name',
		'physical_unit',
		'price',
		'introduction',
		'weight',
		'thumbnails_url',
		'pic_url',
		'detail',
		'remark',
		'display_index',
		'created_at',
		'shelve_type',
		'shelve_start_time',
		'shelve_end_time',
		'min_limit',
		'stock_type',
		'stocks',
		'is_deleted',
		'is_support_make_thanks_card',
		'type',
		'update_time',
		'postage_id',
		'is_use_online_pay_interface',
		'is_use_cod_pay_interface',
		'promotion_title',
		'user_code',
		'bar_code',
		'unified_postage_money',
		'postage_type',
		'is_member_product',
		'supplier',
		'supplier_user_id',
		'supplier_name',
		'purchase_price',
		'is_enable_bill',
		'is_delivery',
		'buy_in_supplier',

		'is_model_deleted',
		'custom_model_properties',
		'model_type',
		'swipe_images',
		'model_name',
		'model',
		'categories',
		'properties',

		'group_buy_info',
		'sales',
		# 促销
		'promotion',

		'display_price',
		'display_price_range',

		# 多规格相关
		'system_model_properties',
		'models',
		'_is_use_custom_model',
		'standard_model',
		'current_used_model',
		'custom_models',

	)

	def __init__(self, model=None):
		super(Product, self).__init__()

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)




	def save(self,product_data):
		owner_id = product_data.base_info['owner_id']

		db_model = mall_models.Product.create(
			owner_id=owner_id,
			name=product_data.base_info['name'],
			promotion_title=product_data.base_info['promotion_title'],
			user_code=product_data.base_info['user_code'],

			detail=product_data.base_info['detail'],
			type=product_data.base_info['type'],

			# 支付信息
			is_use_online_pay_interface=product_data.pay_info['is_use_online_pay_interface'],
			is_use_cod_pay_interface=product_data.pay_info['is_use_cod_pay_interface'],
			is_enable_bill=product_data.pay_info['is_enable_bill'],

			thumbnails_url=product_data.image_info['thumbnails_url'],

			# 运费信息
			postage_type=product_data.postage_info['postage_type'],
			postage_id=product_data.postage_info['postage_id'],
			unified_postage_money=product_data.postage_info['unified_postage_money'],
			is_delivery=product_data.postage_info['is_delivery'],
		)

		standard_model = product_data.standard_model

		mall_models.ProductModel.create(
			owner=owner_id,
			product=db_model,
			name='standard',
			is_standard=True,
			price=standard_model['price'],
			weight=standard_model['weight'],
			stock_type=standard_model['stock_type'],
			stocks=standard_model['stocks'],
			user_code=standard_model['user_code'],
			is_deleted=standard_model['is_deleted']
		)

		# 处理custom商品规格
		custom_models = product_data.custom_models
		for custom_model in custom_models:
			product_model = mall_models.ProductModel.create(
				owner=owner_id,
				product=db_model,
				name=custom_model['name'],
				is_standard=False,
				price=custom_model['price'],
				weight=custom_model['weight'],
				stock_type=custom_model['stock_type'],
				stocks=custom_model['stocks'],
				user_code=custom_model['user_code']
			)

			for property in custom_model['properties']:
				mall_models.ProductModelHasPropertyValue.create(
					model=product_model,
					property_id=property['property_id'],
					property_value_id=property['property_value_id']
				)

		# 处理轮播图
		for swipe_image in product_data.image_info['swipe_images']:
			if swipe_image['width'] and swipe_image['height']:
				mall_models.ProductSwipeImage.objects.create(
					product=db_model,
					url=swipe_image['url'],
					width=swipe_image['width'],
					height=swipe_image['height']
				)

		# 处理商品分类
		for category_id in product_data.category_ids.split(','):
			category_id = int(category_id)
			mall_models.CategoryHasProduct.create(
				category_id=category_id,
				product_id=db_model.id)

		topic_name = "test-topic"
		data = {
			"name": "save_product",
			"data": {
				"product_id": db_model.id,
				"product_name": db_model.name
			}
		}
		msg_name = "cancel_order"
		msgutil.send_message(topic_name, msg_name, data)