# -*- coding: utf-8 -*-


from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.product_config import ProductConfig
from business.common.page_info import PageInfo


class AProductCreationOption(api_resource.ApiResource):
	"""
	商品配置相关信息
	"""
	app = "product"
	resource = "creation_option"

	@staticmethod
	def __load_pay_interfaces(corp):
		"""
		获取支付接口配置
		"""
		pay_interfaces = corp.pay_interface_repository.get_active_pay_interfaces()
		datas = []
		for pay_interface in pay_interfaces:
			data = {
				"id": pay_interface.id,
				"type": pay_interface.type,
				"name": pay_interface.name
			}
			datas.append(data)

		return datas

	@staticmethod
	def __load_product_property_templates(corp):
		"""
		获取商品属性模板集合
		"""
		product_property_templates = corp.product_property_template_repository.get_templates()
		datas = []
		for property_template in product_property_templates:
			data = {
				"id": property_template.id,
				"name": property_template.name
			}
			datas.append(data)

		return datas

	@staticmethod
	def __load_categories(corp):
		"""
		获取分类集合
		"""
		target_page = PageInfo(1, 1000)
		categories, _ = corp.category_repository.get_all_categories(target_page)
		datas = []
		for category in categories:
			datas.append({
				"id": category.id,
				"name": category.name
			})

		return datas


	@param_required(['corp_id'])
	def get(args):
		corp = args['corp']
		config = {}

		#支付接口配置
		config['pay_interfaces'] = AProductCreationOption.__load_pay_interfaces(corp)

		#运费模板
		config['postage_config_info'] = None

		#属性模板
		config['property_templates'] = AProductCreationOption.__load_product_property_templates(corp)

		#分类信息
		config['categories'] = AProductCreationOption.__load_categories(corp)

		return config
