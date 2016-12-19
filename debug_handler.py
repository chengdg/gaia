# -*- coding: utf-8 -*-
"""
异常时变量的解析，需要eaglet支持
"""
from business.order.delivery_item import DeliveryItem


def handle(vars):
	data = {}
	for var in vars:
		key = var['key']
		value = var['value']
		if isinstance(value, DeliveryItem):
			try:
				data['delivery_item'] = {
					'id': value.id
				}
			except BaseException as e:
				data[key] = {
					'error_type': str(e)
				}

	print('----data', data)

	return data
