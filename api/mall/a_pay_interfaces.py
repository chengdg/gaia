# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.pay_interface import PayInterface
from business.mall.weixin_pay_interface import WeixinPayInterface
from business.mall.ali_pay_interface import AliPayInterface


class APayInterfaces(api_resource.ApiResource):
	"""
	支付方式列表
	"""
	app = 'mall'
	resource = 'pay_interfaces'

	@param_required(['corp'])
	def get(args):
		corp = args['corp']
		pay_interfaces = corp.pay_interface_repository.get_pay_interfaces()

		datas = []
		for pay_interface in pay_interfaces:
			data = {
				"id": pay_interface.id,
				"type": pay_interface.str_type,
				"name": pay_interface.name,
				"is_active": pay_interface.is_active,
				"config": None
			}

			if pay_interface.is_weixin_pay():
				weixin_pay_interface = WeixinPayInterface(pay_interface)
				config = weixin_pay_interface.config
				if weixin_pay_interface.is_v2_weixin_pay():
					data['config'] = {
						"version": 'v2',
						"id": config.id,
						"app_id": config.app_id,
						"partner_id": config.partner_id,
						"partner_key": config.partner_key,
						"paysign_key": config.paysign_key
					}
				elif weixin_pay_interface.is_v3_weixin_pay():
					data['config'] = {
						"version": 'v3',
						"id": config.id,
						"app_id": config.app_id,
						"mch_id": config.mch_id,
						"api_key": config.api_key,
						"paysign_key": config.paysign_key
					}
				else:
					pass
			elif pay_interface.is_ali_pay():
				ali_pay_interface = AliPayInterface(pay_interface)
				config = ali_pay_interface.config
				data['config'] = {
					'version': 'v5',
					'id': config.id,
					'partner': config.partner,
					'key': config.key,
					'ali_public_key': config.ali_public_key,
					'private_key': config.private_key,
					'seller_email': config.seller_email
				}
			else:
				pass
			datas.append(data)

		return {
			"pay_interfaces": datas
		}
