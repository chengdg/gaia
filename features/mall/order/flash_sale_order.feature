#_author_:张三香 2017.02.07

Feature:限时抢购活动订单
	"""
		管理员【支付】含限时抢购商品的订单
		管理员【申请退款】参与限时抢购活动的订单
	"""

Background:
	Given 重置'apiserver'的bdd环境
	Given 重置'weapp'的bdd环境

	Given zhouxun登录系统
	And zhouxun已添加商品规格
		"""
		[{
			"name": "颜色",
			"type": "图片",
			"values":
				[{
					"name": "黑色",
					"image": "/static/test_resource_img/icon_color/black.png"
				},{
					"name": "白色",
					"image": "/static/test_resource_img/icon_color/white.png"
				}]
		},{
			"name": "尺寸",
			"type": "文字",
			"values":
			[{
				"name": "M"
			},{
				"name": "S"
			}]
		}]
		"""
	When zhouxun添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}]
		"""
	When zhouxun添加商品
		"""
		[{
			"name": "无规格商品1",
			"model":{
				"models":{
					"standard":{
						"price": 10.11,
						"purchase_price": 9.00,
						"stock_type": "有限",
						"stocks": 100
					}
				}
			}
		},{
			"name": "无规格商品2",
			"model":{
				"models":{
					"standard":{
						"price": 20.00,
						"purchase_price": 19.00,
						"stock_type": "无限"
					}
				}
			}
		},{
			"name":"多规格商品3",
			"model":{
				"models":{
					"黑色 M":{
						"price": 30.10,
						"purchase_price":30.00,
						"stock_type":"有限",
							"stocks":10
						},
					"白色 S":{
						"price":30.20,
						"purchase_price":30.00,
						"stock_type": "有限",
						"stocks": 20
							}
					}
				}
		}]
		"""
	When zhouxun将商品移动到'在售'货架
		"""
		["无规格商品1", "无规格商品2","多规格商品3"]
		"""
	Given zhouxun登录系统::weapp
	When zhouxun创建限时抢购活动::weapp
		"""
		[{
			"name": "无规格商品1限时抢购",
			"promotion_title":"",
			"start_date": "2015-01-01",
			"end_date": "1天后",
			"product_name":"无规格商品1",
			"member_grade": "全部会员",
			"count_per_purchase": 2,
			"promotion_price": 5.00,
			"limit_period": 1
		}]
		"""
	When zhouxun创建限时抢购活动::weapp
		"""
		[{
			"name": "多规格商品3限时抢购",
			"promotion_title":"",
			"start_date": "2015-01-01",
			"end_date": "1天后",
			"product_name":"多规格商品3",
			"member_grade": "全部会员",
			"count_per_purchase":2,
			"promotion_price": 30.00,
			"limit_period": 1
		}]
		"""

Scenario:1 管理员支付含有限时抢购商品的订单（无规格商品）
	#订单包含1个无规格的限时抢购商品
	Given bill关注zhouxun的公众号::apiserver
	When bill访问zhouxun的webapp::apiserver 
	When bill购买zhouxun的商品::apiserver
		"""
		{
			"order_id":"001",
			"date":"2016-01-01",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type": "微信支付",
			"products":
				[{
					"name":"无规格商品1",
					"count":2
				}]
		}
		"""
	Given zhouxun登录系统
	When zhouxun支付订单'001'
		"""
		{
			"time":"2016-01-02 00:00:00"
		}
		"""
	Then zhouxun获得订单列表
		"""
		[{
			"bid": "001",
			"pay_interface_type_code":"weixin_pay",
			"created_at":"2016-01-01 00:00:00",
			"payment_time":"2016-01-02 00:00:00",
			"status_code":"paid",
			"save_money":10.22,
			"member_info": {
				"is_subscribed":true,
				"name":"bill"
				},
			"ship_name": "bill",
			"ship_tel":"13811223344",
			"ship_area_text":"北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_money":10.00,
			"final_price":10.00,
			"weizoom_card_money":0.00,
			"member_card_money":0.00,
			"delivery_items":
				[{
					"bid":"001-zhouxun",
					"status_code":"paid",
					"ship_name": "bill",
					"created_at":"2016-01-01 00:00:00",
					"payment_time":"2016-01-02 00:00:00",
					"supplier_info":
						{
							"supplier_type": "supplier",
							"name":"zhouxun"
						},
					"products":
						[{
							"name":"无规格商品1",
							"sale_price":5.00,
							"origin_price":10.11,
							"count":2,
							"promotion_info":{
								"type":"flash_sale",
								"promotion_saved_money":10.22
							}
						}]
				}]
		}]
		"""
	Then zhouxun获得订单'001'
		"""
		{
			"bid":"001",
			"status_code":"paid",
			"created_at":"2016-01-01 00:00:00",
			"payment_time":"2016-01-02 00:00:00",
			"pay_interface_type_code":"weixin_pay",
			"delivery_items":
				[{
					"supplier_info":
						{
							"name":"zhouxun",
							"supplier_type":"supplier"
						},
					"products":
						[{
							"name":"无规格商品1",
							"sale_price":5.00,
							"origin_price":10.11,
							"count":2,
							"promotion_info":{
								"type":"flash_sale",
								"promotion_saved_money":10.22
							}
						}],
					"status_code":"paid"
				}],
			"product_price":10.00,
			"save_money":10.22,
			"pay_money":10.00,
			"final_price":10.00,
			"weizoom_card_money":0.00,
			"member_card_money":0.00
		}
		"""

Scenario:2 管理员支付含有限时抢购商品的订单（多规格商品）
	#订单包含2个多规格的限时抢购商品

	Given bill关注zhouxun的公众号::apiserver
	When bill访问zhouxun的webapp::apiserver 
	When bill购买zhouxun的商品::apiserver
		"""
		{
			"order_id":"001",
			"date":"2016-01-01",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type": "微信支付",
			"products":
				[{
					"name":"多规格商品3",
					"model":"黑色 M",
					"count":1
				},{
					"name":"多规格商品3",
					"model":"白色 S",
					"count":1
				}]
		}
		"""
	Given zhouxun登录系统
	When zhouxun支付订单'001'
		"""
		{
			"time":"2016-01-02 00:00:00"
		}
		"""
	Then zhouxun获得订单列表
		"""
		[{
			"bid": "001",
			"pay_interface_type_code":"weixin_pay",
			"created_at":"2016-01-01 00:00:00",
			"payment_time":"2016-01-02 00:00:00",
			"status_code":"paid",
			"save_money":0.30,
			"member_info": {
				"is_subscribed":true,
				"name":"bill"
				},
			"ship_name": "bill",
			"ship_tel":"13811223344",
			"ship_area_text":"北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_money":60.00,
			"final_price":60.00,
			"weizoom_card_money":0.00,
			"member_card_money":0.00,
			"delivery_items":
				[{
					"bid":"001-zhouxun",
					"status_code":"paid",
					"ship_name": "bill",
					"created_at":"2016-01-01 00:00:00",
					"payment_time":"2016-01-02 00:00:00",
					"supplier_info":
						{
							"supplier_type": "supplier",
							"name":"zhouxun"
						},
					"products":
						[{
							"name":"多规格商品3",
							"product_model_name_texts":["黑色","M"],
							"sale_price":30.00,
							"origin_price":30.10,
							"count":1,
							"promotion_info":{
								"type":"flash_sale",
								"promotion_saved_money":0.10
							}
						},{
							"name":"多规格商品3",
							"product_model_name_texts":["白色","S"],
							"sale_price":30.00,
							"origin_price":30.20,
							"count":1,
							"promotion_info":{
								"type":"flash_sale",
								"promotion_saved_money":0.20
							}
						}]
				}]
		}]
		"""
	Then zhouxun获得订单'001'
		"""
		{
			"bid":"001",
			"status_code":"paid",
			"created_at":"2016-01-01 00:00:00",
			"payment_time":"2016-01-02 00:00:00",
			"pay_interface_type_code":"weixin_pay",
			"delivery_items":
				[{
					"supplier_info":
						{
							"name":"zhouxun",
							"supplier_type":"supplier"
						},
					"products":
						[{
							"name":"多规格商品3",
							"product_model_name_texts":["黑色","M"],
							"sale_price":30.00,
							"origin_price":30.10,
							"count":1,
							"promotion_info":{
								"type":"flash_sale",
								"promotion_saved_money":0.10
							}
						},{
							"name":"多规格商品3",
							"product_model_name_texts":["白色","S"],
							"sale_price":30.00,
							"origin_price":30.20,
							"count":1,
							"promotion_info":{
								"type":"flash_sale",
								"promotion_saved_money":0.20
							}
						}],
					"status_code":"paid"
				}],
			"product_price":60.00,
			"save_money":0.30,
			"pay_money":60.00,
			"final_price":60.00,
			"weizoom_card_money":0.00,
			"member_card_money":0.00
		}
		"""

Scenario:3 管理员退款含有限时抢购商品的出货单
	Given bill关注zhouxun的公众号::apiserver
	When bill访问zhouxun的webapp::apiserver 
	When bill购买zhouxun的商品::apiserver
		"""
		{
			"order_id":"001",
			"date":"2016-10-01",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type": "微信支付",
			"products":[{
				"name":"无规格商品1",
				"count":1
			},{
				"name":"无规格商品2",
				"count":2
			}],
			"postage": 0.00
		}
		"""
	When bill使用支付方式'微信支付'进行支付订单'001'于2016-10-01 10:00:00::apiserver

	Given zhouxun登录系统
	When zhouxun申请退款出货单'001-zhouxun'
		"""
		{
			"cash":20.00,
			"weizoom_card_money":0.00,
			"coupon_money":25.00,
			"integral":0,
			"member_card_money":0.00,
			"time": "2016-10-02 10:00:00"
		}
		"""
	Then zhouxun获得订单列表
		"""
		[{
			"bid": "001",
			"status_code": "refunding",
			"pay_interface_type_code": "weixin_pay",
			"pay_money": 45.00,
			"product_price": 45.00,
			"postage":0.00,
			"save_money": 5.11,
			"origin_final_price": 45.00,
			"origin_weizoom_card_money": 0.00,
			"origin_member_card_money": 0.00,
			"final_price": 45.00,
			"weizoom_card_money": 0.00,
			"member_card_money": 0.00,
			"integral": 0,
			"integral_money": 0.00,
			"coupon_money": 0.00,
			"refunding_info": {
				"cash": 0.00,
				"weizoom_card_money": 0.00,
				"member_card_money": 0.00,
				"coupon_money": 0.00,
				"integral": 0,
				"integral_money": 0.00,
				"total": 0.00
			},
			"delivery_items": [{
				"bid": "010-zhouxun",
				"status_code": "refunding",
				"refunding_info": {
					"finished": false,
					"total_can_refund": 45.00,
					"cash": 20.00,
					"weizoom_card_money": 0.00,
					"member_card_money":0.00,
					"coupon_money": 25.00,
					"integral": 0,
					"integral_money": 0.00,
					"total": 45.00
					},
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "zhouxun"
				},
				"products": [{
					"name": "无规格商品1",
					"count": 1
				},{
					"name": "无规格商品2",
					"count": 2
				}]
			}]
		}]
		"""
	Then zhouxun获得订单'001'
		"""
		{
			"bid": "001",
			"status_code": "refunding",
			"pay_interface_type_code": "weixin_pay",
			"coupon_money": 0.00,
			"pay_money": 45.00,
			"product_price": 45,
			"postage":0.00,
			"save_money": 5.11,
			"origin_final_price": 45.00,
			"origin_weizoom_card_money": 0.00,
			"final_price": 45.00,
			"weizoom_card_money": 0.00,
			"integral": 0,
			"integral_money": 0.00,
			"weizoom_card_info": {
				"used_card": []
			},
			"refunding_info": {
				"cash": 0.00,
				"weizoom_card_money": 0.00,
				"member_card_money": 0.00,
				"coupon_money": 0.00,
				"integral": 0,
				"integral_money": 0.00,
				"total": 0.00
			},
			"delivery_items": [{
				"bid": "010-zhouxun",
				"status_code": "refunding",
				"postage": 0.00,
				"refunding_info": {
					"finished": false,
					"cash": 20.00,
					"weizoom_card_money": 0.00,
					"member_card_money":0.00,
					"coupon_money": 25.00,
					"integral": 0,
					"integral_money": 0.00,
					"total": 45.00
					},
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "zhouxun"
				},
				"products": [{
					"name": "无规格商品1",
					"count": 1
				},{
					"name": "无规格商品2",
					"count": 2
				}]
			}]
		}
		"""
