# __author__ : "冯雪静"

Feature: 限时抢购和普通优惠券订单

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
	Given bill关注zhouxun的公众号::apiserver

@order
Scenario: 1 使用全店优惠券的限时抢购商品订单（优惠券全额抵扣）

	Given zhouxun登录系统::weapp
	When zhouxun添加优惠券规则::weapp
		"""
		[{
			"name": "通用券1",
			"money": 100.00,
			"limit_counts": 1,
			"using_limit": "",
			"count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"description":"使用说明",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""
	When zhouxun为会员发放优惠券::weapp
		"""
		{
			"name": "通用券1",
			"count": 1,
			"members": ["bill"]
		}
		"""
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
				},{
					"name":"无规格商品1",
					"count":1
				}],
			"coupon": "coupon1_id_1"
		}
		"""
	Given zhouxun登录系统
	Then zhouxun获得订单列表
		"""
		[{
			"bid": "001",
			"status_code": "paid",
			"pay_interface_type_code": "preference",
			"pay_money": 0.00,
			"product_price": 65.00,
			"save_money": 70.51,
			"final_price": 0.00,
			"coupon_money": 65.00,
			"extra_coupon_info":{
				"bid":"coupon1_id_1",
				"type":"all_products_coupon"
			},
			"delivery_items": [{
				"bid": "001-zhouxun",
				"status_code": "paid",
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
			"status_code": "paid",
			"pay_interface_type_code": "preference",
			"coupon_money": 65.00,
			"extra_coupon_info":{
				"bid":"coupon1_id_1",
				"type":"all_products_coupon"
			},
			"pay_money": 0.00,
			"product_price": 65.00,
			"save_money": 70.51,
			"final_price": 0.00,
			"delivery_items": [{
				"bid": "001-zhouxun",
				"status_code": "paid",
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

@order
Scenario: 2 使用全店优惠券的限时抢购商品订单（优惠券部分抵扣）

	Given zhouxun登录系统::weapp
	When zhouxun添加优惠券规则::weapp
		"""
		[{
			"name": "通用券2",
			"money": 20.00,
			"limit_counts": 1,
			"using_limit": "",
			"count": 5,
			"start_date": "今天",
			"end_date": "1天后",
			"description":"使用说明",
			"coupon_id_prefix": "coupon2_id_"
		}]
		"""
	When zhouxun为会员发放优惠券::weapp
		"""
		{
			"name": "通用券2",
			"count": 1,
			"members": ["bill"]
		}
		"""
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
				},{
					"name":"无规格商品1",
					"count":1
				}],
			"coupon": "coupon2_id_1"
		}
		"""
	Given zhouxun登录系统
	Then zhouxun获得订单列表
		"""
		[{
			"bid": "001",
			"status_code": "created",
			"pay_interface_type_code": "weixin_pay",
			"pay_money": 45.00,
			"product_price": 65.00,
			"save_money": 25.51,
			"final_price": 45.00,
			"coupon_money": 20.00,
			"extra_coupon_info":{
				"bid":"coupon1_id_1",
				"type":"all_products_coupon"
			},
			"delivery_items": [{
				"bid": "001-zhouxun",
				"status_code": "created",
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
			"status_code": "created",
			"pay_interface_type_code": "weixin_pay",
			"coupon_money": 20.00,
			"extra_coupon_info":{
				"bid":"coupon1_id_1",
				"type":"all_products_coupon"
			},
			"pay_money": 45.00,
			"product_price": 65.00,
			"save_money": 25.51,
			"final_price": 45.00,
			"delivery_items": [{
				"bid": "001-zhouxun",
				"status_code": "created",
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