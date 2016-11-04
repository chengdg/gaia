# -*- coding: utf-8 -*-

from business import model as busniess_model
from db.mall import promotion_models
from db.mall import models as mall_models
import settings


class FillPromotionDetailService(busniess_model.Service):
	"""
	对促销集合批量填充详情服务
	"""

	@staticmethod
	def __get_promotion_detail_class(promotion_type):
		"""
		获取促销特定数据对应的业务对象的class

		Parameters
			[in] promotion_type: 促销类型

		Returns
			促销特定数据的class（比如FlashSale）
		"""
		DetailClass = None
		if promotion_type == promotion_models.PROMOTION_TYPE_FLASH_SALE:
			DetailClass = promotion_models.FlashSale
		elif promotion_type == promotion_models.PROMOTION_TYPE_PRICE_CUT:
			DetailClass = promotion_models.PriceCut
		elif promotion_type == promotion_models.PROMOTION_TYPE_INTEGRAL_SALE:
			DetailClass = promotion_models.IntegralSale
		elif promotion_type == promotion_models.PROMOTION_TYPE_PREMIUM_SALE:
			DetailClass = promotion_models.PremiumSale
		elif promotion_type == promotion_models.PROMOTION_TYPE_COUPON:
			DetailClass = promotion_models.CouponRule

		return DetailClass

	@staticmethod
	def __fill_integral_sale_rule_details(integral_sales):
		"""
		填充与积分应用相关的`积分应用规则`
		"""
		integral_sale_ids = []
		id2sale = {}
		for integral_sale in integral_sales:
			integral_sale_detail_id = integral_sale.context['detail_id']
			integral_sale.rules = []
			integral_sale_ids.append(integral_sale_detail_id)
			id2sale[integral_sale_detail_id] = integral_sale

		integral_sale_rules = list(
			promotion_models.IntegralSaleRule.select().dj_where(integral_sale_id__in=integral_sale_ids))
		for integral_sale_rule in integral_sale_rules:
			integral_sale_id = integral_sale_rule.integral_sale_id
			id2sale[integral_sale_id].add_rule(integral_sale_rule)

		for integral_sale in integral_sales:
			integral_sale.calculate_discount()

	@staticmethod
	def __fill_premium_products_details(premium_sales, corp):
		"""
		填充与限时抢购相关的`促销商品详情`
		"""
		premium_sale_ids = []
		id2sale = {}
		for premium_sale in premium_sales:
			prenium_sale_detail_id = premium_sale.context['detail_id']
			premium_sale.premium_products = []
			premium_sale_ids.append(prenium_sale_detail_id)
			id2sale[prenium_sale_detail_id] = premium_sale

		premium_sale_products = promotion_models.PremiumSaleProduct.select().dj_where(owner_id=corp.id,
																					  premium_sale_id__in=premium_sale_ids)
		product_ids = [premium_sale_product.product_id for premium_sale_product in premium_sale_products]

		products = mall_models.Product.select().dj_where(id__in=product_ids)

		if corp.mall_type:
			pool_product_list = [p.product_id for p in mall_models.ProductPool.select().dj_where(woid=corp.id,
																								 status=mall_models.PP_STATUS_ON)]
		else:
			pool_product_list = []

		id2product = dict([(product.id, product) for product in products])

		for premium_sale_product in premium_sale_products:
			# add by duhao当赠品和主商品不是一个供应商时，需要把赠品的供应商id变为和主商品一样，以便和主商品显示在同一个子订单中
			premium_sale_id = premium_sale_product.premium_sale_id
			promotion = promotion_models.Promotion.get(type=promotion_models.PROMOTION_TYPE_PREMIUM_SALE,
													   detail_id=premium_sale_id)
			product2promotion = promotion_models.ProductHasPromotion.get(promotion=promotion.id)
			main_product = product2promotion.product

			product_id = premium_sale_product.product_id

			# realtime_stock = RealtimeStock.from_product_id({
			# 	'product_id': product_id
			# })
			# realtime_stock_dict = realtime_stock.model2stock.values()[0]

			product = id2product[product_id]

			if pool_product_list and product_id in pool_product_list:
				shelve_type = mall_models.PRODUCT_SHELVE_TYPE_ON
			else:
				shelve_type = product.shelve_type

			data = {
				'id': product.id,
				'name': product.name,
				'thumbnails_url': '%s%s' % (settings.IMAGE_HOST, product.thumbnails_url) if product.thumbnails_url.find(
					'http') == -1 else product.thumbnails_url,
				'original_premium_count': premium_sale_product.count,
				'premium_count': premium_sale_product.count,
				'premium_unit': premium_sale_product.unit,
				'premium_product_id': premium_sale_product.product_id,
				'supplier': main_product.supplier,
				# 'stock_type': realtime_stock_dict['stock_type'],
				# 'stocks': realtime_stock_dict['stocks'],
				'shelve_type': shelve_type,
				'is_deleted': product.is_deleted
			}
			id2sale[premium_sale_id].premium_products.append(data)


	def fill_detail(self, promotions, corp):
		"""
		为促销填充促销特定数据
		"""
		type2promotions = dict()
		for promotion in promotions:
			type2promotions.setdefault(promotion.type, []).append(promotion)
		for promotion_type, promotions in type2promotions.items():
			if promotion_type == promotion_models.PROMOTION_TYPE_PREMIUM_SALE:
				self.__fill_premium_products_details(promotions, corp)
			elif promotion_type == promotion_models.PROMOTION_TYPE_INTEGRAL_SALE:
				self.__fill_integral_sale_rule_details(promotions)
			else:
				raise ValueError('DetailClass(None) is not valid')