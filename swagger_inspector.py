# -*- coding: utf-8 -*-
"""
swagger文档检查器
"""
import json
import os

from api import resources
from eaglet.core.api_resource import APPRESOURCE2CLASS


def get_resource_api_list(APPRESOURCE2CLASS):
	resource_api_list = []
	for (app_resource, resource_cls) in APPRESOURCE2CLASS.items():
		app, resource = app_resource.split('-')
		api_cls = resource_cls['cls']

		methods = filter(lambda method: hasattr(api_cls, method), ['get', 'post', 'put', 'delete'])

		for method in methods:
			resource_api_list.append("/{}/{}/-{}".format(app, resource, method))
	return resource_api_list


def get_swagger_api_list(swagger_path):
	swagger_api_list = []
	swagger_files = filter(lambda x: x.endswith("json"), os.listdir(swagger_path))

	for f in swagger_files:
		file = open(os.path.join(swagger_path, f), 'rb')
		data_json = json.load(file)
		path_list = data_json['paths'].keys()

		for path in path_list:
			methods = data_json["paths"][path].keys()

			if path[-1] != "/":
				path += "/"
			for method in methods:
				swagger_api_list.append("{}-{}".format(path, method))
	return swagger_api_list


resource_api_list = get_resource_api_list(APPRESOURCE2CLASS)

project_home = os.path.split(os.path.realpath(__file__))[0].split('.git')[0]

swagger_path = os.path.join(project_home, 'swagger')
swagger_api_list = get_swagger_api_list(swagger_path)

print('******result:******')

print(u"共有{}个API,{}个API文档".format(len(resource_api_list),len(swagger_api_list)))

missing_swagger_doc = list(set(resource_api_list) - set(swagger_api_list))
redundant_swagger_doc = list(set(swagger_api_list) - set(resource_api_list))
print(u"缺少文档：共计{}个. {}".format(len(missing_swagger_doc), str(missing_swagger_doc)))

print(u"有文档但没接口:共计{}个. {}".format(len(redundant_swagger_doc), str(redundant_swagger_doc)))
