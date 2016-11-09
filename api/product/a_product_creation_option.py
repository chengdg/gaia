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
	def __load_postag_config(corp, product_id=None):
		"""
		获取创建/查看商品时候,运费模板配置信息
		"""
		# 普通平台,商品使用平台设置的,自应平台应该显示商品的供货商的默认运费模板
		if not corp.is_self_run_platform():
			postage_config = corp.postage_config_repository.get_corp_used_postage_config()
			return {
				'id': postage_config.id,
				'name': postage_config.name
			}
		else:
			if not product_id:
				return {'id': '', 'name': ''}
			product = corp.product_pool.get_product_by_id(product_id)
			postage_config = corp.postage_config_repository.get_supplier_used_postage_config(product.supplier_id)
			return {
				'id': postage_config.id,
				'name': postage_config.name
			}


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

	@staticmethod
	def __load_limit_zones(corp):
		"""
		获取限定区域信息
		"""
		limit_zones = corp.limit_zone_repository.get_limit_zones()
		datas = []
		for limit_zone in limit_zones:
			datas.append({
				"id": limit_zone.id,
				"name": limit_zone.name
			})
		return datas

	@param_required(['corp_id'])
	def get(args):
		corp = args['corp']
		# 查看商品
		product_id = args.get('product_id')
		config = {}

		#支付接口配置
		config['pay_interfaces'] = AProductCreationOption.__load_pay_interfaces(corp)

		#运费模板
		config['postage_config_info'] = AProductCreationOption.__load_postag_config(corp, product_id=product_id)

		#属性模板
		config['property_templates'] = AProductCreationOption.__load_product_property_templates(corp)

		#分类信息
		config['categories'] = AProductCreationOption.__load_categories(corp)

		#限定区域信息
		config['limit_zones'] = AProductCreationOption.__load_limit_zones(corp)

		return config
