
Feature:订单列表-待支付
"""

"""

Background:
	Given 重置'apiserver'的bdd环境
	Given jobs登录系统

	#添加支付方式
	When jobs添加支付方式
		"""
		[{
			"type": "货到付款",
			"is_active": "启用"
		},{
			"type": "微信支付",
			"is_active": "启用"
		},{
			"type": "支付宝",
			"is_active": "启用"
		}]
		"""

	#添加商品
		#单规格商品-统一运费（0.00）
		When jobs添加商品
			"""
			[{
				"name": "无规格商品1",
				"price": 11.00,
				"weight": 1.0,
				"stock_type": "无限",
				"postage":0.00,
				"pay_interfaces":
					[{
						"type": "在线支付"
					},{
						"type": "货到付款"
					}],
				"invoice":false,
				"distribution_time":false,
				"create_time":"2015-09-01 10:00"
			}]
			"""
		#新关注的会员默认为普通等级的会员
		Given bill关注jobs的公众号::apiserver


@gaia @order @allOrder @ztqb
Scenario:1 待支付订单-单规格商品；单商品；统一运费（0.00）；微信支付
	When bill访问jobs的webapp::apiserver
	When bill购买jobs的商品::apiserver
		"""
		{
			"order_id":"001",
			"date":"2016-01-01",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type": "微信支付",
			"products":[{
				"name":"无规格商品1",
				"price":11.00,
				"count":1
			}],
			"postage": 0.00,
			"customer_message": "bill购买无规格商品1"
		}
		"""

	Given jobs登录系统
	Then jobs获得订单列表
		"""
		[{
			"order_no":"001",
			"methods_of_payment":"微信支付",
			"order_time":"2016-01-01 00:00",
			"save_money": 0.00,
			"buyer":"bill",
			"is_first_order":false,
			"is_group_buying":false,
			"customer_message": "bill购买无规格商品1",
			"business_message":"",
			"ship_name":"bill",
			"ship_tel":"13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"invoice":"",
			"pay_money": 11.00,
			"postage": 0.00,
			"status":"待支付",
			"actions": ["支付","修改价格","取消订单"],
			"delivery_items":[{
				"products":[{
					"name":"无规格商品1",
					"origin_price":11.00,
					"count":1
				}]
			}]
		}]
		"""



