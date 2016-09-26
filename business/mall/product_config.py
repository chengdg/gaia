# -*- coding: utf-8 -*-
from eaglet.decorator import param_required

from business import model as business_model
# from business.mall.owner import Owner
from business.product.product import Product
from db.mall import models as mall_models


class ProductConfig(business_model.Model):
	"""
	新商品池业务逻辑对象
	"""
	__slots__ = (
		'owner_id',
		'postage_config_info',
		'property_templates',
		'pay_interface_config',
		'mall_type',
		'is_bill',
		'store_name',
		'product',
		'categories'
	)

	@staticmethod
	@param_required(['owner_id', 'product_id'])
	def get(args):
		pass
		# owner_id = args['owner_id']
		# product_id = args['product_id']

		# product_config = ProductConfig()
		# owner = Owner(owner_id)

		# # 商品数据
		# if product_id:
		# 	product = Product.from_id({"product_id": product_id, 'owner_id': owner_id, 'fill_options': {
		# 		'with_product_model': True,
		# 		'with_image': True,
		# 		'with_property': True,
		# 		'with_model_property_info': True,
		# 		'with_all_category': True,
		# 		'with_group_buy_info': True
		# 	}})
		# 	product_config.product = product.to_dict()
		# else:
		# 	product_config.product = {}

		# # 支付方式
		# pay_interface_config = {
		# 	"online_pay_interfaces": [],
		# 	"is_enable_cod_pay_interface": False
		# }
		# pay_interfaces = mall_models.PayInterface.select().dj_where(owner=owner_id)
		# for pay_interface in pay_interfaces:
		# 	if not pay_interface.is_active:
		# 		continue
		# 	pay_interface.name = mall_models.PAYTYPE2NAME[pay_interface.type]
		# 	if pay_interface.type == mall_models.PAY_INTERFACE_COD:
		# 		pay_interface_config['is_enable_cod_pay_interface'] = True
		# 	elif pay_interface.type == mall_models.PAY_INTERFACE_WEIZOOM_COIN:
		# 		pass
		# 	else:
		# 		_dict = pay_interface.to_dict()
		# 		_dict['name'] = mall_models.PAYTYPE2NAME[_dict['type']]
		# 		pay_interface_config['online_pay_interfaces'].append(
		# 			_dict)

		# product_config.pay_interface_config = pay_interface_config

		# # 运费配置
		# system_postage_config = mall_models.PostageConfig.select().dj_where(
		# 	owner=owner_id, is_used=True).first()
		# postage_config_info = {
		# 	'system_postage_config': system_postage_config.to_dict() if system_postage_config else None,
		# 	'is_use_system_postage_config': False
		# }

		# product_config.postage_config_info = postage_config_info

		# # 属性模板
		# property_templates = ProductPropertyTemplate.from_owner_id({'owner_id': owner_id})
		# product_config.property_templates = map(lambda x: x.to_dict(), property_templates)

		# # if (hasattr(product, 'postage_type') and
		# # 		    product.postage_type == models.POSTAGE_TYPE_CUSTOM):
		# # 	postage_config_info['is_use_system_postage_config'] = True

		# # mall_type
		# product_config.mall_type = owner.mall_type
		# product_config.is_bill = False if owner.mall_type else True
		# product_config.store_name = owner.store_name

		# # 商品分组
		# if product_id:
		# 	product_config.categories = product.categories
		# else:
		# 	product_config.categories = map(lambda x: x.to_dict(),
		# 	                                mall_models.ProductCategory.select().dj_where(owner_id=owner_id))

		# return product_config
