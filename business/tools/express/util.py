# -*- coding: utf-8 -*-

import os
import json

########################################################################
# get_express_company_json: 获得快递公司信息, 读取json文件
########################################################################
def get_express_company_json():
	base_path = os.path.abspath('.')
	path = os.path.join(base_path, 'business/tools/express/express_company.json')
	file = open(path, 'rb')
	data_json = json.load(file)
	return data_json



########################################################################
# get_name_by_id: 根据快递公司id，获取快递公司名称
########################################################################
def get_name_by_id(value):
	if not value:
		return ''
		
	data_json = get_express_company_json()
	for item in data_json:
		if item['id'] == value:
			return item['name']

	return ''


########################################################################
# get_name_by_value: 根据快递公司value，获取快递公司名称
########################################################################
def get_name_by_value(value):
	if not value:
		return ''
		
	data_json = get_express_company_json()
	for item in data_json:
		if item['value'] == value:
			return item['name']

	return value


########################################################################
# get_value_by_name: 根据快递公司名称，获取快递公司value
########################################################################
def get_value_by_name(name):
	if not name:
		return ''

	data_json = get_express_company_json()
	for item in data_json:
		if item['name'] == name:
			return item['value']

	return name
