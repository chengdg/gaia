Feature:优惠券活动订单

Background:
	Given 重置'apiserver'的bdd环境
	Given 重置'weapp'的bdd环境

	Given yangmi登录系统
	When yangmi添加商品
		"""
		[{
			"name": "无规格商品1-yangmi",
			"model": {
				"models":{
					"standard":{
						"price": 10.00,
						"purchase_price": 9.00,
						"stock_type": "有限",
						"stocks": 100
					}
				}
			}
		}]
		"""

	Given zhouxun登录系统
	When zhouxun添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}]
		"""
	Given zhouxun已添加商品规格
		"""
		[{
			"name": "颜色",
			"type": "图片",
			"values": [{
				"name": "黑色",
				"image": "/static/test_resource_img/icon_color/black.png"
			},{
				"name": "白色",
				"image": "/static/test_resource_img/icon_color/white.png"
			}]
		},{
			"name": "尺寸",
			"type": "文字",
			"values": [{
				"name": "M"
			},{
				"name": "S"
			}]
		}]
		"""

	When zhouxun添加商品
		"""
		[{
			"name": "无规格商品1-zhouxun",
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
			"name": "多规格商品2-zhouxun",
			"model":{
				"models": {
					"黑色 M": {
						"price": 20.22,
						"purchase_price": 19.22,
						"stock_type": "有限",
						"stocks": 100
					},
					"白色 S": {
						"price": 21.22,
						"purchase_price": 20.22,
						"stock_type": "有限",
						"stocks": 100
					}
				}
			}
		}]
		"""
	When zhouxun添加代销商品
		"""
		["无规格商品1-yangmi"]
		"""
	When zhouxun将商品移动到'在售'货架
		"""
		["无规格商品1-zhouxun","多规格商品2-zhouxun","无规格商品1-yangmi"]
		"""

	Given bill关注zhouxun的公众号::apiserver

@gaiax @order
Scenario:1 使用全店优惠券的单商品订单（优惠券全额抵扣）
	#创建通用券
	Given zhouxun登录系统::weapp
	When zhouxun添加优惠券规则::weapp
		"""
		[{
			"name": "通用券1",
			"money": 100.00,
			"limit_counts": 1,
			"using_limit": "",
			"count": 5,
			"start_date": "2015-01-01",
			"end_date": "1天后",
			"description":"使用说明",
			"coupon_id_prefix": "coupon1_id_"
		}]
		"""

	#发放优惠券
	When zhouxun创建优惠券发放规则发放优惠券::weapp
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
			"coupon": "coupon1_id_1",
			"products":[{
				"name":"无规格商品1-zhouxun",
				"count":1
			}],
			"postage": 0.00
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
			"product_price": 10.11,
			"postage":0.00,
			"save_money": 10.11,
			"origin_final_price": 0.00,
			"final_price": 0.00,
			"coupon_money": 10.11,
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
					"name": "无规格商品1-zhouxun",
					"count": 1
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
			"coupon_money": 10.11,
			"extra_coupon_info":{
				"bid":"coupon1_id_1",
				"type":"all_products_coupon"
			},
			"pay_money": 0.00,
			"product_price": 10.11,
			"postage":0.00,
			"save_money": 10.11,
			"origin_final_price": 0.00,
			"final_price": 0.00,
			"delivery_items": [{
				"bid": "001-zhouxun",
				"status_code": "paid",
				"postage": 0.00,
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "zhouxun"
				},
				"products": [{
					"name": "无规格商品1-zhouxun",
					"count": 1
				}]
			}]
		}
		"""
	
@gaiax @order
Scenario:2 使用全店优惠券的多供货商多规格商品订单（优惠券部分抵扣）
	#创建通用券
	Given zhouxun登录系统::weapp
	When zhouxun添加优惠券规则::weapp
		"""
		[{
			"name": "通用券2",
			"money": 20.00,
			"limit_counts": 1,
			"using_limit": "",
			"count": 5,
			"start_date": "2015-01-01",
			"end_date": "1天后",
			"description":"使用说明",
			"coupon_id_prefix": "coupon2_id_"
		}]
		"""

	#发放优惠券
	When zhouxun创建优惠券发放规则发放优惠券::weapp
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
			"order_id":"002",
			"date":"2016-02-01",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type": "微信支付",
			"coupon": "coupon2_id_1",
			"products":[{
				"name": "无规格商品1-yangmi",
				"count": 1
			},{
				"name": "无规格商品1-zhouxun",
				"count": 1
			},{
				"name":"多规格商品2-zhouxun",
				"model": "黑色 M",
				"count": 1
			},{
				"name":"多规格商品2-zhouxun",
				"model": "白色 S",
				"count": 1
			}],
			"postage": 0.00
		}
		"""

	Given zhouxun登录系统
	Then zhouxun获得订单列表
		"""
		[{
			"bid": "002",
			"status_code": "created",
			"pay_interface_type_code": "weixin_pay",
			"pay_money": 41.55,
			"product_price": 61.55,
			"postage":0.00,
			"save_money": 20.00,
			"origin_final_price": 41.55,
			"final_price": 41.55,
			"coupon_money": 20.00,
			"extra_coupon_info":{
				"bid":"coupon2_id_1",
				"type":"all_products_coupon"
			},
			"delivery_items": [{
				"bid": "002-yangmi",
				"status_code": "created",
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "yangmi"
				},
				"products": [{
					"name": "无规格商品1-yangmi",
					"count": 1
				}]
			},{
				"bid": "002-zhouxun",
				"status_code": "created",
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "zhouxun"
				},
				"products": [{
					"name": "无规格商品1-zhouxun",
					"count": 1
				},{
					"name":"多规格商品2-zhouxun",
					"product_model_name_texts": ["黑色","M"],
					"count": 1
				},{
					"name":"多规格商品2-zhouxun",
					"product_model_name_texts": ["白色", "S"],
					"count": 1
				}]
			}]
		}]
		"""

	Then zhouxun获得订单'002'
		"""
		{
			"bid": "002",
			"status_code": "created",
			"pay_interface_type_code": "weixin_pay",
			"coupon_money": 20.00,
			"extra_coupon_info":{
				"bid":"coupon2_id_1",
				"type":"all_products_coupon"
			},
			"pay_money": 41.55,
			"product_price": 61.55,
			"postage":0.00,
			"save_money": 20.00,
			"origin_final_price": 41.55,
			"final_price": 41.55,
			"delivery_items": [{
				"bid": "002-yangmi",
				"status_code": "created",
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "yangmi"
				},
				"products": [{
					"name": "无规格商品1-yangmi",
					"count": 1
				}]
			},{
				"bid": "002-zhouxun",
				"status_code": "created",
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "zhouxun"
				},
				"products": [{
					"name": "无规格商品1-zhouxun",
					"count": 1
				},{
					"name":"多规格商品2-zhouxun",
					"product_model_name_texts": ["黑色","M"],
					"count": 1
				},{
					"name":"多规格商品2-zhouxun",
					"product_model_name_texts": ["白色", "S"],
					"count": 1
				}]
			}]
		}
		"""

@gaiax @order
Scenario:3 使用多品券的多规格商品订单
	#创建多商品券
	Given zhouxun登录系统::weapp
	When zhouxun添加优惠券规则::weapp
		"""
		[{
			"name": "多商品券1",
			"money": 100.00,
			"limit_counts": 1,
			"using_limit": "",
			"count": 5,
			"start_date": "2015-01-01",
			"end_date": "1天后",
			"description":"使用说明",
			"coupon_product": "多规格商品2-zhouxun",
			"coupon_id_prefix": "coupon3_id_"
		}]
		"""

	#发放优惠券
	When zhouxun创建优惠券发放规则发放优惠券::weapp
		"""
		{
			"name": "多商品券1",
			"count": 1,
			"members": ["bill"]
		}
		"""

	When bill访问zhouxun的webapp::apiserver 
	When bill购买zhouxun的商品::apiserver
		"""
		{
			"order_id":"003",
			"date":"2016-03-01",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type": "微信支付",
			"coupon": "coupon3_id_1",
			"products":[{
				"name":"多规格商品2-zhouxun",
				"model": "黑色 M",
				"count": 1
			},{
				"name":"多规格商品2-zhouxun",
				"model": "白色 S",
				"count": 1
			}],
			"postage": 0.00
		}
		"""

	Given zhouxun登录系统
	Then zhouxun获得订单列表
		"""
		[{
			"bid": "003",
			"status_code": "paid",
			"pay_interface_type_code": "preference",
			"pay_money": 0.00,
			"product_price": 41.44,
			"postage":0.00,
			"save_money": 41.44,
			"origin_final_price": 0.00,
			"final_price": 0.00,
			"coupon_money": 41.44,
			"extra_coupon_info":{
				"bid":"coupon3_id_1",
				"type":"multi_products_coupon"
			},
			"delivery_items": [{
				"bid": "003-zhouxun",
				"status_code": "paid",
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "zhouxun"
				},
				"products": [{
					"name":"多规格商品2-zhouxun",
					"product_model_name_texts": ["黑色","M"],
					"count": 1
				},{
					"name":"多规格商品2-zhouxun",
					"product_model_name_texts": ["白色", "S"],
					"count": 1
				}]
			}]
		}]
		"""

	Then zhouxun获得订单'003'
		"""
		{
			"bid": "003",
			"status_code": "paid",
			"pay_interface_type_code": "preference",
			"coupon_money": 41.44,
			"extra_coupon_info":{
				"bid":"coupon3_id_1",
				"type":"multi_products_coupon"
			},
			"pay_money": 0.00,
			"product_price": 41.44,
			"postage":0.00,
			"save_money": 41.44,
			"origin_final_price": 0.00,
			"final_price": 0.00,
			"delivery_items": [{
				"bid": "003-zhouxun",
				"status_code": "paid",
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "zhouxun"
				},
				"products": [{
					"name":"多规格商品2-zhouxun",
					"product_model_name_texts": ["黑色","M"],
					"count": 1
				},{
					"name":"多规格商品2-zhouxun",
					"product_model_name_texts": ["白色", "S"],
					"count": 1
				}]
			}]
		}
		"""

@gaiax @order
Scenario:4 使用多品券的多供货商多规格商品订单（优惠券金额超出商品金额）
	#创建多商品券
	Given zhouxun登录系统::weapp
	When zhouxun添加优惠券规则::weapp
		"""
		[{
			"name": "多商品券2",
			"money": 100.00,
			"limit_counts": 1,
			"using_limit": "",
			"count": 5,
			"start_date": "2015-01-01",
			"end_date": "1天后",
			"description":"使用说明",
			"coupon_product": "无规格商品1-yangmi,多规格商品2-zhouxun",
			"coupon_id_prefix": "coupon4_id_"
		}]
		"""

	#发放优惠券
	When zhouxun创建优惠券发放规则发放优惠券::weapp
		"""
		{
			"name": "多商品券2",
			"count": 1,
			"members": ["bill"]
		}
		"""

	When bill访问zhouxun的webapp::apiserver 
	When bill购买zhouxun的商品::apiserver
		"""
		{
			"order_id":"004",
			"date":"2016-04-01",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type": "微信支付",
			"coupon": "coupon4_id_1",
			"products":[{
				"name": "无规格商品1-yangmi",
				"count": 1
			},{
				"name": "无规格商品1-zhouxun",
				"count": 1
			},{
				"name":"多规格商品2-zhouxun",
				"model": "黑色 M",
				"count": 1
			},{
				"name":"多规格商品2-zhouxun",
				"model": "白色 S",
				"count": 1
			}],
			"postage": 0.00
		}
		"""

	Given zhouxun登录系统
	Then zhouxun获得订单列表
		"""
		[{
			"bid": "004",
			"status_code": "created",
			"pay_interface_type_code": "weixin_pay",
			"pay_money": 10.11,
			"product_price": 61.55,
			"postage":0.00,
			"save_money": 51.44,
			"origin_final_price": 10.11,
			"final_price": 10.11,
			"coupon_money": 51.44,
			"extra_coupon_info":{
				"bid":"coupon4_id_1",
				"type":"multi_products_coupon"
			},
			"delivery_items": [{
				"bid": "004-yangmi",
				"status_code": "created",
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "yangmi"
				},
				"products": [{
					"name": "无规格商品1-yangmi",
					"count": 1
				}]
			},{
				"bid": "004-zhouxun",
				"status_code": "created",
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "zhouxun"
				},
				"products": [{
					"name": "无规格商品1-zhouxun",
					"count": 1
				},{
					"name":"多规格商品2-zhouxun",
					"product_model_name_texts": ["黑色","M"],
					"count": 1
				},{
					"name":"多规格商品2-zhouxun",
					"product_model_name_texts": ["白色", "S"],
					"count": 1
				}]
			}]
		}]
		"""

	Then zhouxun获得订单'004'
		"""
		{
			"bid": "004",
			"status_code": "created",
			"pay_interface_type_code": "weixin_pay",
			"coupon_money": 51.44,
			"extra_coupon_info":{
				"bid":"coupon4_id_1",
				"type":"multi_products_coupon"
			},
			"pay_money": 10.11,
			"product_price": 61.55,
			"postage":0.00,
			"save_money": 51.44,
			"origin_final_price": 10.11,
			"final_price": 10.11,
			"delivery_items": [{
				"bid": "004-yangmi",
				"status_code": "created",
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "yangmi"
				},
				"products": [{
					"name": "无规格商品1-yangmi",
					"count": 1
				}]
			},{
				"bid": "004-zhouxun",
				"status_code": "created",
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "zhouxun"
				},
				"products": [{
					"name": "无规格商品1-zhouxun",
					"count": 1
				},{
					"name":"多规格商品2-zhouxun",
					"product_model_name_texts": ["黑色","M"],
					"count": 1
				},{
					"name":"多规格商品2-zhouxun",
					"product_model_name_texts": ["白色", "S"],
					"count": 1
				}]
			}]
		}
		"""

@gaiax @order
Scenario:5 管理员退款使用优惠券的订单,优惠券不返还
	#创建通用券10元
	Given zhouxun登录系统::weapp
	When zhouxun添加优惠券规则::weapp
		"""
		[{
			"name": "通用券3",
			"money": 10.00,
			"limit_counts": "无限",
			"count": 3,
			"start_date": "2013-10-10",
			"end_date": "10天后",
			"description":"使用说明",
			"coupon_id_prefix": "coupon5_id_"
		}]
		"""


	Given zhouxun登录系统::weapp
	When zhouxun创建优惠券发放规则发放优惠券::weapp
		"""
		{
			"name": "通用券3",
			"count": 1,
			"members": ["bill"]
		}
		"""
	When bill访问zhouxun的webapp::apiserver
	When bill购买zhouxun的商品::apiserver
		"""
		{
			"order_id":"005",
			"date":"2016-05-01",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type": "微信支付",
			"coupon": "coupon5_id_1",
			"products":[{
				"name":"无规格商品1-zhouxun",
				"count":1
			}],
			"postage": 0.00
		}
		"""
	When bill使用支付方式'微信支付'进行支付订单'005'于2016-05-01 10:00:00::apiserver

	Given zhouxun登录系统
	Then zhouxun能获得优惠券'通用券3'的码库::weapp
		"""
		{
			"coupon5_id_1": {
				"money": 10.00,
				"status": "已使用",
				"consumer": "bill",
				"target": "bill"
			},
			"coupon5_id_2": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon5_id_3": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""

	When zhouxun申请退款出货单'005-zhouxun'
		"""
		{
			"cash":5.00,
			"weizoom_card_money":0.00,
			"coupon_money":5.11,
			"integral":0,
			"member_card_money":0.00,
			"time": "2016-05-02 10:00:00"
		}
		"""

	Then zhouxun能获得优惠券'通用券3'的码库::weapp
		"""
		{
			"coupon5_id_1": {
				"money": 10.00,
				"status": "已使用",
				"consumer": "bill",
				"target": "bill"
			},
			"coupon5_id_2": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon5_id_3": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""

	When zhouxun退款成功出货单'005-zhouxun'
		"""
		{
			"time": "2016-05-02 11:00:00"
		}
		"""

	Then zhouxun能获得优惠券'通用券3'的码库::weapp
		"""
		{
			"coupon5_id_1": {
				"money": 10.00,
				"status": "已使用",
				"consumer": "bill",
				"target": "bill"
			},
			"coupon5_id_2": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon5_id_3": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""