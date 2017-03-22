# -*- coding: utf-8 -*-

import json

from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from db.mall import models as mall_models
from business import model as business_model
from business.decorator import cached_context_property

import settings
from util import send_product_message


class Product(business_model.Model):
	"""
	商品
	"""
	__slots__ = (
		'id',
		'owner_id',
		'type',
		'create_type',
		'is_deleted',
		'name',
		'display_index',
		'is_member_product',
		'weshop_sync',
		'shelve_type',
		'shelve_start_time',
		'shelve_end_time',
		'detail',
		'thumbnails_url',
		'order_thumbnails_url',
		'pic_url',
		'swipe_images',
		'detail_link',
		'bar_code',
		'min_limit',
		'categories',
		'id2category',
		'properties',
		'labels',

		#供应商信息
		'supplier_id',
		'supplier',
		'classification_lists',
		'classification_id',
		'classification_nav',
		#'supplier_user_id',

		#商品规格信息
		'is_use_custom_model',
		#'model_name',
		#'product_model_properties',
		'standard_model',
		'custom_models',
		'used_system_model_properties',

		#物流信息
		'postage_id',
		'postage_type',
		'unified_postage_money',

		#价格、销售信息
		'price_info',
		'sales',
		'is_sellout',
		'is_use_online_pay_interface',
		'is_use_cod_pay_interface',
		'product_promotion_title', #商品的促销标题
		'is_enable_bill',
		'buy_in_supplier',

		#促销信息
		'promotions',
		'promotion_title', #商品关联的促销活动的促销标题
		'integral_sale',
		'product_review',
		'is_deleted',
		'is_delivery', # 是否勾选配送时间
		# 'supplier_name' # 供货商名称
		'purchase_price',
		'price',
		'weight',
		'stock_type',
		'limit_zone_type',
		'limit_zone',

		# cps推广信息
		'cps_promoted_info',

		#时间信息
		'created_at',
		'sync_at',

		#审核状态
		'is_updated',
		'is_accepted',
		'status',

		#毛利信息
		'gross_profit_info',

		#供货商信息
		'supplier_info',
	)

	def __init__(self, model=None):
		business_model.Model.__init__(self)

		if model:
			self._init_slot_from_model(model)
			self.owner_id = model.owner_id
			self.min_limit = model.stocks
			self.thumbnails_url = '%s%s' % (settings.IMAGE_HOST, model.thumbnails_url) if model.thumbnails_url.find('http') == -1 else model.thumbnails_url
			self.pic_url = '%s%s' % (settings.IMAGE_HOST, model.pic_url) if model.pic_url.find('http') == -1 else model.pic_url
			self.custom_models = []
			self.swipe_images = []
			self.categories = []
			self.properties = []
			self.labels = []
			self.classification_lists = []
			self.sales = 0
			self.supplier_id = self.supplier
			self.supplier = None
			self.promotions = []
			self.create_type = None
			self.sync_at = None
			self.supplier_info = dict()

	def get_corp(self):
		from business.mall.corporation_factory import CorporationFactory
		return CorporationFactory.get()

	@property
	def is_sellout(self):
		"""
		[property] 是否卖光
		"""
		return self.total_stocks <= 0

	def get_labels(self, classification_id=None):
		"""
		只要单独给商品配置过标签，那么就不再获取所属商品分类的标签
		"""
		corp = self.get_corp()
		product_id = self.id
		classification_id = classification_id if classification_id else mall_models.ClassificationHasProduct.select().dj_where(
			product_id = product_id
		).first().classification_id
		product_has_labels = mall_models.ProductHasLabel.select().dj_where(product_id=product_id, classification_id=-1)
		if product_has_labels.count() > 0: #如果单独给商品配置过标签，则从ProductHasLabel中获取
			from business.mall.product_label.product_label_repository import ProductLabelRepository
			label_ids = [p.label_id for p in product_has_labels]
			#再获取商品所属分类所拥有的标签
			classification = corp.product_classification_repository.get_classification_by_product_id(classification_id)
			classification_labels = classification.get_labels()
			label_ids += [c.label_id for c in classification_labels]
			return ProductLabelRepository.get(corp).get_labels(set(label_ids))
		else: #没有就获取所属分类的标签
			from business.mall.product_label.product_label_repository import ProductLabelRepository
			return ProductLabelRepository.get(corp).get_labels_by_classification_id(classification_id)

	def manage_label(self, label_ids):
		"""
		管理商品标签，注意：不是商品所属分类包含的标签，而是直接属于商品的标签
		"""
		mall_models.ProductHasLabel.delete().dj_where(product_id=self.id).execute()
		for label_id in label_ids:
			mall_models.ProductHasLabel.create(
				product_id = self.id,
				label_id = label_id
			)

	@is_sellout.setter
	def is_sellout(self, value):
		"""
		[property setter] 是否卖光
		"""
		pass

	@property
	def refuse_reasons(self):
		"""
		驳回原因日志
		"""
		logs_models = mall_models.ProductRefuseLogs.select().dj_where(product_id=self.id)
		return [{'reason': log.refuse_reason, 'created_at': log.created_at.strftime('%Y-%m-%d %H:%M:%S')} for log in logs_models]

	@property
	def stocks(self):
		"""
		商品库存,如：[1,15,18,无限]
		"""
		stocks = set()
		unlimit = None

		product_models = mall_models.ProductModel.select().dj_where(product_id=self.id, is_deleted=False)

		if product_models.dj_where(is_standard=False).count() > 0:
			for product_model in product_models:
				if product_model.stock_type == mall_models.PRODUCT_STOCK_TYPE_UNLIMIT:
					unlimit = u'无限'
				else:
					stocks.add(product_model.stocks)
		else:
			product_model = product_models.first()
			if product_model.stock_type == mall_models.PRODUCT_STOCK_TYPE_UNLIMIT:
				unlimit = u'无限'
			else:
				stocks.add(product_model.stocks)

		if unlimit:
			stocks.add(unlimit)

		stocks = list(stocks)
		stocks.sort()

		return stocks

	@property
	def has_multi_models(self):
		"""
		是否多规格
		"""
		db_models = mall_models.ProductModel.select().dj_where(product_id=self.id, is_standard=False, is_deleted=False)
		return db_models.count() > 0

	@property
	def has_same_postage(self):
		"""
		是否统一运费
		"""
		return self.postage_type == mall_models.POSTAGE_TYPE_UNIFIED

	def verify(self, corp):
		"""
		审核通过
		"""
		product_id = self.id
		# 将商品放入product pool
		corp.product_pool.add_products([product_id])
		# 将商品放入待售shelf
		corp.forsale_shelf.add_products([product_id])

		# 更新商品状态
		mall_models.Product.update(
			status=mall_models.PRODUCT_STATUS['NOT_YET'],
			is_updated=False,
			is_accepted=True
		).dj_where(id=product_id).execute()

		send_product_message.send_product_outgiving_message(corp.id, self.id)

	def update_product_unverified(self, args):
		"""
		编辑商品信息(未审核)
		"""
		product_id = self.id
		product_data = json.dumps({
			'base_info': args['base_info'],
			'models_info': args['models_info'],
			'image_info': args['image_info'],
			'logistics_info': args['logistics_info']
		})
		product_unverified = mall_models.ProductUnverified.select().dj_where(product_id=product_id).first()
		if product_unverified:
			mall_models.ProductUnverified.update(product_data=product_data).dj_where(product_id=product_id).execute()
		else:
			mall_models.ProductUnverified.create(
				product_id = product_id,
				product_data = product_data
			)

		mall_models.Product.update(is_updated=True).dj_where(id=self.id).execute()

	def submit_verify(self):
		"""
		提交审核
		"""
		mall_models.Product.update(
			status=mall_models.PRODUCT_STATUS['SUBMIT']
		).dj_where(id=self.id).execute()

		send_product_message.send_product_change(self.get_corp().id, self.id)

	def verify_modifications(self):
		"""
		审核通过商品的编辑内容
		"""
		product_id = self.id
		product_data = json.loads(mall_models.ProductUnverified.select().dj_where(product_id=product_id).get().product_data)
		mall_models.Product.update(is_updated=False, status=mall_models.PRODUCT_STATUS['NOT_YET']).dj_where(id=self.id).execute()
		from business.product.update_product_service import UpdateProductService
		corp = self.get_corp()
		update_product_service = UpdateProductService.get(corp)
		update_product_service.update_product(self.id, {
			'corp': corp,
			'base_info': product_data['base_info'],
			'models_info': product_data['models_info'],
			'logistics_info': product_data['logistics_info'],
			'image_info': product_data['image_info']
		})

	def refuse_verify(self, reason):
		"""
		驳回
		"""
		mall_models.ProductRefuseLogs.create(
			product_id = self.id,
			refuse_reason = reason
		)

		mall_models.Product.update(
			status=mall_models.PRODUCT_STATUS['REFUSED']
		).dj_where(id=self.id).execute()

		#发送钉钉消息
		send_product_message.send_reject_product_ding_message(self.owner_id, self.id, reason)


	# 如果规格有图片就显示，如果没有，使用缩略图
	@property
	def order_thumbnails_url(self):
		"""
		[property] 订单中的缩略图
		"""
		'''
		if hasattr(self, 'custom_model_properties') and self.custom_model_properties:
			for model in self.custom_model_properties:
				if model['property_pic_url']:
					return model['property_pic_url']
		'''
		context = self.context
		if not 'order_thumbnails_url' in context:
			context['order_thumbnails_url'] = self.thumbnails_url
		return context['order_thumbnails_url']

	@order_thumbnails_url.setter
	def order_thumbnails_url(self, url):
		"""
		[property setter] 订单中的缩略图
		"""
		# self.context['order_thumbnails_url'] = url
		self.thumbnails_url = url

	@property
	def hint(self):
		"""
		[property] 判断商品是否被禁止使用全场优惠券
		"""
		corp = self.context['corp']
		forbidden_coupon_product_ids = ForbiddenCouponProductIds.get_for_corp({
			'corp': corp
		}).ids
		if self.id in forbidden_coupon_product_ids:
			return u'该商品不参与全场优惠券使用！'
		else:
			return u''

	def is_on_shelve(self):
		"""
		判断商品是否是上架状态
		"""
		return self.shelve_type == 'on_shelf'

	def set_shelve_type(self, shelve_type):
		"""
		设置商品的货架状态
		"""
		self.shelve_type = shelve_type

	def apply_discount(self, webapp_user):
		"""
		执行webapp_user携带的折扣信息

		Parameters
			[in] webapp_user
		"""
		if self.is_member_product:
			_, discount_value = webapp_user.member.discount
			discount = discount_value / 100.0

			self.price_info['min_price'] = round(self.price_info['min_price'] * discount, 2) #折扣后的价格
			self.price_info['max_price'] = round(self.price_info['max_price'] * discount, 2) #折扣后的价格
			self.price_info['display_price'] = round(float(self.price_info['display_price']) * discount, 2) #折扣后的价格

			for model in self.models:
				model.price = round(model.price * discount, 2)

	@cached_context_property
	def __deleted_models(self):
		return list(mall_models.ProductModel.select().dj_where(product_id=self.id, is_deleted=True))

	def get_specific_model(self, model_name):
		"""
		获得特定的商品规格信息

		@param [in] model_name: 商品规格名

		@return ProductModel对象

		注意，这里返回的有可能是被删除的规格，使用者应该通过product_model.is_deleted来判断
		"""
		models = self.models
		if not models:
			watchdog.info({
				'msg': u'商品models为空！',
				'product_id': self.id,
				'product_detail': self.to_dict()
			})
			Product.__fill_model_detail(self.context['corp'], [self], True)
			models = self.models
		candidate_models = filter(lambda m: m.name == model_name if m else False, models)
		if len(candidate_models) > 0:
			model = candidate_models[0]
			return model
		else:
			candidate_models = filter(lambda m: m.name == model_name if m else False, self.__deleted_models)
			if len(candidate_models) > 0:
				model = candidate_models[0]
				return model
			else:
				return None

	# def after_from_dict(self):
	# 	product_models = []
	# 	for model_dict in self.models:
	# 		product_models.append(ProductModel.from_dict(model_dict))
	# 	self.models = product_models

	# 	if self.promotion:
	# 		self.promotion = PromotionRepository.get_promotion_from_dict_data(self.promotion)

	# 		if not self.promotion.is_active():
	# 			#缓存中的促销已过期
	# 			self.promotion = None

	# 	if self.integral_sale:
	# 		self.integral_sale = PromotionRepository.get_promotion_from_dict_data(self.integral_sale)

	# 		if not self.integral_sale.is_active():
	# 			self.integral_sale = None

	@cached_context_property
	def supplier_name(self):
		try:
			# 非微众系列商家
			if not self.context['corp'].user_profile.webapp_type:
				return ''
			# 手动添加的供货商
			if self.supplier:
				return Supplier.get_supplier_name(self.supplier)
			# 同步的供货商
			relation = mall_models.WeizoomHasMallProductRelation.select().dj_where(weizoom_product_id=self.id).first()
			if relation:
				supplier_name = account_model.UserProfile.select().dj_where(user_id=relation.mall_id).first().store_name
			else:
				supplier_name = ''

			return supplier_name
		except:
			watchdog.alert(unicode_full_stack())
			return ''

	@cached_context_property
	def supplier_postage_config(self):
		if not self.supplier:
			return {}

		supplier_postage_config_model = mall_models.SupplierPostageConfig.select().dj_where(
				supplier_id=self.supplier,
				status=True
			).first()
		if supplier_postage_config_model and supplier_postage_config_model.postage:
			return {
				'condition_type': supplier_postage_config_model.condition_type,
				'condition_money': supplier_postage_config_model.condition_money,
				'postage': supplier_postage_config_model.postage
			}
		else:
			return {}

	@cached_context_property
	def use_supplier_postage(self):
		if not self.supplier:
			return False
		supplier_model = mall_models.Supplier.select().dj_where(id=self.supplier).first()
		user_profile = account_model.UserProfile.select().dj_where(user_id=supplier_model.owner_id).first()
		if supplier_model.name == u'自营' and user_profile.webapp_type == 3:
			return False
		else:
			return True


	def is_supplied_by_supplier(self):
		"""
		判断商品是否由供应商提供
		"""
		return self.supplier != 0

	# def _post_action(self):
	# 	"""
	# 	内部方法，将mall_model.Product中与Product领域对象同名的属性做调整，使之符合业务领域
	# 	仅在product内部调用，外部不要使用此方法
	# 	"""
	# 	if self.supplier == 0:
	# 		self.supplier = None

	def update_cps_promotion_info(self, promotion_id, money, stock, sale_count, total_money, status):
		"""
		:param status 推广状态 PROMOTING: 推广中 PROMOTE_OVER: # 推广结束"

		"""
		mall_models.PromoteDetail.update(promote_money=money,
										 promote_sale_count=sale_count,
										 promote_total_money=total_money,
										 promote_status=status,
										 promote_stock=stock)\
			.dj_where(product_id=self.id,
					  id=promotion_id).execute()

	def apply_cps_promotion(self, money, stock, time_from, time_to, sale_count, total_money):
		# 如果商品正在推广,那么就不能再次推广
		if mall_models.PromoteDetail.select().dj_where(product_id=self.id,
													   promote_status=mall_models.PROMOTING).count() > 0:
			return False

		promotion_model = mall_models.PromoteDetail.create(product_id=self.id,
														   promote_money=money,
														   promote_time_from=time_from,
														   promote_time_to=time_to,
														   promote_sale_count=sale_count,
														   promote_total_money=total_money,
														   promote_stock=stock)
		# 将所有代销该商品的平台,都更新成未处理
		mall_models.ProductPool.update(is_cps_promotion_processed=False).dj_where(product_id=self.id).execute()
		cps_promotion_info = {
			'money': money,
			'time_from': time_from,
			'time_to': time_to,
			'sale_count': sale_count,
			'total_money': total_money,
			'stock': stock,
			'id': promotion_model.id,
			'is_cps_promotion_processed': True
		}
		self.cps_promoted_info = cps_promotion_info

		return True

	def customize_price(self, price, product_model_id):
		"""
		社群可以修改商品价格
		"""
		corp_id = self.get_corp().id
		mall_models.ProductCustomizedPrice.delete().dj_where(corp_id=corp_id, product_id=self.id, product_model_id=product_model_id).execute()
		mall_models.ProductCustomizedPrice.create(
			corp_id = corp_id,
			product_id = self.id,
			product_model_id = product_model_id,
			price = price
		)