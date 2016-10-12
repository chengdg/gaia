
Feature:订单列表-待支付
"""

"""

Background:
	Given 重置'apiserver'的bdd环境
	Given 重置'weizoom_card'的bdd环境
	Given jobs登录系统
	When jobs开通使用微众卡权限

	#添加支付方式
		When jobs添加支付方式
			"""
			{
				"version":3,
				"type": "微信支付",
				"is_active": "启用",
				"weixin_appid": "wxf32a294a6995d5b9",
				"mch_id": "1316811801",
				"api_key": "w1201e1202i1203z1204o1205o1206mw"
			}
			"""
		When jobs添加支付方式
			"""
			{
				"type": "支付宝",
				"is_active": "启用",
				"partner": "11",
				"key": "21",
				"ali_public_key": "31",
				"private_key": "41",
				"seller_email": "a@a.com"
			}
			"""
		When jobs添加支付方式
			"""
			{
				"type": "货到付款",
				"is_active": "启用"
			}
			"""
		When jobs添加支付方式
			"""
			{
				"type": "微众卡支付",
				"is_active": "启用"
			}
			"""

	#创建微众卡
		Given test登录管理系统::weizoom_card
		When test新建通用卡::weizoom_card
			"""
			[{
				"name":"10元微众卡",
				"prefix_value":"010",
				"type":"virtual",
				"money":"10.00",
				"num":"5",
				"comments":"微众卡"
			}]
			"""
		#微众卡审批出库
		When test下订单::weizoom_card
			"""
			[{
				"card_info":[{
					"name":"10元微众卡",
					"order_num":"1",
					"start_date":"2015-04-07 00:00",
					"end_date":"2220-10-07 00:00"
				}],
				"order_info":{
					"order_id":"0001"
					}		
			}]
			"""
		And test批量激活订单'0001'的卡::weizoom_card

	#添加商品规格
		When jobs添加商品规格
			"""
			{
				"name": "颜色",
				"type": "图片",
				"values": [{
					"name": "黑色",
					"image": "/standard_static/test_resource_img/hangzhou1.jpg"
				},{
					"name": "白色",
					"image": "/standard_static/test_resource_img/hangzhou2.jpg"
				}]
			}
			"""
		When jobs添加商品规格
			"""
			{
				"name": "尺寸",
				"type": "文本",
				"values": [{
					"name": "M"
				},{
					"name": "S"
				}]
			}
			"""
		
	#添加商品
		#单规格商品-统一运费（0.00）
		When jobs添加商品
			"""
			{
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
			}
			"""

		#单规格商品-发票;统一运费
		When jobs添加商品
			"""
			{
				"name": "无规格商品2-发票",
				"price": 22.11,
				"weight": 1.0,
				"stock_type": "无限",
				"postage":2.00,
				"pay_interfaces":
					[{
						"type": "在线支付"
					},{
						"type": "货到付款"
					}],
				"invoice":true,
				"distribution_time":false,
				"create_time":"2015-09-02 10:00"
			}
			"""

		#单规格会员价商品
		When jobs添加商品
			"""
			{
				"name": "会员价无规格商品4",
				"price": 40.00,
				"weight": 1.0,
				"stock_type": "无限",
				"postage":5.00,
				"pay_interfaces":
					[{
						"type": "在线支付"
					},{
						"type": "货到付款"
					}],
				"invoice":false,
				"distribution_time":false,
				"create_time":"2015-09-04 10:00"
			}
			"""

	#会员
		#新关注的会员默认为普通等级的会员
		Given bill关注jobs的公众号


@order @allOrder
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

@order @allOrder
Scenario:2 待支付订单-单规格商品；单商品；发票;统一运费；支付宝
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
			"pay_type": "支付宝",
			"invoice":{
				"type":"个人",
				"value":"李李"
			},
			"products":[{
				"name":"无规格商品2-发票",
				"price":22.11,
				"count":1
			}],
			"postage": 2.00,
			"customer_message": "bill购买无规格商品2—发票"
		}
		"""

	Given jobs登录系统
	Then jobs获得订单列表
		"""
		[{
			"order_no":"001",
			"methods_of_payment":"支付宝",
			"order_time":"2016-01-01 00:00",
			"save_money": 0.00,
			"buyer":"bill",
			"is_first_order":false,
			"is_group_buying":false,
			"customer_message": "bill购买无规格商品2—发票",
			"business_message":"",
			"ship_name":"bill",
			"ship_tel":"13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"invoice":"个人,李李",
			"pay_money": 24.11,
			"postage": 2.00,
			"status":"待支付",
			"actions": ["支付","修改价格","取消订单"],
			"delivery_items":[{
				"products":[{
					"name":"无规格商品2-发票",
					"origin_price":22.11,
					"count":1
				}]
			}]
		}]
		"""

@order @allOrder
Scenario:3 待支付订单-多规格商品；单商品；配送时间；系统运费‘顺丰’；支付宝
	#添加运费配置
		Given jobs登录系统
		When jobs添加邮费配置
			"""
			{
				"name":"顺丰",
				"first_weight":1,
				"first_weight_price":15.00,
				"added_weight":1,
				"added_weight_price":5.00
			}
			"""
		When jobs添加邮费配置
			"""
			{
				"name" : "圆通",
				"first_weight":1,
				"first_weight_price":10.00
			}
			"""
		When jobs选择'顺丰'运费配置
	#添加商品
		#多规格商品-配送时间；系统运费‘顺丰’
		When jobs添加商品
			"""
			{
				"name": "多规格商品3-配送时间",
				"model": {
					"models": {
						"黑色 S": {
							"price": 30.00,
							"weight": 1.0,
							"stock_type": "有限",
							"stocks": 10
						},
						"白色 M": {
							"price": 31.00,
							"weight": 1.0,
							"stock_type": "无限"
						}
					}
				},
				"postage":"顺丰",
				"pay_interfaces":
					[{
						"type": "在线支付"
					},{
						"type": "货到付款"
					}],
				"invoice":false,
				"distribution_time":true,
				"create_time":"2015-09-03 10:00"
			}
			"""

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
			"pay_type": "支付宝",
			"distribution_time":"2016-01-05 10:00-12:30",
			"products":[{
				"name":"多规格商品3-配送时间",
				"price":30.00,
				"count": 1,
				"model": "黑色 S"
			}],
			"postage": 15.00,
			"customer_message": "bill购买多规格商品3-配送时间"
		}
		"""

	Given jobs登录系统
	Then jobs获得订单列表
		"""
		[{
			"order_no":"001",
			"methods_of_payment":"支付宝",
			"order_time":"2016-01-01 00:00",
			"save_money": 0.00,
			"buyer":"bill",
			"is_first_order":false,
			"is_group_buying":false,
			"customer_message": "bill购买多规格商品3-配送时间",
			"business_message":"",
			"distribution_time":"2016-01-05 10:00-12:30",
			"ship_name":"bill",
			"ship_tel":"13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_money": 45.00,
			"postage": 15.00,
			"status":"待支付",
			"actions": ["支付","修改价格","取消订单"],
			"delivery_items":[{
				"products":[{
					"name":"多规格商品3-配送时间",
					"origin_price":30.00,
					"model": "黑色 S",
					"count":1
				}]
			}]
		}]
		"""

@order @allOrder
Scenario:4 待支付订单-多规格，单规格；多商品；系统运费，微信支付
	#添加运费配置
		Given jobs登录系统
		When jobs添加邮费配置
			"""
			{
				"name":"顺丰",
				"first_weight":1,
				"first_weight_price":15.00,
				"added_weight":1,
				"added_weight_price":5.00
			}
			"""
		When jobs添加邮费配置
			"""
			{
				"name" : "圆通",
				"first_weight":1,
				"first_weight_price":10.00
			}
			"""
		When jobs选择'顺丰'运费配置
	#添加商品
		#多规格商品-配送时间；系统运费‘顺丰’
		When jobs添加商品
			"""
			{
				"name": "多规格商品3-配送时间",
				"model": {
					"models": {
						"黑色 S": {
							"price": 30.00,
							"weight": 1.0,
							"stock_type": "有限",
							"stocks": 10
						},
						"白色 M": {
							"price": 31.00,
							"weight": 1.0,
							"stock_type": "无限"
						}
					}
				},
				"postage":"顺丰",
				"pay_interfaces":
					[{
						"type": "在线支付"
					},{
						"type": "货到付款"
					}],
				"invoice":false,
				"distribution_time":true,
				"create_time":"2015-09-03 10:00"
			}
			"""

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
			"pay_type": "支付宝",
			"invoice":{
				"type":"公司",
				"value":"北京网通"
			},
			"distribution_time":"2016-01-05 10:00-12:30",
			"products":[{
				"name":"无规格商品1",
				"price":11.00,
				"count": 1
			},{
				"name":"无规格商品2-发票",
				"price":22.11,
				"count": 1
			},{
				"name":"多规格商品3-配送时间",
				"price":31.00,
				"count": 1,
				"model": "白色 M"
			}],
			"postage": 17.00,
			"customer_message": "bill购买多商品"
		}
		"""

	Given jobs登录系统
	Then jobs获得订单列表
		"""
		[{
			"order_no":"001",
			"methods_of_payment":"支付宝",
			"order_time":"2016-01-01 00:00",
			"save_money": 0.00,
			"buyer":"bill",
			"is_first_order":false,
			"is_group_buying":false,
			"customer_message": "bill购买多规格商品3-配送时间",
			"business_message":"",
			"distribution_time":"2016-01-05 10:00-12:30",
			"ship_name":"bill",
			"ship_tel":"13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_money": 103.22,
			"postage": 17.00,
			"status":"待支付",
			"actions": ["支付","修改价格","取消订单"],
			"delivery_items":[{
				"products":[{
					"name":"无规格商品1",
					"price":11.00,
					"count": 1
				},{
					"name":"无规格商品2-发票",
					"price":22.11,
					"count": 1
				},{
					"name":"多规格商品3-配送时间",
					"price":31.00,
					"count": 1,
					"model": "白色 M"
				}]
			}]
		}]
		"""

@order @allOrder
Scenario:5 待支付订单-单规格商品；单商品；会员价；统一运费；微信支付
	#系统默认存在普通会员等级
		Given jobs登录系统
		When jobs添加会员等级
				"""
				[{
					"name": "金牌会员",
					"upgrade": "手动升级",
					"discount": "7"
				}]
				"""
		When jobs更新会员等级'普通会员'
				"""
				{
					"name": "普通会员",
					"upgrade": "手动升级",
					"discount": "9"
				}
				"""

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
				"name":"会员价无规格商品4",
				"price":36.00,
				"count":1
			}],
			"postage": 5.00,
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
			"save_money": 4.00,
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
			"pay_money": 36.00,
			"postage": 5.00,
			"status":"待支付",
			"actions": ["支付","修改价格","取消订单"],
			"delivery_items":[{
				"products":[{
					"name":"会员价无规格商品4",
					"origin_price":40.00,
					"count":1
				}]
			}]
		}]
		"""

@order @allOrder
Scenario:6 待支付订单-单规格商品；单商品；统一运费（0.00）；微众卡部分支付
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
			"weizoom_card_info":{
				"id":"010000001",
				"password":"1234567"
			},
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
			"methods_of_payment":"优惠抵扣",
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


