#_author_:张三香 2017.01.20

Feature:管理员支付订单
	"""
		管理员【支付】订单:
			订单列表的状态由待支付变为待发货
			订单详情的状态由待支付变为待发货
			订单中对应商品的销量增加
	"""

Background:
	Given jobs登录系统
	When jobs添加商品
		"""
		[{
			"name": "黄桥烧饼",
			"model":{
				"models":{
					"standard":{
						"price": 1.00,
						"purchase_price":0.99,
						"stock_type": "有限",
						"stocks":10
					}
				}
			},
			"postage_type":"统一运费",
			"unified_postage_money":1.00
		}]
		"""
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
			"type":"微信支付",
			"is_active":"启用",
			"version":3,
			"weixin_appid":"app_id_1",
			"mch_id":"mch_id_1",
			"api_key":"api_key_1",
			"paysign_key":"paysign_key_1"
		}]
		"""
	When zhouxun添加商品
		"""
		[{
			"name":"无规格商品1",
			"swipe_images":
				[{
					"url": "/static/test_resource_img/hangzhou1.jpg"
				},{
					"url": "/static/test_resource_img/hangzhou2.jpg"
				}],
			"model":{
				"models":{
					"standard":{
						"price": 10.10,
						"purchase_price": 10.00,
						"stock_type": "无限"
						}
					}
				},
			"postage_type":"统一运费",
			"unified_postage_money":1.00
		},{
			"name":"多规格商品2",
			"swipe_images":
				[{
					"url": "/static/test_resource_img/hangzhou2.jpg"
				}],
			"model":{
				"models":{
					"黑色 M":{
						"price": 20.10,
						"purchase_price":20.00,
						"stock_type":"有限",
							"stocks":10
						},
					"白色 S":{
						"price":20.20,
						"purchase_price":20.00,
						"stock_type": "有限",
						"stocks": 20
							}
					}
				}
		}]
		"""
	When zhouxun添加代销商品
		"""
		["黄桥烧饼"]
		"""
	When zhouxun将商品移动到'在售'货架
		"""
		["无规格商品1","多规格商品2","黄桥烧饼"]
		"""
@order @order_order
Scenario:1 支付包含单个供货商单个商品（无规格）的订单
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
					"count":1
				}],
			"postage":1.00,
			"customer_message": "bill购买无规格商品1"
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
			"is_group_buy":false,
			"created_at":"2016-01-01 00:00:00",
			"payment_time":"2016-01-02 00:00:00",
			"status_code":"paid",
			"save_money":0.00,
			"member_info": {
				"is_subscribed":true,
				"name":"bill"
				},
			"is_first_order":true,
			"ship_name": "bill",
			"ship_tel":"13811223344",
			"ship_area_text":"北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_money":11.10,
			"is_weizoom_order":true,
			"final_price":11.10,
			"weizoom_card_money":0.00,
			"member_card_money":0.00,
			"remark":"",
			"postage":1.00,
			"delivery_items":
				[{
					"bid":"001-zhouxun",
					"status_code":"paid",
					"ship_name": "bill",
					"created_at":"2016-01-01 00:00:00",
					"payment_time":"2016-01-02 00:00:00",
					"customer_message":"bill购买无规格商品1",
					"postage":1.00,
					"supplier_info":
						{
							"supplier_type": "supplier",
							"name":"zhouxun"
						},
					"products":
						[{
							"name":"无规格商品1",
							"sale_price":10.10,
							"origin_price":10.10,
							"count":1
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
			"status_logs":
				[{
					"from_status_code":"",
					"to_status_code":"created",
					"time":"2016-01-01 00:00:00"
				},{
					"from_status_code":"created",
					"to_status_code":"paid",
					"time":"2016-01-02 00:00:00"
				}],
			"ship_name": "bill",
			"ship_tel":"13811223344",
			"ship_area_text":"北京市 北京市 海淀区",
			"ship_address":"泰兴大厦",
			"remark":"",
			"operation_logs":
				[{
					"action_text":"下单",
					"operator":"客户",
					"time":"2016-01-01 00:00:00"
				},{
					"action_text":"支付",
					"operator":"zhouxun",
					"time":"2016-01-02 00:00:00"
				}],
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
							"sale_price":10.10,
							"origin_price":10.10,
							"count":1
						}],
					"postage":1.00,
					"status_code":"paid",
					"operation_logs":
						[{
							"action_text":"下单",
							"operator":"客户",
							"time":"2016-01-01 00:00:00"
						},{
							"action_text":"支付",
							"operator":"zhouxun",
							"time":"2016-01-02 00:00:00"
						}]
				}],
			"product_price":10.10,
			"postage":1.00,
			"save_money":0.00,
			"pay_money":11.10,
			"final_price":11.10,
			"weizoom_card_money":0.00,
			"member_card_money":0.00
		}
		"""
	Then zhouxun能获得'在售'商品列表
		"""
		[{
			"name": "多规格商品2",
			"sales":0
		},{
			"name": "无规格商品1",
			"sales":1
		},{
			"name": "黄桥烧饼",
			"sales":0
		}]
		"""

@order @order_order
Scenario:2 支付包含多个供货商多个商品（无规格+多规格）的订单
	#jobs-黄桥烧饼（1.00 *2,运费1.00）
	#zhouxun-无规格商品1（10.10 *1,运费1.00）
	#zhouxun-多规格商品2（黑色 M 20.10 *1 +白色 S 20.20 *1,运费 0.00）

	Given bill关注zhouxun的公众号::apiserver
	When bill访问zhouxun的webapp::apiserver 
	When bill购买zhouxun的商品::apiserver
		"""
		{
			"order_id":"002",
			"date":"2016-01-01",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type": "微信支付",
			"products":
				[{
					"name":"黄桥烧饼",
					"count":2
				},{
					"name":"无规格商品1",
					"count":1
				},{
					"name":"多规格商品2",
					"model":"黑色 M",
					"count":1
				},{
					"name":"多规格商品2",
					"model":"白色 S",
					"count":1
				}],
			"postage":2.00
		}
		"""
	Given zhouxun登录系统
	When zhouxun支付订单'002'
		"""
		{
			"time":"2016-01-02 00:00:00"
		}
		"""
	Then zhouxun获得订单列表
		"""
		[{
			"bid": "002",
			"created_at":"2016-01-01 00:00:00",
			"payment_time":"2016-01-02 00:00:00",
			"status_code":"paid",
			"pay_money":54.40,
			"final_price":54.40,
			"weizoom_card_money":0.00,
			"member_card_money":0.00,
			"remark":"",
			"postage":2.00,
			"delivery_items":
				[{
					"bid":"002-jobs",
					"status_code": "paid",
					"created_at":"2016-01-01 00:00:00",
					"payment_time":"2016-01-02 00:00:00",
					"postage":1.00,
					"supplier_info":
						{
							"supplier_type": "supplier",
							"name":"jobs"
						},
					"products":
						[{
							"name":"黄桥烧饼",
							"count":2
						}]
				},{
					"bid":"002-zhouxun",
					"status_code": "paid",
					"created_at":"2016-01-01 00:00:00",
					"payment_time":"2016-01-02 00:00:00",
					"postage":1.00,
					"supplier_info":
						{
							"supplier_type":"supplier",
							"name":"zhouxun"
						},
					"products":
						[{
							"name":"无规格商品1",
							"count":1
						},{
							"name":"多规格商品2",
							"product_model_name_texts":["黑色","M"],
							"count":1
						},{
							"name":"多规格商品2",
							"product_model_name_texts":["白色","S"],
							"count":1
						}]
				}]
		}]
		"""
	Then zhouxun获得订单'002'
		"""
		{
			"bid":"002",
			"status_code":"paid",
			"created_at":"2016-01-01 00:00:00",
			"payment_time":"2016-01-02 00:00:00",
			"status_logs":
				[{
					"from_status_code":"",
					"to_status_code":"created",
					"time":"2016-01-01 00:00:00"
				},{
					"from_status_code":"created",
					"to_status_code":"paid",
					"time":"2016-01-02 00:00:00"
				}],
			"operation_logs":
				[{
					"action_text":"下单",
					"operator":"客户",
					"time":"2016-01-01 00:00:00"
				},{
					"action_text":"支付",
					"operator":"zhouxun",
					"time":"2016-01-02 00:00:00"
				}],
			"delivery_items":
				[{
					"supplier_info":
						{
							"name":"jobs",
							"supplier_type":"supplier"
						},
					"products":
						[{
							"name":"黄桥烧饼",
							"count":2
						}],
					"postage":1.00,
					"status_code":"paid",
					"operation_logs":
						[{
							"action_text":"下单",
							"operator":"客户",
							"time":"2016-01-01 00:00:00"
						},{
							"action_text":"支付",
							"operator":"zhouxun",
							"time":"2016-01-02 00:00:00"
						}]
				},{
					"supplier_info":
						{
							"name":"zhouxun",
							"supplier_type":"supplier"
						},
					"products":
						[{
							"name":"无规格商品1",
							"count":1
						},{
							"name":"多规格商品2",
							"product_model_name_texts":["黑色","M"],
							"count":1
						},{
							"name":"多规格商品2",
							"product_model_name_texts":["白色","S"],
							"count":1
						}],
					"postage":1.00,
					"status_code":"paid",
					"operation_logs":
						[{
							"action_text":"下单",
							"operator":"客户",
							"time":"2016-01-01 00:00:00"
						},{
							"action_text":"支付",
							"operator":"zhouxun",
							"time":"2016-01-02 00:00:00"
						}]
				}],
			"product_price":52.40,
			"postage":2.00,
			"save_money":0.00,
			"pay_money":54.40,
			"final_price":54.40,
			"weizoom_card_money":0.00,
			"member_card_money":0.00
		}
		"""
	Then zhouxun能获得'在售'商品列表
		"""
		[{
			"name":"多规格商品2",
			"sales":2
		},{
			"name":"无规格商品1",
			"sales":1
		},{
			"name":"黄桥烧饼",
			"sales":2
		}]
		"""