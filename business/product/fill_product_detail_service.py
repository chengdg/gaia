# coding=utf-8
# -*- utf-8 -*-
from eaglet.decorator import param_required

from bdem import msgutil
from business import model as business_model

from business.product.product import Product
from business.product.product_model_generator import ProductModelGenerator
from db.mall import models as mall_models
from zeus_conf import TOPIC
from core import paginator


class FillProductDetailService(business_model.Service):
	"""
	对商品集合批量进行详情填充的服务
	"""
	def __fill_model_detail(self, corp, products, is_enable_model_property_info=False):
		"""填充商品规格相关细节
		向product中添加is_use_custom_model, models, used_system_model_properties三个属性
		"""
		if products[0].models:
			#已经完成过填充，再次进入，跳过填充
			return

		#TODO2: 因为这里是静态方法，所以目前无法使用product.context['corp']，构造基于Object的临时解决方案，需要优化
		product_model_generator = ProductModelGenerator.get(corp)
		product_model_generator.fill_models_for_products(products, is_enable_model_property_info)

	def __fill_display_price(self, products):
		"""根据商品规格，获取商品价格
		"""
		for product in products:
			if product.is_use_custom_model:
				custom_models = product.models
				if len(custom_models) == 1:
					#只有一个custom model，显示custom model的价格信息
					product_model = custom_models[0]
					product.price_info = {
						'display_price': str("%.2f" % product_model.price),
						'display_original_price': str("%.2f" % product_model.original_price),
						'display_market_price': str("%.2f" % product_model.market_price),
						'min_price': product_model.price,
						'max_price': product_model.price,
					}
				else:
					#有多个custom model，显示custom model集合组合后的价格信息
					prices = []
					market_prices = []
					for product_model in custom_models:
						if product_model.price > 0:
							prices.append(product_model.price)
						if product_model.market_price > 0:
							market_prices.append(product_model.market_price)

					if len(market_prices) == 0:
						market_prices.append(0.0)

					if len(prices) == 0:
						prices.append(0.0)

					prices.sort()
					market_prices.sort()
					# 如果最大价格和最小价格相同，价格处显示一个价格。
					if prices[0] == prices[-1]:
						price_range =  str("%.2f" % prices[0])
					else:
						price_range = '%s-%s' % (str("%.2f" % prices[0]), str("%.2f" % prices[-1]))

					if market_prices[0] == market_prices[-1]:
						market_price_range = str("%.2f" % market_prices[0])
					else:
						market_price_range = '%s-%s' % (str("%.2f" % market_prices[0]), str("%.2f" % market_prices[-1]))

					# 最低价
					min_price = prices[0]
					# 最高价
					max_price = prices[-1]

					product.price_info = {
						#'display_price': price_range,
						#'display_original_price': price_range,
						'display_price': min_price,
						'display_original_price': min_price,
						'display_market_price': market_price_range,
						'min_price': min_price,
						'max_price': max_price,
					}
			else:
				standard_model = None
				if product.models:
					standard_model = product.models[0]

				if standard_model:
					product.price_info = {
						'display_price': str("%.2f" % standard_model.price),
						'display_original_price': str("%.2f" % standard_model.original_price),
						'display_market_price': str("%.2f" % standard_model.market_price),
						'min_price': standard_model.price,
						'max_price': standard_model.price,
					}
				else:
					product.price_info = {
						'display_price': str("%.2f" % 0),
						'display_original_price': str("%.2f" % 0),
						'display_market_price': str("%.2f" % 0),
						'min_price': 0,
						'max_price': 0,
					}

	def fill_detail(self, products, options):
		"""填充各种细节信息

		此方法会根据options中的各种填充选项，填充相应的细节信息

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
		"""
		if len(products) == 0:
			return
			
		is_enable_model_property_info = options.get('with_model_property_info',False)
		product_ids = [product.id for product in products]

		for product in products:
			product.detail_link = '/mall/product/?id=%d&source=onshelf' % product.id

		if options.get('with_price', False):
			#price需要商品规格信息
			self.__fill_model_detail(self.corp, products, is_enable_model_property_info)
			self.__fill_display_price(products)

		if options.get('with_product_model', False):
			self.__fill_model_detail(self.corp, products, is_enable_model_property_info)

		if options.get('with_product_promotion', False):
			Product.__fill_promotion_detail(corp, products, product_ids)

		if options.get('with_image', False):
			Product.__fill_image_detail(corp, products, product_ids)

		if options.get('with_property', False):
			Product.__fill_property_detail(corp, products, product_ids)

		if options.get('with_selected_category', False):
			Product.__fill_category_detail(
				corp,
				products,
				product_ids,
				True)

		if options.get('with_all_category', False):
			Product.__fill_category_detail(
				corp,
				products,
				product_ids,
				False)

		if options.get('with_sales', False):
			Product.__fill_sales_detail(corp, products, product_ids)