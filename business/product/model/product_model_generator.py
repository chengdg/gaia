# -*- coding: utf-8 -*-
"""
商品规格生成器
"""

import json
from bs4 import BeautifulSoup
import math
from datetime import datetime

from eaglet.decorator import param_required
#from wapi import wapi_utils
from eaglet.core.cache import utils as cache_util
from db.mall import models as mall_models
from db.mall import promotion_models
from db.account import models as account_models
from eaglet.core import watchdog
from business import model as business_model
import settings
from business.product.model.product_model import ProductModel


class ProductModelGenerator(business_model.Service):
	"""
	商品规格生成器
	"""
	def __get_all_model_property_info(self, products, is_enable_model_property_info):
		"""
		获取系统中所有的商品规格属性信息

		@param[in] is_enable_model_property_info: 是否启用商品规格属性信息

		@return
			id2property <id, property>映射
			id2propertyvalue <id, property_value>映射
		"""
		if not is_enable_model_property_info:
			return {}, {}

		#获得product所属的corp的id集合
		corp_ids = set([product.owner_id for product in products])

		#获得property集合
		properties = list(mall_models.ProductModelProperty.select().dj_where(owner__in=list(corp_ids)))
		property_ids = [property.id for property in properties]
		id2property = dict([(str(property.id), property) for property in properties])
		
		#获得property value集合
		id2propertyvalue = {}
		for value in mall_models.ProductModelPropertyValue.select().dj_where(property__in=property_ids):
			id = '%d:%d' % (value.property_id, value.id)
			id2propertyvalue[id] = value

		_id2property = {}
		_id2propertyvalue = {}
		for id, property in id2property.items():
			_id2property[id] = {
				"id": property.id,
				"type": 'text' if property.type == mall_models.PRODUCT_MODEL_PROPERTY_TYPE_TEXT else 'image',
				"name": property.name,
				"values": []
			}

		for id, value in id2propertyvalue.items():
			_property_id, _value_id = id.split(':')
			_property = _id2property[_property_id]
			data = {
				'property_id': _property['id'],
				'property_name': _property['name'],
				'property_type': _property['type'],
				"id": value.id,
				"name": value.name,
				"image": value.pic_url
			}
			_id2propertyvalue[id] = data
			_property['values'].append(data)

		return _id2property, _id2propertyvalue

	def fill_models_for_products(self, products, is_enable_model_property_info, divide_info=None):
		"""
		为商品集合填充规格信息

		@param[in, out] products: 待填充规格信息的商品集合，填充后，product将获得models, used_system_model_properties, is_use_custom_model三个属性
		@param[in] is_enable_model_property_info: 是否为model填充与model相关的系统商品规格信息
		"""
		id2product = dict()
		product_ids = list()
		for product in products:
			id2product[product.id] = product
			product_ids.append(product.id)

		id2property, id2propertyvalue = self.__get_all_model_property_info(products, is_enable_model_property_info)

		if divide_info:
			settlement_type = divide_info.settlement_type
			divide_rebate = divide_info.divide_rebate
			product_model_id2price = {c.product_model_id: c.price for c in
									  mall_models.ProductCustomizedPrice.select().dj_where(corp_id=self.corp.id, product_id__in=product_ids)}

		# 获取所有models
		product2models = {}
		#product2deleted_models = {}
		for db_model in mall_models.ProductModel.select().dj_where(product_id__in=product_ids, is_deleted=False):
			if db_model.is_deleted:
				pass
				#product_model = ProductModel(db_model, id2property, id2propertyvalue)
				#product2deleted_models.setdefault(db_model.product_id, []).append(product_model)
			else:
				product_model = ProductModel(db_model, id2property, id2propertyvalue)
				if divide_info:
					"""
					社群的毛利、毛利率
					固定扣点+溢价: 商品售价(或者社群修改价) * 社群扣点
					毛利分成: {
						non_cps: (商品售价 - 微众售价) * 社群毛利点  ==> 社群毛利,
								 (商品售价 - 微众售价)/商品售价 * 社群毛利点 ==>社群毛利率
					}
					"""
					customized_price = product_model_id2price.get(product_model.id, product_model.price)
					if product_model.price == 0:
						gross_profit = 0
						gross_profit_rate = 0
					else:
						if settlement_type == account_models.ACCOUNT_DIVIDE_TYPE_FIXED:  # 固定扣点+溢价
							gross_profit = customized_price * divide_rebate / 100
							gross_profit_rate = divide_rebate
						elif settlement_type == account_models.ACCOUNT_DIVIDE_TYPE_PROFIT:  # 毛利分成
							gross_profit = (product_model.price - product_model.purchase_price) * divide_rebate / 100
							gross_profit_rate = gross_profit / product_model.price * 100

					product_model.gross_profit = '%.2f' % gross_profit
					product_model.gross_profit_rate = '%.2f' % gross_profit_rate
					product_model.customized_price = '%.2f' % customized_price
				product2models.setdefault(db_model.product_id, []).append(product_model)

		for product_id, product_models in product2models.items():
			product = id2product[product_id]
			if len(product_models) == 1 and product_models[0].is_standard_model():
				product.is_use_custom_model = False
				product.standard_model = product_models[0]
				product.custom_models = []
				product.gross_profit_info = {
					'gross_profit': product.standard_model.gross_profit,
					'gross_profit_rate': product.standard_model.gross_profit_rate
				}
			else:
				product.is_use_custom_model = True
				product.standard_model = None
				product.custom_models = [model for model in product_models if not model.is_standard_model()]
				if divide_info and not divide_info.settlement_type == account_models.ACCOUNT_DIVIDE_TYPE_FIXED:#非固定底价方式，选择毛利率最大的
					product.custom_models = sorted(product.custom_models, key=lambda k: k.gross_profit_rate, reverse=True)
				product.gross_profit_info = {
					'gross_profit': product.custom_models[0].gross_profit,
					'gross_profit_rate': product.custom_models[0].gross_profit_rate
				}

			#self.__fill_used_product_model_property(product)


	def __fill_used_product_model_property(self, product):
		"""
		填充商品中使用了的商品规格属性的信息

		从models中构建used_system_model_properties，
		加入商品有以下两个规格
		1. {property:'颜色', value:'红色'}, {property:'尺寸', value:'M'}
		2. {property:'颜色', value:'黄色'}, {property:'尺寸', value:'M'}

		则合并后的used_system_model_properties为:
		[{
			property: '颜色',
			values: ['红色', '黄色']
		}, {
			property: '尺寸',
			values: ['M']
		}]
		"""
		id2property = {}
		if product.is_use_custom_model:
			for model in product.custom_models:
				if not model:
					continue

				if model.property_values:
					for model_property_value in model.property_values:
						model_property_value['type'] = 'product_model_property_value'
						property_id = model_property_value['propertyId']

						property_info = id2property.get(property_id, None)
						if property_info:
							#model_property_value可能会有重复
							if not model_property_value['id'] in property_info['added_value_set']:
								property_info['values'].append(model_property_value)
								property_info['added_value_set'].add(model_property_value['id'])
						else:
							added_value_set = set()
							added_value_set.add(model_property_value['id'])
							property_info = {
								"type": "product_model_property",
								"id": property_id,
								"name": model_property_value['propertyName'],
								"added_value_set": added_value_set,
								"values": [model_property_value]
							}
							id2property[property_id] = property_info

			#获得properties，并进行必要的排序
			properties = id2property.values()
			for property in properties:
				del property['added_value_set']
				property['values'].sort(lambda x,y: cmp(x['id'], y['id']))
			properties.sort(lambda x,y: cmp(x['id'], y['id']))
			product.used_system_model_properties = properties

		else:
			product.used_system_model_properties = None
