# __author__ : "冯雪静"
Feature: 限时抢购和积分活动订单

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
	When zhouxun更新积分规则为
		"""
		{
			"integral_each_yuan": 2
		}
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
			"name":"多规格商品3",
			"model":{
				"models":{
					"黑色 M":{
						"price": 30.20,
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
		["无规格商品1", "多规格商品3"]
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
			"start_date": "今天",
			"end_date": "1天后",
			"product_name":"多规格商品3",
			"member_grade": "全部会员",
			"count_per_purchase":2,
			"promotion_price": 30.00,
			"limit_period": 1
		}]
		"""
	When zhouxun创建积分应用活动::weapp
		"""
		[{
			"name": "多商品积分应用1",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "无规格商品1,多规格商品3",
			"is_permanant_active": false,
			"rules": [{
				"member_grade": "全部",
				"discount": 49.95,
				"discount_money": 5.00
			}]
		}]
		"""
	Given bill关注zhouxun的公众号::apiserver


@gaiax @order
Scenario: 1 管理员支付含有限时抢购和积分商品的订单（多规格商品）

	When bill访问zhouxun的webapp::apiserver
	When bill获得zhouxun的50会员积分::apiserver
	Then bill在zhouxun的webapp中拥有50会员积分::apiserver
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
					"count":1,
					"integral": 10,
					"integral_money": 5.00
				},{
					"name":"多规格商品3",
					"model":"白色 S",
					"count":1,
					"integral": 10,
					"integral_money": 5.00
				},{
					"name":"无规格商品1",
					"count":1,
					"integral": 10,
					"integral_money": 5.00
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
			"pay_money": 50.00,
			"product_price": 65.00,
			"save_money": 20.51,
			"final_price": 50.00,
			"weizoom_card_money": 0.00,
			"member_card_money": 0.00,
			"integral": 30,
			"integral_money": 15.00,
			"member_info": {
				"is_subscribed":true,
				"name":"bill"
				},
			"ship_name": "bill",
			"ship_tel":"13811223344",
			"ship_area_text":"北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"delivery_items": [{
				"bid":"001-zhouxun",
				"status_code":"paid",
				"ship_name": "bill",
				"created_at":"2016-01-01 00:00:00",
				"payment_time":"2016-01-02 00:00:00",
				"supplier_info": {
					"supplier_type": "supplier",
					"name":"zhouxun"
				},
				"products": [{
					"name":"多规格商品3",
					"product_model_name_texts":["黑色","M"],
					"sale_price":30.00,
					"origin_price":30.20,
					"count":1,
					"promotion_info":{
						"type":"flash_sale",
						"promotion_saved_money":0.20
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
				},{
					"name":"无规格商品1",
					"sale_price":5.00,
					"origin_price":10.11,
					"count":1,
					"promotion_info":{
						"type":"flash_sale",
						"promotion_saved_money":5.11
					}
				}]
			}]
		}]
		"""
	Then zhouxun获得订单'001'
		"""
		{
			"bid": "001",
			"status_code":"paid",
			"created_at":"2016-01-01 00:00:00",
			"payment_time":"2016-01-02 00:00:00",
			"pay_interface_type_code":"weixin_pay",
			"pay_money": 50.00,
			"product_price": 65.00,
			"save_money": 20.51,
			"final_price": 50.00,
			"weizoom_card_money": 0.00,
			"member_card_money": 0.00,
			"integral": 30,
			"integral_money": 15.00,
			"delivery_items": [{
				"bid": "001-zhouxun",
				"status_code":"paid",
				"ship_name": "bill",
				"created_at":"2016-01-01 00:00:00",
				"payment_time":"2016-01-02 00:00:00",
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "zhouxun"
				},
				"products": [{
					"name":"多规格商品3",
					"product_model_name_texts":["黑色","M"],
					"sale_price":30.00,
					"origin_price":30.20,
					"count":1,
					"promotion_info":{
						"type":"flash_sale",
						"promotion_saved_money":0.20
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
				},{
					"name":"无规格商品1",
					"sale_price":5.00,
					"origin_price":10.11,
					"count":1,
					"promotion_info":{
						"type":"flash_sale",
						"promotion_saved_money":5.11
					}
				}]
			}]
		}
		"""
	When bill访问zhouxun的webapp::apiserver 
	Then bill在zhouxun的webapp中拥有20会员积分::apiserver

@gaiax @order
Scenario: 2 管理员退款含有限时抢购和积分商品的订单

	When bill访问zhouxun的webapp::apiserver
	When bill获得zhouxun的50会员积分::apiserver
	Then bill在zhouxun的webapp中拥有50会员积分::apiserver
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
					"count":1,
					"integral": 10,
					"integral_money": 5.00
				},{
					"name":"多规格商品3",
					"model":"白色 S",
					"count":1,
					"integral": 10,
					"integral_money": 5.00
				},{
					"name":"无规格商品1",
					"count":1,
					"integral": 10,
					"integral_money": 5.00
				}]
		}
		"""
	When bill使用支付方式'微信支付'进行支付订单'001'于2016-01-02 10:00:00::apiserver
	Then bill在zhouxun的webapp中拥有20会员积分::apiserver
	Given zhouxun登录系统
	When zhouxun申请退款出货单'001-zhouxun'
		"""
		{
			"cash":10.00,
			"weizoom_card_money":0.00,
			"coupon_money":15.00,
			"integral":80,
			"member_card_money":0.00,
			"time": "2016-01-03 10:00:00"
		}
		"""
	Then zhouxun获得订单列表
		"""
		[{
			"bid": "001",
			"status_code": "refunding",
			"pay_interface_type_code": "weixin_pay",
			"pay_money": 50.00,
			"product_price": 65.00,
			"save_money": 20.51,
			"origin_final_price": 50.00,
			"origin_weizoom_card_money": 0.00,
			"origin_member_card_money": 0.00,
			"final_price": 50.00,
			"weizoom_card_money": 0.00,
			"member_card_money": 0.00,
			"integral": 30,
			"integral_money": 15.00,
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
				"bid": "001-zhouxun",
				"status_code": "refunding",
				"refunding_info": {
					"finished": false,
					"total_can_refund": 65.00,
					"cash": 10.00,
					"weizoom_card_money": 0.00,
					"member_card_money":0.00,
					"coupon_money": 15.00,
					"integral": 80,
					"integral_money": 40.00,
					"total": 65.00
					},
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "zhouxun"
				},
				"products": [{
					"name":"多规格商品3",
					"product_model_name_texts":["黑色","M"],
					"sale_price":30.00,
					"origin_price":30.20,
					"count":1,
					"promotion_info":{
						"type":"flash_sale",
						"promotion_saved_money":0.20
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
				},{
					"name":"无规格商品1",
					"sale_price":5.00,
					"origin_price":10.11,
					"count":1,
					"promotion_info":{
						"type":"flash_sale",
						"promotion_saved_money":5.11
					}
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
			"pay_money": 50.00,
			"product_price": 65.00,
			"save_money": 20.51,
			"origin_final_price": 50.00,
			"origin_weizoom_card_money": 0.00,
			"final_price": 50.00,
			"weizoom_card_money": 0.00,
			"integral": 30,
			"integral_money": 15.00,
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
				"bid": "001-zhouxun",
				"status_code": "refunding",
				"postage": 0.00,
				"refunding_info": {
					"finished": false,
					"cash": 10.00,
					"weizoom_card_money": 0.00,
					"member_card_money":0.00,
					"coupon_money": 15.00,
					"integral": 80,
					"integral_money": 40.00,
					"total": 65.00
					},
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "zhouxun"
				},
				"products": [{
					"name":"多规格商品3",
					"product_model_name_texts":["黑色","M"],
					"sale_price":30.00,
					"origin_price":30.20,
					"count":1,
					"promotion_info":{
						"type":"flash_sale",
						"promotion_saved_money":0.20
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
				},{
					"name":"无规格商品1",
					"sale_price":5.00,
					"origin_price":10.11,
					"count":1,
					"promotion_info":{
						"type":"flash_sale",
						"promotion_saved_money":5.11
					}
				}]
			}]
		}
		"""
	When bill访问zhouxun的webapp::apiserver
	Then bill在zhouxun的webapp中拥有20会员积分::apiserver

@gaiax @order
Scenario: 3 管理员退款成功含有限时抢购和积分商品的订单

	When bill访问zhouxun的webapp::apiserver
	When bill获得zhouxun的50会员积分::apiserver
	Then bill在zhouxun的webapp中拥有50会员积分::apiserver
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
					"count":1,
					"integral": 10,
					"integral_money": 5.00
				},{
					"name":"多规格商品3",
					"model":"白色 S",
					"count":1,
					"integral": 10,
					"integral_money": 5.00
				},{
					"name":"无规格商品1",
					"count":1,
					"integral": 10,
					"integral_money": 5.00
				}]
		}
		"""
	When bill使用支付方式'微信支付'进行支付订单'001'于2016-01-02 10:00:00::apiserver
	Then bill在zhouxun的webapp中拥有20会员积分::apiserver
	Given zhouxun登录系统
	When zhouxun申请退款出货单'001-zhouxun'
		"""
		{
			"cash":10.00,
			"weizoom_card_money":0.00,
			"coupon_money":15.00,
			"integral":80,
			"member_card_money":0.00,
			"time": "2016-01-03 10:00:00"
		}
		"""
	When zhouxun退款成功出货单'001-zhouxun'
		"""
		{
			"time":"2016-01-03 11:00:00"
		}
		"""
	Then zhouxun获得订单列表
		"""
		[{
			"bid": "001",
			"status_code": "refunded",
			"pay_interface_type_code": "weixin_pay",
			"pay_money": 40.00,
			"product_price": 65.00,
			"save_money": 20.51,
			"origin_final_price": 50.00,
			"origin_weizoom_card_money": 0.00,
			"origin_member_card_money": 0.00,
			"final_price": 40.00,
			"weizoom_card_money": 0.00,
			"member_card_money": 0.00,
			"integral": 30,
			"integral_money": 15.00,
			"refunding_info": {
				"cash": 10.00,
				"weizoom_card_money": 0.00,
				"member_card_money": 0.00,
				"coupon_money": 15.00,
				"integral": 80,
				"integral_money": 40.00,
				"total": 65.00
			},
			"delivery_items": [{
				"bid": "001-zhouxun",
				"status_code": "refunded",
				"refunding_info": {
					"finished": true,
					"total_can_refund": 65.00,
					"cash": 10.00,
					"weizoom_card_money": 0.00,
					"member_card_money":0.00,
					"coupon_money": 15.00,
					"integral": 80,
					"integral_money": 40.00,
					"total": 65.00
					},
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "zhouxun"
				},
				"products": [{
					"name":"多规格商品3",
					"product_model_name_texts":["黑色","M"],
					"sale_price":30.00,
					"origin_price":30.20,
					"count":1,
					"promotion_info":{
						"type":"flash_sale",
						"promotion_saved_money":0.20
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
				},{
					"name":"无规格商品1",
					"sale_price":5.00,
					"origin_price":10.11,
					"count":1,
					"promotion_info":{
						"type":"flash_sale",
						"promotion_saved_money":5.11
					}
				}]
			}]
		}]
		"""

	Then zhouxun获得订单'001'
		"""
		{
			"bid": "001",
			"status_code": "refunded",
			"pay_interface_type_code": "weixin_pay",
			"pay_money": 40.00,
			"product_price": 65.00,
			"save_money": 20.51,
			"origin_final_price": 50.00,
			"origin_weizoom_card_money": 0.00,
			"final_price": 40.00,
			"weizoom_card_money": 0.00,
			"integral": 30,
			"integral_money": 15.00,
			"weizoom_card_info": {
				"used_card": []
			},
			"refunding_info": {
				"cash": 10.00,
				"weizoom_card_money": 0.00,
				"member_card_money": 0.00,
				"coupon_money": 15.00,
				"integral": 80,
				"integral_money": 40.00,
				"total": 65.00
			},
			"delivery_items": [{
				"bid": "001-zhouxun",
				"status_code": "refunded",
				"refunding_info": {
					"finished": true,
					"cash": 10.00,
					"weizoom_card_money": 0.00,
					"member_card_money":0.00,
					"coupon_money": 15.00,
					"integral": 80,
					"integral_money": 40.00,
					"total": 65.00
					},
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "zhouxun"
				},
				"products": [{
					"name":"多规格商品3",
					"product_model_name_texts":["黑色","M"],
					"sale_price":30.00,
					"origin_price":30.20,
					"count":1,
					"promotion_info":{
						"type":"flash_sale",
						"promotion_saved_money":0.20
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
				},{
					"name":"无规格商品1",
					"sale_price":5.00,
					"origin_price":10.11,
					"count":1,
					"promotion_info":{
						"type":"flash_sale",
						"promotion_saved_money":5.11
					}
				}]
			}]
		}
		"""
	When bill访问zhouxun的webapp::apiserver
	Then bill在zhouxun的webapp中拥有20会员积分::apiserver