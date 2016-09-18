# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models
from core import paginator
from core import dateutil

from db.mall import models as mall_models
from db.mall import promotion_models 
from business.mall.product import Product
from business.account.user_profile import UserProfile

class ShopRemind(business_model.Model):
	"""
	店铺提醒集合
	此类 主要是首页店铺提醒功能
	"""
	__slots__ = (
		'onshelf_product_count',  # 在售商品数量
		'sellout_product_count',  # 库存不足商品
		'to_be_shipped_order_count',  # 待发货数量
		'refunding_order_count',  # 退款数量
		'flash_sale_count',  # 限时抢购数量
		'premium_sale_count',  # 买赠数量
		'integral_sale_count',  # 积分应用数量
		'coupon_count',  # 优惠卷数量
		'red_envelope_count'   # 分享红包数量
	)
	
	def __init__(self, model=None):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)

	@staticmethod
	@param_required(['owner_id', 'with_options'])
	def from_owner_id(args):
		shop_remind = ShopRemind()
		options = args['with_options']
		ShopRemind.__with_options(args['owner_id'], shop_remind, options)
		return shop_remind


	@staticmethod
	def __with_options(owner_id, shop_remind, options):
		'''
			根据options传入的值获取
			'with_onshelf_product_count',  # 在售商品数量
			'with_sellout_product_count',  # 库存不足商品
			'with_to_be_shipped_order_count',  # 待发货数量
			'with_refunding_order_count',  # 退款数量
			'with_flash_sale_count',  # 限时抢购数量
			'with_premium_sale_count',  # 买赠数量
			'with_integral_sale_count',  # 积分应用数量
			'with_coupon_count',  # 优惠卷数量
			'with_red_envelope_count'   # 分享红包数量

		'''
		if options.get('with_onshelf_product_count', None):
			shop_remind.__onshelf_product_count(owner_id)

		if options.get('with_sellout_product_count', None):
			shop_remind.__sellout_product_count(owner_id)

		if options.get('with_to_be_shipped_order_count', None):
			shop_remind.__to_be_shipped_order_count(owner_id)

		if options.get('with_refunding_order_count', None):
			shop_remind.__refunding_order_count(owner_id)

		if options.get('with_flash_sale_count', None):
			shop_remind.__flash_sale_count(owner_id)
		
		if options.get('with_premium_sale_count', None):
			shop_remind.__premium_sale_count(owner_id)
		
		if options.get('with_integral_sale_count', None):
			shop_remind.__integral_sale_count(owner_id)
		
		if options.get('with_coupon_count', None):
			shop_remind.__coupon_count(owner_id)
		
		if options.get('with_red_envelope_count', None):
			shop_remind.__red_envelope_count(owner_id)


	def __onshelf_product_count(self, owner_id):
		#在售商品数
		products = mall_models.Product.select().dj_where(owner_id=owner_id, shelve_type=mall_models.PRODUCT_SHELVE_TYPE_ON)
		self.onshelf_product_count = products.count()

	def __sellout_product_count(self, owner_id):
		#库存不足商品数
		onshelf_products = Product.from_onshelf_products({
				'owner_id': owner_id, 
				'fill_options': {
					'with_product_model': True
				}
			})
		sellout_products = []
		for product in onshelf_products:
			for model in product.models:
				if model and model['stock_type'] ==  mall_models.PRODUCT_STOCK_TYPE_LIMIT and model['stocks'] <= 0:
					sellout_products.append(product)
					break
		self.sellout_product_count = len(sellout_products)

	def __to_be_shipped_order_count(self, owner_id):
		#待发货订单数
		user_profile = UserProfile.from_user_id({'user_id': owner_id})
		order = mall_models.Order.select().dj_where(
			webapp_id=user_profile.webapp_id,
			status=mall_models.ORDER_STATUS_PAYED_NOT_SHIP
		)
		self.to_be_shipped_order_count = order.count()

	def __refunding_order_count(self, owner_id):
		#退款中订单数
		user_profile = UserProfile.from_user_id({'user_id': owner_id})
		order = mall_models.Order.select().dj_where(
			webapp_id=user_profile.webapp_id,
			status__in=[mall_models.ORDER_STATUS_REFUNDING, mall_models.ORDER_STATUS_GROUP_REFUNDING]
		)
		self.refunding_order_count = order.count()

	def __flash_sale_count(self, owner_id):
		#即将到期的限时抢购活动数
		self.flash_sale_count = self._get_expiring_promotion_count(owner_id, promotion_models.PROMOTION_TYPE_FLASH_SALE)

	def __premium_sale_count(self, owner_id):
		#即将到期的买赠活动数
		self.premium_sale_count = self._get_expiring_promotion_count(owner_id, promotion_models.PROMOTION_TYPE_PREMIUM_SALE)

	def __integral_sale_count(self, owner_id):
		#即将到期的积分应用活动数
		self.integral_sale_count = self._get_expiring_promotion_count(owner_id, promotion_models.PROMOTION_TYPE_INTEGRAL_SALE)

	def __coupon_count(self, owner_id):
		#即将到期的优惠券活动数
		self.coupon_count = self._get_expiring_promotion_count(owner_id, promotion_models.PROMOTION_TYPE_COUPON)

	def __red_envelope_count(self, owner_id):
		#即将到期的分享红包活动数
		red_envelopes = promotion_models.RedEnvelopeRule.select().dj_where(
			owner_id=owner_id,
			status=True,
			limit_time=True,
			is_delete=False,
			end_time__lte=dateutil.get_tomorrow_str('today')
		)
		red_envelope_ids = []
		for red in red_envelopes:
			is_timeout = False if red.end_time > datetime.now() else True
			if not is_timeout:
				red_envelope_ids.append(red.id)
		self.red_envelope_count = len(red_envelope_ids)

	def _get_expiring_promotion_count(self, owner_id, promotion_type):
		"""
		即将到期的促销活动数
		"""
		return promotion_models.Promotion.select().dj_where(
			owner_id=owner_id,
			status=promotion_models.PROMOTION_STATUS_STARTED,
			type=promotion_type,
			end_date__lte=dateutil.get_tomorrow_str('today')
		).count()
