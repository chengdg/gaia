# -*- coding: utf-8 -*-
import json

from eaglet.core import watchdog

from business import model as business_model

class EncodeProductService(business_model.Service):
	"""
	将Product对象转换为可输出dict的服务
	"""
	def get_base_info(self, product):
		"""
		获得商品的基础信息
		"""
		data = {
			"name": product.name,
			"type": product.type,
			"create_type": product.create_type,
			"bar_code": product.bar_code,
			"display_index": product.display_index,
			"min_limit": product.min_limit,
			"is_enable_bill": product.is_enable_bill,
			"promotion_title": product.promotion_title,
			"detail": product.detail,
			"sales": product.sales,
			"is_member_product": product.is_member_product,
			"is_delivery": product.is_delivery,
			"sync_at": product.sync_at.strftime('%Y-%m-%d %H:%M') if product.sync_at else None,
			"created_at": product.created_at.strftime('%Y-%m-%d %H:%M'),
			"thumbnails_url": product.thumbnails_url,
		}

		return data

	def get_models_info(self, product):
		"""
		获得商品的models_info数据
		"""
		models_info = {
			'is_use_custom_model': False,
			'standard_model': None,
			'custom_models': [],
			'used_system_model_properties': None
		}
		models_info['is_use_custom_model'] = product.is_use_custom_model

		standard_model = product.standard_model
		if standard_model:
			models_info['standard_model'] = {
				"id": standard_model.id,
				"name": standard_model.name,
				"price": standard_model.price,
				"purchase_price": standard_model.purchase_price,
				"weight": standard_model.weight,
				"stock_type": standard_model.stock_type,
				"stocks": standard_model.stocks,
				"user_code": standard_model.user_code
			}
		else:
			models_info['standard_model'] = None
		
		custom_models = product.custom_models
		if custom_models:
			for custom_model in custom_models:
				models_info['custom_models'].append({
					"id": custom_model.id,
					"name": custom_model.name,
					"price": custom_model.price,
					"purchase_price": custom_model.purchase_price,
					"weight": custom_model.weight,
					"stock_type": custom_model.stock_type,
					"stocks": custom_model.stocks,
					"user_code": custom_model.user_code,
					"property_values": custom_model.property_values,
					"property2value": custom_model.property2value
				})
		else:
			models_info['custom_models'] = []

		return models_info

	def get_image_info(self, product):
		"""
		获得商品的image_info数据
		"""
		image_info = {
			'thumbnails_url': product.thumbnails_url,
			'images': []
		}

		images = image_info['images']
		for image in product.swipe_images:
			images.append({
				"url": image['url'],
				#"link_url": image['link_url'],
				"width": image['width'],
				"height": image['height']
			})

		return image_info

	def get_categories(self, product):
		"""
		获得商品的category集合
		"""
		categories = []
		for category in product.categories:
			categories.append({
				"id": category['id'],
				"name": category['name']
			})

		return categories

	def get_pay_info(self, product):
		return {
			'is_use_online_pay_interface': product.is_use_online_pay_interface,
			'is_use_cod_pay_interface': product.is_use_cod_pay_interface
		}

	def get_properties(self, product):
		data = []
		for product_property in product.properties:
			data.append({
				"name": product_property['name'],
				"value": product_property['value']
			})

		return data

	def get_logistics_info(self, product):
		data = {
			'postage_type': product.postage_type,
			'unified_postage_money': product.unified_postage_money,
			'limit_zone_type': product.limit_zone_type,
			'limit_zone_id': product.limit_zone
		}

		return data

	def get_supplier_info(self, product):
		"""
		获得商品的supplier集合
		"""
		supplier = product.supplier
		if not supplier:
			return None

		data = {
			'id': supplier.id,
			'name': supplier.name,
			'type': supplier.type,
			'divide_type_info': None,
			'retail_type_info': None
		}

		if supplier.is_divide_type():
			divide_info = supplier.get_divide_info()
			data['divide_type_info'] = {
				"id": divide_info.id,
				"divide_money": divide_info.divide_money,
				"basic_rebate": divide_info.basic_rebate,
				"rebate": divide_info.rebate
			}
		elif supplier.is_retail_type():
			retail_info = supplier.get_retail_info()
			data['retail_type_info'] = {
				"id": retail_info.id,
				"rebate": retail_info.rebate
			}

		return data

	def get_classifications(self, product):
		"""
		获得商品的classification集合
		"""
		datas = []

		if len(product.classification_lists) > 0:
			classification_list = product.classification_lists[0]
			
			for classification in classification_list:
				datas.append({
					"id": classification.id,
					"level": classification.level,
					"name": classification.name
				})

		return datas

	def get_labels(self, product):
		"""
		获取商品标签的集合
		"""
		datas = []
		for label in product.labels:
			datas.append({
				'label_id': label.id,
				'label_name': label.name
			})
		return datas

	def get_gross_profit_info(self, product):
		gross_profit_info = product.gross_profit_info
		if gross_profit_info:
			return {
				'gross_profit': gross_profit_info['gross_profit'],
				'gross_profit_rate': gross_profit_info['gross_profit_rate']
			}
		else:
			return None

	def get_cps_promotion_info(self, product):
		cps_promotion_info = product.cps_promoted_info
		if cps_promotion_info:
			data = {
				'cps_gross_profit': cps_promotion_info['cps_gross_profit'],
				'cps_gross_profit_rate': cps_promotion_info['cps_gross_profit_rate'],
				'money': cps_promotion_info['money'],
				'time_from': cps_promotion_info['time_from'],
				'time_to': cps_promotion_info['time_to'],
				'sale_count': cps_promotion_info['sale_count'],
				'total_money': cps_promotion_info['total_money'],
				'stock': cps_promotion_info['stock'],
				'is_cps_promotion_processed': cps_promotion_info['is_cps_promotion_processed'],
				'id': cps_promotion_info['id']
			}
			return data
		return None

	def get_promotions(self, product):
		promotions = product.promotions
		datas = []
		for promotion in promotions:
			promotion_detail = promotion.detail
			if promotion.type_name == 'flash_sale':
				detail = {
					'count_per_period': promotion_detail.count_per_period,
					'limit_period': promotion_detail.limit_period,
					'count_per_purchase': promotion_detail.count_per_purchase,
					'promotion_price': promotion_detail.promotion_price
				}
			elif promotion.type_name == 'premium_sale':
				detail = {
					'count': promotion_detail.count,
					'is_enable_cycle_mode': promotion_detail.is_enable_cycle_mode,
					'premium_products': promotion_detail.premium_products
				}
			elif promotion.type_name == 'integral_sale':
				detail = {
					'rules': promotion_detail.rules,
					'discount': promotion_detail.discount,
					'discount_money': promotion_detail.discount_money,
					'is_permanant_active': promotion_detail.is_permanant_active
				}
			data = {
				'id': promotion.id,
				'name': promotion.name,
				'promotion_title': promotion.promotion_title,
				'type': promotion.type,
				'type_name': promotion.type_name,
				'status': promotion.status,
				'start_date': promotion.start_date,
				'end_date': promotion.end_date,
				'member_grade_id': promotion.member_grade_id,
				'detail': detail,
				'created_at': promotion.created_at
			}
			datas.append(data)
		return datas

	def encode(self, product):
		pass

	def get_price_info(self, product):
		price_info = product.price_info
		if price_info:
			return {
				'display_price': price_info['display_price'],
				'display_original_price': price_info['display_original_price'],
				'display_market_price': price_info['display_market_price'],
				'min_price': price_info['min_price'],
				'max_price': price_info['max_price'],
			}
