# -*- coding: utf-8 -*-
from eaglet.core import paginator

from db.mall import promotion_models
from business import model as business_model
from business.mall.promotion.promotion import Promotion
from business.mall.promotion.fill_promotion_detail_service import FillPromotionDetailService
from business.common.filter_parser import FilterParser
from db.mall import models as db_models


class PromotionRepository(business_model.Service):

	def get_promotion_by_ids(self, promotion_ids, fill_options=None):
		models = promotion_models.Promotion.select().dj_where(id__in=promotion_ids,
															  owner_id=self.corp.id)
		promotions = [Promotion(model) for model in models]
		fill_promotion_detail_service = FillPromotionDetailService(self.corp)
		fill_promotion_detail_service.fill_detail(promotions, self.corp, fill_options)
		return promotions

	def delete_promotions(self, promotion_ids):
		promotion_models.Promotion.update(
			status=promotion_models.PROMOTION_STATUS_DELETED
		).dj_where(id__in=promotion_ids).execute()
		return True

	def get_promotion_by_id(self, promotion_id, fill_options=None):
		promotions = self.get_promotion_by_ids([promotion_id], fill_options=fill_options)
		return promotions[0] if promotions else None

	def search_premium_sale_promotions(self, page_info, fill_options=None, filters=None):
		"""
		搜索买赠的促销活动
		"""
		filters = filters if filters else {}
		filters['__f-type-equal'] = promotion_models.PROMOTION_TYPE_PREMIUM_SALE
		options = {
			'order_options': ['-start_date']
		}
		promotions, pageinfo = self.get_promotions(page_info, fill_options=fill_options, options=options,
												   filters=filters)
		return promotions, pageinfo

	def search_flash_sale_promotions(self, page_info, fill_options=None, filters=None):
		"""
		搜索限时抢购的促销活动
		"""
		filters = filters if filters else {}
		filters['__f-type-equal'] = promotion_models.PROMOTION_TYPE_FLASH_SALE
		options = {
			'order_options': ['-start_date']
		}
		promotions, pageinfo = self.get_promotions(page_info, fill_options=fill_options, options=options,
												   filters=filters)
		return promotions, pageinfo

	def search_integral_sale_promotions(self, page_info, fill_options=None, filters=None):
		"""
		搜索积分应用的促销活动
		"""
		filters = filters if filters else {}
		filters['__f-type-equal'] = promotion_models.PROMOTION_TYPE_INTEGRAL_SALE
		options = {
			'order_options': ['-start_date']
		}
		promotions, pageinfo = self.get_promotions(page_info, fill_options=fill_options, options=options,
												   filters=filters)
		return promotions, pageinfo

	def __split_filters(self, filters):
		promotion_filter_values = {}
		premium_sale_filter_values = {}
		flash_sale_filter_values = {}
		product_filter_values = {}
		filter_parse_result = FilterParser.get().parse(filters)

		for filter_field_op, filter_value in filter_parse_result.items():
			items = filter_field_op.split('__')
			filter_field = items[0]
			op = None
			if len(items) > 1:
				op = items[1]
			filter_category = None
			should_ignore_field = False
			if filter_field == 'id' or filter_field == 'status' or filter_field == 'type':
				filter_category = promotion_filter_values
			elif filter_field == 'product_name':
				filter_field = 'name'
				filter_category = product_filter_values
			elif filter_field == 'start_date' or filter_field == 'end_date' or filter_field == 'barcode':
				filter_category = product_filter_values
			if not should_ignore_field:
				if op:
					filter_field_op = '%s__%s' % (filter_field, op)
				filter_category[filter_field_op] = filter_value
		# 如果有补充条件,可以手动补充
		promotion_filter_values['status__in'] = [promotion_models.PROMOTION_STATUS_STARTED,
												 promotion_models.PROMOTION_STATUS_NOT_START,
												 promotion_models.PROMOTION_STATUS_FINISHED,]
		promotion_filter_values['owner_id'] = self.corp.id
		return {
			'product': product_filter_values,
			'premium_sale': premium_sale_filter_values,
			'flash_sale': flash_sale_filter_values,
			'promotion': promotion_filter_values,
		}

	def __get_promotion_order_options(self, options):
		type2field = {
			'start_date': promotion_models.Promotion.start_date
		}

		fields = []
		for order_type in options.get('order_options', []):
			is_desc = False
			if order_type[0] == '-':
				is_desc = True
				order_type = order_type[1:]

			field = type2field[order_type]
			if is_desc:
				field = field.desc()

			fields.append(field)

		return fields

	def get_promotions(self, page_info, fill_options=None, options=None, filters=None):
		type2fiters = self.__split_filters(filters=filters)
		order_options = self.__get_promotion_order_options(options=options)

		promotion_filters = type2fiters['promotion']
		promotions = promotion_models.Promotion.select().dj_where(**promotion_filters)

		# product_filters = type2fiters['product']
		# if product_filters:
		# 	products = self.corp.product_pool.search_products_by_filters(**product_filters)
		# 	product_ids = [product.id for product in products]
		# 	relations = promotion_models.ProductHasPromotion.select().dj_where(product_id__in=product_ids)
		# 	promotions = promotions.dj_where(id__in=[re.promotion_id for re in relations])
		premium_sale_filters = type2fiters['premium_sale']
		if premium_sale_filters:
			premium_sales = promotion_models.PremiumSale.select().dj_where(**premium_sale_filters)
			promotions = promotions.dj_where(detail_id__in=[premium_sale.id for premium_sale in premium_sales])
		flash_sale_filters = type2fiters['flash_sale']
		if flash_sale_filters:
			pass
		product_filters = type2fiters['product']
		if product_filters:
			# 根据promotion查处所有这些促销的商品
			promotion_ids = [promotion.id for promotion in promotions]
			relations = promotion_models.ProductHasPromotion.select().dj_where(promotion_id__in=promotion_ids)
			product_filters['id__in'] = [relation.product_id for relation in relations]
			# 根据商品id和其他商品条件搜索出商品
			products = self.corp.product_pool.search_products_by_filters(**product_filters)
			product_ids = [product.id for product in products]
			# 根据正确的商品搜索出促销
			relations = promotion_models.ProductHasPromotion.select().dj_where(product_id__in=product_ids)
			promotions = promotions.dj_where(id__in=[re.promotion_id for re in relations])
		if order_options:
			promotions = promotions.order_by(*order_options)

		pageinfo, promotions = paginator.paginate(promotions, page_info.cur_page, page_info.count_per_page)
		promotions = [Promotion(promotion) for promotion in promotions]
		fill_promotion_detail_service = FillPromotionDetailService(self.corp)
		fill_promotion_detail_service.fill_detail(promotions, self.corp, fill_options)

		return promotions, pageinfo

	def enable_promotion(self, promotion_id):
		"""
        开启促销活动
        promotion_ids: [promotion_id,...]
        """
		promotion_models.Promotion.update(
			status=promotion_models.PROMOTION_STATUS_STARTED
		).dj_where(id=promotion_id,
				   status=promotion_models.PROMOTION_STATUS_NOT_START,
				   ).execute()
		return True

	def disable_promotion(self, promotion_id):
		"""
        关闭撤销活动
        """
		promotion_models.Promotion.update(
			status=promotion_models.PROMOTION_STATUS_FINISHED
		).dj_where(id=promotion_id,
				   status=promotion_models.PROMOTION_STATUS_STARTED).execute()
		return True
