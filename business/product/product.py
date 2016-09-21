# -*- coding: utf-8 -*-
from bdem import msgutil

from business import model as business_model
from db.mall import models as mall_models


class Product(business_model.Model):
	__slots__ = (
		'id',
		'owner_id',
		'name',
		'price',
		'weight',
		'thumbnails_url',

		'detail',

		'display_index',
		'created_at',
		'shelve_type',

		'min_limit',

		'is_deleted',

		'type',
		'update_time',

		'is_use_online_pay_interface',
		'is_use_cod_pay_interface',

		'promotion_title',
		'bar_code',

		'postage_id',
		'unified_postage_money',
		'postage_type',

		'is_member_product',

		'supplier',

		'supplier_user_id',

		'supplier_name',

		'is_enable_bill',
		'is_delivery',
		'buy_in_supplier',

	)

	def __init__(self, model=None):
		super(Product, self).__init__()

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)

	def save(self, product, additional_data):
		owner_id = product.owner_id

		# 兼容历史数据
		if additional_data['is_use_custom_models']:
			user_code = additional_data.standard_model['user_code']
		else:
			user_code = ''

		# 创建商品表
		db_model = mall_models.Product.create(
			owner_id=owner_id,
			name=product.name,
			promotion_title=product.promotion_title,
			bar_code=product.bar_code,
			user_code=user_code,  # 兼容历史数据
			detail=product.detail,
			type=product.type,

			# 支付信息
			is_use_online_pay_interface=product.is_use_online_pay_interface,
			is_use_cod_pay_interface=product.is_use_cod_pay_interface,
			is_enable_bill=product.is_enable_bill,

			thumbnails_url=product.thumbnails_url,
			# 运费信息
			postage_type=product.postage_type,
			postage_id=product.postage_id,
			unified_postage_money=product.unified_postage_money,
			is_delivery=product.is_delivery,
			shelve_type=mall_models.DEFAULT_SHELVE_TYPE
		)

		standard_model = additional_data['standard_model']

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
		custom_models = additional_data['custom_models']
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
		for swipe_image in additional_data['swipe_images']:
			if swipe_image['width'] and swipe_image['height']:
				mall_models.ProductSwipeImage.objects.create(
					product=db_model,
					url=swipe_image['url'],
					width=swipe_image['width'],
					height=swipe_image['height']
				)

		# 处理商品分类
		for category_id in additional_data['category_ids']:
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
		msg_name = "msg_save_product"
		msgutil.send_message(topic_name, msg_name, data)
