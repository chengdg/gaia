# -*- coding: utf-8 -*-
import json

from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource

from business.mall.product_pool import ProductPool
from db.mall import models as mall_models
from db.account import models as account_models
from business.account.user_profile import UserProfile
from business import model as business_model
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
from settings import PANDA_IMAGE_DOMAIN
from services.product_service.task import clear_sync_product_cache

from core import paginator


def _init_custom_model(self, custom_model_str):
	properties = []
	property_infos = custom_model_str.split('_')
	for property_info in property_infos:
		items = property_info.split(':')
		properties.append({
			'property_id': int(items[0]),
			'property_value_id': int(items[1])
		})
	return properties


def _extract_product_model(args):
	is_use_custom_models = int(args.get("is_use_custom_model", ''))

	custom_model_data = json.loads(args.get('customModels', '[]'))
	if custom_model_data and is_use_custom_models:
		standard_model = {
			"price": 0.0,
			"weight": 0.0,
			"stock_type": mall_models.PRODUCT_STOCK_TYPE_LIMIT,
			"stocks": 0,
			"user_code": '',
			"is_deleted": True
		}
		custom_models = custom_model_data
		for model in custom_models:
			model['properties'] = _init_custom_model(model['name'])
			if model.get('stocks') and int(model.get('stocks')) == -1:
				model['stocks'] = 0
	else:
		stock_type = int(args.get(
			'stock_type',
			mall_models.PRODUCT_STOCK_TYPE_UNLIMIT)
		)
		stocks = args.get('stocks')
		if stocks and int(stocks) == -1:
			stocks = 0
		stocks = int(stocks) if stocks else 0
		standard_model = {
			"price": args.get('price', '0.0').strip(),
			"weight": args.get('weight', '0.0').strip(),
			"stock_type": stock_type,
			"stocks": stocks,
			"user_code": args.get('user_code', '').strip(),
		}
		custom_models = []

	return standard_model, custom_models


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

	@staticmethod
	def empty_product():
		product = Product(None)
		return product

	@staticmethod
	@param_required(['db_model'])
	def from_model(args):
		model = args['db_model']
		product = Product(model)
		return product

	# @staticmethod
	# @param_required(['product_id'])
	# def from_id(args):
	#     product_db_model = mall_models.Product.get(id=args['product_id'])
	#     return Product(product_db_model)

	@staticmethod
	@param_required(['product_id'])
	def from_panda_product_id(args):
		panda_product = mall_models.PandaHasProductRelation.select() \
			.dj_where(panda_product_id=args['product_id']).first()
		if panda_product:
			product_db_model = mall_models.Product.get(id=panda_product.weapp_product_id)
			return Product(product_db_model)

	@staticmethod
	@param_required(['product_ids'])
	def from_ids(args):
		product_models = mall_models.Product.select().dj_where(id__in=args['product_ids'])
		products = []
		for model in product_models:
			products.append(Product(model))
		return products

	def fill_specific_model(self, model_name):
		product_model = mall_models.ProductModel.select().dj_where(product_id=self.id, name=model_name).first()
		product = self
		product.price = product_model.price
		product.weight = product_model.weight
		product.stock_type = product_model.stock_type
		product.stocks = product_model.stocks
		product.model_name = model_name
		product.model = product_model
		product.is_model_deleted = False
		product.user_code = product_model.user_code
		if product_model.is_deleted:
			product.is_model_deleted = True

		property_ids = []
		property_value_ids = []
		name = product.model_name
		if product.model_name != 'standard':
			for model_property_info in product.model_name.split('_'):
				property_id, property_value_id = model_property_info.split(':')
				property_ids.append(property_id)
				property_value_ids.append(property_value_id)

				id2property = dict(
					[
						(property.id, {"id": property.id, "name": property.name})
						for property in mall_models.ProductModelProperty.select().dj_where(id__in=property_ids)
						])
				for property_value in mall_models.ProductModelPropertyValue.select().dj_where(
						id__in=property_value_ids):
					id2property[property_value.property_id]['property_value'] = property_value.name
					id2property[property_value.property_id]['property_pic_url'] = property_value.pic_url
			product.custom_model_properties = id2property.values()
			product.custom_model_properties.sort(lambda x, y: cmp(x['id'], y['id']))
		else:
			product.custom_model_properties = None

	@property
	def db_models(self):
		"""

		"""
		models = self.context.get('models', None)
		if not models and self.id:
			# return ProductTemplateProperty.from_template_id({"template_id": self.id})
			pass
		return models

	@db_models.setter
	def db_models(self, models):
		"""

		"""
		self.context['models'] = models

	# def save(self, panda_product_id):
	#
	#     user_profile = UserProfile.from_webapp_type({'webapp_type': 2})
	#     if not user_profile:
	#         return None
	#     owner_id = user_profile[0].user_id
	#     product = mall_models.Product.create(
	#         owner=owner_id,
	#         name=self.name,
	#         supplier=self.supplier,
	#         detail=self.detail,
	#         pic_url='',
	#         introduction='',
	#         thumbnails_url=self.thumbnails_url,
	#         price=self.price,
	#         weight=self.weight,
	#         stock_type=self.stock_type,
	#         purchase_price=self.purchase_price,
	#         stocks=0,
	#         promotion_title=self.promotion_title if self.promotion_title else ''
	#
	#     )
	#     mall_models.PandaHasProductRelation.create(
	#         panda_product_id=int(panda_product_id),
	#         weapp_product_id=product.id,
	#     )
	#     new_product = Product(product)
	#
	#     return new_product


	def modify(self,args):
		# 获取默认运费
		owner_id = args['owner_id']
		product_id = args['product_id']
		# todo 
		mall_type = account_models.UserProfile.select().dj_where(user_id=owner_id).first().webapp_type
		


		swipe_images = json.loads(args.get('swipe_images', '[]'))
		thumbnails_url = swipe_images[0]["url"]

		# 添加团购活动判断:非自营\团购\标准规格 todo
		# if mall_type == 0:
		# 	is_group_buying = product_is_group(product_id, woid)
		# else:
		# 	is_group_buying = False
		has_product_model = mall_models.ProductModel.select().dj_where(
			owner_id=owner_id,
			product_id=product_id,
			name='standard').exists()



		# if is_group_buying and has_product_model:
		# 	# 团购流程
		# 	utils.handle_group_product(request, product_id, swipe_images, thumbnails_url)
		if False:
			pass
		else:
			# 标准流程


			# 处理商品规格
			standard_model, custom_models = _extract_product_model(args)
			# 处理standard商品规格
			has_product_model = mall_models.ProductModel.objects.filter(
				owner_id=owner_id,
				product_id=product_id,
				name='standard').exists()

			if standard_model.get('is_deleted', None):
				# 多规格的情况
				db_standard_model = models.ProductModel.objects.filter(
					owner_id=woid,
					product_id=product_id,
					name='standard'
				)
				if not db_standard_model[0].is_deleted:
					from mall.promotion import models as promotion_models
					# 单规格改多规格商品
					db_standard_model.update(is_deleted=True)

					# 结束对应买赠活动 jz
					premiumSaleIds = set(promotion_models.PremiumSaleProduct.objects.filter(
						product_id=db_standard_model[0].product_id).values_list('premium_sale_id', flat=True))
					if len(premiumSaleIds) > 0:
						from webapp.handlers import event_handler_util
						promotionIds = set(promotion_models.Promotion.objects.filter(
							detail_id__in=premiumSaleIds,
							type=promotion_models.PROMOTION_TYPE_PREMIUM_SALE).values_list('id', flat=True))
						event_data = {
							"id": ','.join([str(id) for id in promotionIds])
						}
						event_handler_util.handle(event_data, 'finish_promotion')
			else:
				models.ProductModel.objects.filter(
					owner_id=woid, product_id=product_id, name='standard'
				).update(
					price=standard_model['price'],
					weight=standard_model['weight'],
					stock_type=standard_model['stock_type'],
					stocks=standard_model['stocks'],
					user_code=standard_model['user_code'],
					is_deleted=False
				)

			# 清除旧的custom product model
			existed_models = [product_model for product_model in models.ProductModel.objects.filter(
				owner=request.manager,
				product_id=product_id
			) if product_model.name != 'standard']
			existed_model_names = set([model.name for model in existed_models])

			# 处理custom商品规格
			updated_model_names = set()
			for custom_model in custom_models:
				custom_model_name = custom_model['name']
				if custom_model_name in existed_model_names:
					# model已经存在，更新之
					# # 记录被更新的model name
					updated_model_names.add(custom_model_name)
					models.ProductModel.objects.filter(
						product_id=product_id, name=custom_model_name
					).update(
						price=custom_model['price'],
						weight=custom_model['weight'],
						stock_type=custom_model['stock_type'],
						stocks=custom_model['stocks'],
						user_code=custom_model['user_code'],
						is_deleted=False
					)

					product_model = models.ProductModel.objects.get(
						product_id=product_id, name=custom_model_name)
					models.ProductModelHasPropertyValue.objects.filter(
						model=product_model).delete()
				else:
					# model不存在，创建之
					product_model = models.ProductModel.objects.create(
						owner=request.manager,
						product_id=product_id,
						name=custom_model['name'],
						is_standard=False,
						price=custom_model['price'],
						weight=custom_model['weight'],
						stock_type=custom_model['stock_type'],
						stocks=custom_model['stocks'],
						user_code=custom_model['user_code']
					)

				for property in custom_model['properties']:
					models.ProductModelHasPropertyValue.objects.create(
						model=product_model,
						property_id=property['property_id'],
						property_value_id=property['property_value_id']
					)

			# 删除不用的models
			existed_model_names_not_delete = set([model.name for model in existed_models if not model.is_deleted])
			to_be_deleted_model_names = existed_model_names_not_delete - updated_model_names
			if len(to_be_deleted_model_names):
				models.ProductModel.objects.filter(
					product_id=product_id, name__in=to_be_deleted_model_names
				).update(is_deleted=True)

			# 处理轮播图
			models.ProductSwipeImage.objects.filter(
				product_id=product_id
			).delete()
			for swipe_image in swipe_images:
				models.ProductSwipeImage.objects.create(
					product_id=product_id,
					url=swipe_image['url'],
					width=swipe_image['width'],
					height=swipe_image['height']
				)

			# 处理property
			properties = request.POST.get('properties')
			properties = json.loads(properties) if properties else []
			property_ids = set([property['id'] for property in properties])
			existed_property_ids = set([
				                           property.id for property in models.ProductProperty.objects.filter(
					owner_id=woid, product_id=product_id)
				                           ])
			for property in properties:
				if property['id'] < 0:
					models.ProductProperty.objects.create(
						owner=request.manager,
						product_id=product_id,
						name=property['name'],
						value=property['value']
					)
				else:
					models.ProductProperty.objects.filter(
						owner_id=woid, id=property['id']
					).update(name=property['name'], value=property['value'])
			property_ids_to_be_delete = existed_property_ids - property_ids
			models.ProductProperty.objects.filter(
				id__in=property_ids_to_be_delete).delete()

			# 减少原category的product_count
			_update_product_category(request, product_id)

			# 更新product
			postage_type = request.POST['postage_type']
			if postage_type == models.POSTAGE_TYPE_UNIFIED:
				postage_id = -1
				unified_postage_money = request.POST.get(
					'unified_postage_money', '')
				if unified_postage_money == '':
					unified_postage_money = 0.0
			else:
				postage_id = 999  # request.POST['postage_config_id']
				unified_postage_money = 0.0

			min_limit = request.POST.get('min_limit', '0')
			if not min_limit.isdigit():
				min_limit = 0
			else:
				min_limit = float(min_limit)
			purchase_price = request.POST.get("purchase_price", '')
			if purchase_price == '' or not purchase_price:
				purchase_price = 0
			is_enable_bill = request.POST.get('is_enable_bill', False)
			if is_enable_bill in [True, '1', 'True']:
				is_enable_bill = True
			else:
				is_enable_bill = False

			is_delivery = request.POST.get('is_delivery', False)

			is_bill = True if request.manager.username not in settings.WEIZOOM_ACCOUNTS else  False
			if is_bill is False:
				is_enable_bill = False
				is_delivery = False

			param = {
				'name': request.POST.get('name', '').strip(),
				'promotion_title': request.POST.get('promotion_title', '').strip(),
				'user_code': request.POST.get('user_code', '').strip(),
				'bar_code': request.POST.get('bar_code', '').strip(),
				'thumbnails_url': thumbnails_url,
				'detail': request.POST.get('detail', '').strip(),
				'type': request.POST.get('type', models.PRODUCT_DEFAULT_TYPE),
				'is_use_online_pay_interface': 'is_enable_online_pay_interface' in request.POST,
				'is_use_cod_pay_interface': 'is_enable_cod_pay_interface' in request.POST,
				'postage_id': postage_id,
				'unified_postage_money': unified_postage_money,
				'postage_type': postage_type,
				'stocks': min_limit,
				'is_member_product': request.POST.get("is_member_product", False) == 'on',
				# 'supplier': request.POST.get("supplier", 0),
				# 'purchase_price': purchase_price,
				'is_enable_bill': is_enable_bill,
				'is_delivery': is_delivery,
				'buy_in_supplier': int(request.POST.get('buy_in_supplier', False)),
				'limit_zone_type': int(request.POST.get('limit_zone_type', '0')),
				'limit_zone': int(request.POST.get('limit_zone_template', '0'))
			}

			if mall_type == 1:
				param['supplier'] = request.POST.get("supplier", 0)
				param['purchase_price'] = purchase_price

			# 微众商城代码
			# if request.POST.get('weshop_sync', None):
			#     param['weshop_sync'] = request.POST['weshop_sync'][0]
			models.Product.objects.record_cache_args(
				ids=[product_id]
			).filter(
				owner=request.manager,
				id=product_id
			).update(**param)

	def update(self):
		"""

		"""
		change_rows = mall_models.Product.update(name=self.name,
												stock_type=self.stock_type,
												purchase_price=self.purchase_price,
												detail=self.detail,
												price=self.price,
												weight=self.weight,
												promotion_title=self.promotion_title,
												thumbnails_url=self.thumbnails_url
												).dj_where(id=self.id).execute()
		# 清理缓存
		try:

			clear_sync_product_cache.delay(product_id=self.id)
		except:
			msg = unicode_full_stack()
			watchdog.error(msg)
			# print msg
		return change_rows

	def delete(self):
		"""
		主要更新商品为已删除，然后关联关系需要更新不可见
		"""
		#
		change_rows = mall_models.Product.update(is_deleted=True).dj_where(id=self.id).execute()
		if change_rows > 0:
			ProductPool.delete_from_product({'product_id': self.id})
		return change_rows

	@staticmethod
	@param_required(['product_ids'])
	def check_product_shelve_on(args):
		"""
		获取已经上架的产品
		"""
		product_ids = args.get('product_ids')
		pools = mall_models.ProductPool.select().dj_where(product_id__in=product_ids,
														status=mall_models.PP_STATUS_ON)
		on_product_ids = [pool.product_id for pool in pools]
		return list(set(on_product_ids))

	@staticmethod
	@param_required(['product_id', 'owner_id', 'fill_options'])
	def from_id(args):
		product_id = args['product_id']
		owner_id = args['owner_id']

		fill_options = args.get['fill_options']

		is_in_owner_pool = ProductPool.get({'owner_id': owner_id})
		# todo 临时关闭
		# if not is_in_owner_pool:
		#     return None
		db_model = mall_models.Product.select().dj_where(id=product_id).first()
		product = Product(db_model)

		Product.__fill_details(owner_id, [product], fill_options)
		return product

	@staticmethod
	@param_required(['owner_id', 'shelve_type', 'is_deleted', 'fill_options'])
	def from_owner_id(args):
		
		products = mall_models.Product.select().dj_where(owner=args['owner_id'], shelve_type=args['shelve_type'], is_deleted=args['is_deleted'])
		# 分页
		pageinfo, products = paginator.paginate(products, args['cur_page'], args['count_per_page'], query_string=args.get('query_string', None))
		# product_list = []
		products = [Product(product) for product in products]
		Product.__fill_details(args['owner_id'], products, args['fill_options'])

		return products, pageinfo

	@staticmethod
	@param_required(['owner_id', 'fill_options'])
	def from_onshelf_products(args):
		
		products = mall_models.Product.select().dj_where(owner=args['owner_id'], shelve_type=mall_models.PRODUCT_SHELVE_TYPE_ON)
		# product_list = []
		products = [Product(product) for product in products]
		Product.__fill_details(args['owner_id'], products, args['fill_options'])

		return products

	@staticmethod
	@param_required(['owner_id', 'fill_options'])
	def promotion_products(args):
		'''
		已经上架的商品
		'''
		user_profile = UserProfile.from_user_id({'user_id': args['owner_id']})
		mall_type = user_profile.webapp_type
		promotion_products = mall_models.Product.select().dj_where(owner_id=args['owner_id'], shelve_type=mall_models.PRODUCT_SHELVE_TYPE_ON)
		# TODO   查询功能
		# 分页
		pageinfo, promotion_products = paginator.paginate(promotion_products, args['cur_page'], args['count_per_page'], query_string=args.get('query_string', None))
		promotion_products = [Product(product) for product in promotion_products]
		Product.__fill_details(args['owner_id'], promotion_products, args['fill_options'])
		return promotion_products, pageinfo

	@staticmethod
	@param_required(['owner_id','promotion_id' , 'fill_options'])
	def from_promotion_id(args):
		promotion_products = mall_models.Product.select().dj_where(owner_id=args['owner_id'], id=args['promotion_id'])
		promotion_products = [Product(product) for product in promotion_products]
		Product.__fill_details(args['owner_id'], promotion_products, args['fill_options'])

	@staticmethod
	def __fill_details(owner_id, products, options):
		"""填充各种细节信息

		此方法会根据options中的各种填充选项，填充相应的细节信息

		@param owner_id: owner_id
		@param[in] products: Product业务对象集合
		@param[in] options: 填充选项
			with_price: 填充价格信息
			with_product_model: 填充所有商品规格信息
			with_product_promotion: 填充商品促销信息
			with_image: 填充商品轮播图信息
			with_property: 填充商品属性信息
			with_selected_category: 填充选中的分类信息
			with_all_category: 填充所有商品分类详情
			with_sales: 填充商品销售详情
			with_group_buy_info: 填充团购信息
		"""

		if options.get('with_selected_category', False):
			Product.__fill_category_detail(
				owner_id,
				products,
				True)

		if options.get('with_price', False):
			Product.__fill_price(products)

		if options.get('with_product_promotion', False):
			Product.__fill_product_promotion(owner_id, products)

		if options.get('with_sales', False):
			Product.__fill_sales(owner_id, products)

		if options.get('with_all_category', False):
			Product.__fill_category_detail(
				owner_id,
				products,
				False)
		if options.get('with_is_select', None):
			Product.__fill_is_select(owner_id, products)

		if options.get('with_image', False):
			Product.__fill_image_detail(products)

		if options.get('with_property', False):
			Product.__fill_property_detail(owner_id, products)

		if options.get('with_group_buy_info', False):
			Product.__fill_group_buy_info(owner_id, products)

		# todo 优化
		id2property = None
		id2propertyvalue = None
		is_enable_model_property_info = options.get(
			'with_model_property_info',
			False)
		if is_enable_model_property_info:
			# 获取model property，为后续使用做准备
			# properties = list(
			# 	ProductModelProperty.objects.filter(
			# 		owner=webapp_owner))

			pool_weapp_profile = account_models.UserProfile.select().dj_where(webapp_type=2).first()
			if pool_weapp_profile:
				properties = mall_models.ProductModelProperty.select().where(
					(mall_models.ProductModelProperty.owner == owner_id) | (
					mall_models.ProductModelProperty.owner == pool_weapp_profile.user_id))
			else:
				# TODO bert prodcut_pool 增加默认商品规格 owner
				properties = mall_models.ProductModelProperty.select().dj_where(
					owner=owner_id)
			property_ids = [property.id for property in properties]
			id2property = dict([(str(property.id), property)
								for property in properties])
			id2propertyvalue = {}
			for value in mall_models.ProductModelPropertyValue.select().dj_where(property_id__in=property_ids):
				id = '%d:%d' % (value.property_id, value.id)
				id2propertyvalue[id] = value

		product_ids = [product.id for product in products]

		if options.get('with_product_model', False):
			Product.__fill_model_detail(
				owner_id,
				products,
				product_ids,
				id2property,
				id2propertyvalue,
				is_enable_model_property_info)

	@staticmethod
	def __fill_is_select(owner_id, products):
		'''
		# 在优惠卷，新增优惠卷， 选择部分商品添加时   是否有选取按扭
		'''
		#TODO 需要从cache获取被禁的商品id
		# TODO 可以重新选取功能

		forbidden_coupon_product_ids = [] #TODO 需要从cache获取被禁的商品id   #webapp_cache.get_forbidden_coupon_product_ids(request.manager.id)
		for product in products:
			has_forbidden_coupon = False
			if product.id in forbidden_coupon_product_ids:
				has_forbidden_coupon = True
			product.promotion = {
				'can_select': True,
				'has_forbidden_coupon': has_forbidden_coupon
			}

	@staticmethod
	def __fill_group_buy_info(owner_id, products):

		product_ids = [str(p.id) for p in products]

		params = {
			'woid': owner_id,
			'pids': "_".join(product_ids)
		}

		resp = Resource.use('marketapp_apiserver').get({
			'resource': 'group.group_buy_products',
			'data': params
		})

		product2group_info = {}
		if resp and resp['code'] == 200:
			product_group_infos = resp['data']['pid2is_in_group_buy']

			for product_group in product_group_infos:
				product2group_info[product_group["pid"]] = product_group["is_in_group_buy"]

		for product in products:
			product.group_buy_info = {
				'is_in_group_buy': product2group_info.get(product.id, False)
			}

	@staticmethod
	def __fill_price(products):
		"""根据商品规格，获取商品价格
		"""
		# 获取所有models
		product2models = {}
		product_ids = [product.id for product in products]
		for model in mall_models.ProductModel.select().dj_where(product_id__in=product_ids):
			if model.is_deleted:
				# model被删除，跳过
				continue

			product_id = model.product_id
			if product_id in product2models:
				models = product2models[product_id]
			else:
				models = {
					'standard_model': None,
					'custom_models': [],
					'is_use_custom_model': False}
				product2models[product_id] = models

			if model.name == 'standard':
				models['standard_model'] = model
			else:
				models['is_use_custom_model'] = True
				models['custom_models'].append(model)

		# 为每个product确定显示价格
		for product in products:
			product_id = product.id
			if product_id in product2models:
				models = product2models[product.id]
				if models['is_use_custom_model']:
					custom_models = models['custom_models']
					if len(custom_models) == 1:
						product.display_price = custom_models[0].price
					else:
						prices = sorted(
							[model.price
							 for model in custom_models])
						# 列表页部分显示商品的最小价格
						# add by liupeiyu at 19.0
						# product.display_price = '%s-%s' % (prices[0], prices[-1])
						product.display_price = prices[0]
				else:
					product.display_price = models['standard_model'].price
			else:
				product.display_price = product.price

	@staticmethod
	def __fill_product_promotion(owner_id, products):
		# 需要去做  商品促销
		from datetime import datetime
		from db.mall import promotion_models
		today = datetime.today()
		id2product = {}
		product_ids = []
		for product in products:
			# product.promotion = {}
			id2product[product.id] = product
			product_ids.append(product.id)

		type2promotions = {}
		id2promotion = {}
		product_promotion_relations = promotion_models.ProductHasPromotion.select().dj_where(product_id__in=product_ids)
		promotion_ids = [relation.promotion_id for relation in product_promotion_relations]
		promotions = [relation.promotion for relation in product_promotion_relations]
		# promotions = list(promotion_models.ProductHasPromotion.select().dj_where(product_id__in=product_ids))
		for promotion in promotions:
			type2promotions.setdefault(promotion.type, []).append(promotion)
			id2promotion[promotion.id] = promotion

		for relation in product_promotion_relations:
			product = id2product[relation.product_id]
			promotion = id2promotion[relation.promotion_id]
			# import pdb
			# pdb.set_trace()
			product.promotion = {
				'id': promotion.id,
				'type': promotion.type,
				'name': promotion.name,
				'status_value': promotion.status,
				'status': promotion.status,
				'start_date': promotion.start_date.strftime("%Y-%m-%d %H:%M"),
				'end_date': promotion.end_date.strftime('%Y-%m-%d %H:%M')
			}

		# for type, promotions in type2promotions.items():
		# 	if type == promotion_models.PROMOTION_TYPE_FLASH_SALE:
		# 		model2product = dict([(product.context['db_model'].id, product.context['db_model']) for product in products])
		# 		product_model_ids = [product.context['db_model'].id for product in products]
		# 		model_promotion_details = promotion_models.ProductModelFlashSaleDetail.select().dj_where(
		# 			owner=owner_id,
		# 			product_model_id__in=product_model_ids)
		# 		for model_promotion_detail in model_promotion_details:
		# 			model2product[promotion_detail.product_model_id].promotion['price'] = model_promotion_detail.promotion_price
		# 	else:
				# pass

	@staticmethod
	def __fill_sales(owner_id, products):
		# 需要做的    商品销量
		id2product = {}
		product_ids = []
		for product in products:
			product.sales = 0
			id2product[product.id] = product
			product_ids.append(product.id)

		for sales in mall_models.ProductSales.select().dj_where(product_id__in=product_ids):
			product_id = sales.product_id
			if id2product.has_key(product_id):
				id2product[product_id].sales = sales.sales

	@staticmethod
	def __fill_image_detail(products):
		for product in products:
			product.swipe_images = [
				{'id': img.id, 'url': img.url, 'linkUrl': img.link_url, 'width':
					img.width, 'height': img.height,}
				for img in mall_models.ProductSwipeImage.select().dj_where(
					product_id=product.id)]

	@staticmethod
	def __fill_category_detail(owner_id, products, only_selected_category):
		categories = mall_models.ProductCategory.select().dj_where(owner=owner_id).order_by('id')
		product_ids = [p.id for p in products]

		# 获取product关联的category集合
		id2product = dict([(product.id, product) for product in products])
		for product in products:
			product.categories = []
			product.context['id2category'] = {}
			id2product[product.id] = product
			if not only_selected_category:
				for category in categories:
					category_data = {
						'id': category.id,
						'name': category.name,
						'is_selected': False
					}
					product.categories.append(category_data)
					product.context['id2category'][category.id] = category_data

		id2category = dict([(category.id, category) for category in categories])
		for relation in mall_models.CategoryHasProduct.select().dj_where(product_id__in=product_ids).order_by('id'):
			category_id = relation.category_id
			product_id = relation.product_id
			if not category_id in id2category:
				# 微众商城分类，在商户中没有
				continue
			category = id2category[category_id]
			if not only_selected_category:
				id2product[product_id].context['id2category'][
					category.id]['is_selected'] = True
			else:
				id2product[product_id].categories.append({
					'id': category.id,
					'name': category.name,
					'is_selected': True
				})

	@staticmethod
	def __fill_property_detail(owner_id, products):
		for product in products:
			product.properties = [
				{"id": property.id, "name": property.name,
				 "value": property.value}
				for property in mall_models.ProductProperty.
					select().dj_where(product_id=product.id)]

	@staticmethod
	def __fill_model_detail(owner_id, products, product_ids, id2property, id2propertyvalue,
							is_enable_model_property_info):
		_id2property = {}
		_id2propertyvalue = {}
		if is_enable_model_property_info:
			for id, property in id2property.items():
				_id2property[id] = {
					"id": property.id,
					"name": property.name,
					"values": []
				}

			for id, value in id2propertyvalue.items():
				_property_id, _value_id = id.split(':')
				_property = _id2property[_property_id]
				data = {
					'propertyId': _property['id'],
					'propertyName': _property['name'],
					"id": value.id,
					"name": value.name,
					"image": value.pic_url,
					"is_belong_product": False
				}
				_id2propertyvalue[id] = data
				_property['values'].append(data)

		# 获取所有models
		product2models = {}
		for model in mall_models.ProductModel.select().dj_where(product_id__in=product_ids):
			if model.is_deleted:
				# model被删除，跳过
				continue

			model_dict = {
				"id": model.id,
				"name": model.name,
				"price": '%.2f' % model.price,
				"weight": model.weight,
				"stock_type": model.stock_type,
				"stocks": model.stocks if model.stock_type == mall_models.PRODUCT_STOCK_TYPE_LIMIT else u'无限',
				"user_code": model.user_code,
				"market_price": '%.2f' % model.market_price,
				"gross_profit": '%.2f' % (model.price - model.purchase_price)
			}

			'''
			获取model关联的property信息
				model.property_values = [{
					'propertyId': 1,
					'propertyName': '颜色',
					'id': 1,
					'value': '红'
				}, {
					'propertyId': 2,
					'propertyName': '尺寸',
					'id': 3,
					'value': 'S'
				}]

				model.property2value = {
					'颜色': '红',
					'尺寸': 'S'
				}
			'''
			if is_enable_model_property_info and model.name != 'standard':
				ids = model.name.split('_')
				property_values = []
				property2value = {}
				for id in ids:
					# id的格式为${property_id}:${value_id}
					_property_id, _value_id = id.split(':')
					_property = _id2property[_property_id]
					_value = _id2propertyvalue[id]
					property2value[_property['name']] = {
						'id': _value['id'],
						'name': _value['name']
					}
					property_values.append({
						'propertyId': _property['id'],
						'propertyName': _property['name'],
						'id': _value['id'],
						'name': _value['name']
					})
					_value['is_belong_product'] = True
				model_dict['property_values'] = property_values
				model_dict['property2value'] = property2value

			product_id = model.product_id
			if product_id in product2models:
				models = product2models[product_id]
			else:
				models = {
					'standard_model': None,
					'custom_models': [],
					'is_use_custom_model': False}
				product2models[product_id] = models

			if model.name == 'standard':
				models['standard_model'] = model_dict
			else:
				models['is_use_custom_model'] = True
				models['custom_models'].append(model_dict)

		# 为每个product确定显示信息
		for product in products:
			product.sales = -1  # 实现sales逻辑
			product.system_model_properties = _id2property.values()
			product_id = product.id
			if product_id in product2models:
				models = product2models[product.id]
				product.models = [models['standard_model']]
				if models['is_use_custom_model']:
					product._is_use_custom_model = True
					product.custom_models = models['custom_models']
					product.standard_model = models['standard_model']
					custom_models = models['custom_models']
					product.models.extend(custom_models)
					if len(custom_models) == 1:
						target_model = custom_models[0]
						# 格式: X.00
						display_price_range = target_model['price']
					else:
						# 列表页部分显示商品的最小价格那个model的信息
						custom_models.sort(lambda x, y: cmp(float(x['price']), float(y['price'])))
						target_model = custom_models[0]
						low_price = target_model['price']
						high_price = custom_models[-1]['price']
						if low_price == high_price:
							# 格式: X.00
							display_price_range = low_price
						else:
							# 更改 格式: X.00 @延昊南
							low_price = low_price
							high_price = high_price
							display_price_range = '%s ~ %s' % (low_price, high_price)
				else:
					product._is_use_custom_model = False
					target_model = models['standard_model']
					product.standard_model = target_model
					display_price_range = target_model['price']

				product.current_used_model = target_model
				product.display_price = target_model['price']
				product.display_price_range = display_price_range
				product.user_code = target_model['user_code']
				product.stock_type = target_model['stock_type']
				product.min_limit = product.stocks
				product.stocks = u'无限' if target_model[
											  'stock_type'] == mall_models.PRODUCT_STOCK_TYPE_UNLIMIT else target_model[
					'stocks']
			else:
				# 所有规格都已经被删除
				product._is_use_custom_model = False
				product.current_used_model = {}
				product.display_price = product.price
				product.display_price_range = product.price
				product.user_code = product.user_code
				product.stock_type = mall_models.PRODUCT_STOCK_TYPE_LIMIT
				product.stocks = 0
				product.min_limit = 0
				product.standard_model = {}
				product.models = []


class ProductModel(business_model.Model):
	__slots__ = (
		'id',
		'owner_id',
		'product_id',
		'name',
		'is_standard',
		'price',
		'stock_type',
		'stocks',
		'weight',
		'is_deleted',
		'purchase_price'
	)

	def __init__(self, model):
		super(ProductModel, self).__init__()
		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)

	def save(self):
		# 标准规格
		product_model = mall_models.ProductModel.create(
			owner=self.owner_id,
			product=self.product_id,
			name=self.name,
			is_standard=self.is_standard,
			price=self.price,
			stock_type=self.stock_type,
			stocks=self.stocks,
			purchase_price=self.purchase_price,
			is_deleted=self.is_deleted,
			weight=self.weight
		)
		return ProductModel(product_model)

	@staticmethod
	@param_required(['product_id'])
	def from_product_id(args):
		product_models = mall_models.ProductModel.select().dj_where(product_id=args['product_id'],
																	is_deleted=False)

		return [ProductModel(product_model) for product_model in product_models]

	@staticmethod
	@param_required(['product_id', 'name'])
	def from_product_id_name(args):
		product_model = mall_models.ProductModel.select().dj_where(product_id=args['product_id'],
																   is_deleted=False,
																   name=args.get('name')).first()

		return ProductModel(product_model)

	def update(self):

		change_rows = mall_models.ProductModel.update(stock_type=self.stock_type,
													  stocks=self.stocks).dj_where(id=self.id).execute()
		return change_rows

	@staticmethod
	@param_required(['models'])
	def save_many(args):
		"""
		保存多个
		"""
		bulk_create = []
		models = args.get('models')
		bulk_create = [dict(owner=temp_model.owner_id,
							product=temp_model.product_id,
							name=temp_model.name,
							is_standard=temp_model.is_standard,
							price=temp_model.price,
							stock_type=temp_model.stock_type,
							stocks=temp_model.stocks,
							is_deleted=temp_model.is_deleted,
							weight=temp_model.weight,
							purchase_price=temp_model.purchase_price) for temp_model in models]

		mall_models.ProductModel.insert_many(bulk_create).execute()

	@staticmethod
	@param_required(['models', 'product_id'])
	def update_many_models(args):
		"""
		更新成多规格
		"""
		models = args.get('models')
		if not models:
			return None

		# 已经有的规格,直接更新,否则添加
		# model_names = mall_models.ProductModel.select().dj_where(product_id=args.get('product_id'))
		# names = [model_name.name for model_name in model_names]
		# 需要新增的规格
		need_add = []
		try:
			# 如果是true说明是多规格商品,否则是单规格商品
			need_update_stand = True
			# 先暂时将所有的规格更新成已经删除
			mall_models.ProductModel.update(is_deleted=True).dj_where(product_id=args.get('product_id')).execute()
			for temp_model in models:
				if mall_models.ProductModel.select().dj_where(name=temp_model.name,
															  product_id=temp_model.product_id).count() > 0:
					mall_models.ProductModel.update(price=temp_model.price,
													stock_type=temp_model.stock_type,
													stocks=temp_model.stocks,
													weight=temp_model.weight,
													purchase_price=temp_model.purchase_price,
													is_deleted=temp_model.is_deleted) \
						.dj_where(name=temp_model.name,
								  product_id=temp_model.product_id).execute()
					if temp_model.name == 'standard':
						need_update_stand = False
				else:
					need_add.append(temp_model)

			if need_add:
				ProductModel.save_many({'models': need_add})
			if need_update_stand:
				mall_models.ProductModel.update(is_deleted=True).dj_where(product_id=args.get('product_id'),
																		  name='standard').execute()
			return 'SUCCESS'
		except:
			msg = unicode_full_stack()
			watchdog.error(msg)
			return None


class ProductSwipeImage(business_model.Model):
	__slots__ = ()

	def __init__(self, model):
		super(ProductSwipeImage, self).__init__()
		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)
			# mall_models.ProductSwipeImage
			#     product = product,
			#     url = swipe_image['url'],
			#     width = swipe_image['width'],
			#     height = swipe_image['height']

	@staticmethod
	@param_required(['images'])
	def save_many(args):
		"""

		"""
		mall_models.ProductSwipeImage.insert_many(args.get('images')).execute()

	@staticmethod
	@param_required(['swipe_images', 'product_id'])
	def update_product_many(args):
		"""
		更新用户的多个信息
		"""
		mall_models.ProductSwipeImage.delete().dj_where(product=args['product_id']).execute()
		images = []
		for image in args['swipe_images']:
			url = image.get('url')
			if not url.startswith('http'):
				url = PANDA_IMAGE_DOMAIN + url
			images.append(dict(product=args['product_id'],
							   url=url,
							   width=100,
							   height=100))
		# images = [dict(product=args['product_id'],
		#                url=image.get('url'),
		#                width=100,
		#                height=100) for image in args['swipe_images']]

		# for image in self.swipe_images:

		ProductSwipeImage.save_many({'images': images})
