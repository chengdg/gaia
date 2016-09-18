# -*- coding: utf-8 -*-
import json
import logging

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.shop_remind import ShopRemind

class AShopRemind(api_resource.ApiResource):
	'''
	店铺提醒集合.
	'''
	app = 'mall'
	resource = 'shop_remind'

	@param_required(['owner_id'])
	def get(args):
		'''
		店铺提醒
		'''
		shop_remind = ShopRemind.from_owner_id({
				'owner_id': args['owner_id'],
				'with_options': {
					'with_onshelf_product_count': True,
					'with_sellout_product_count': True,
					'with_to_be_shipped_order_count': True,
					'with_refunding_order_count': True,
					'with_flash_sale_count': True,
					'with_premium_sale_count': True,
					'with_integral_sale_count': True,
					'with_coupon_count': True,
					'with_red_envelope_count': True,
				}
			})
		return {
			'shop_remind': shop_remind.to_dict()
		}
