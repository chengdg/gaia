Feature:管理员退款成功出货单

Background:

@order
Scenario:1 管理员退款成功单供货商的订单-待发货
	Given 重置'apiserver'的bdd环境

	Given zhouxun登录系统
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
		}]
		"""
	When zhouxun将商品移动到'在售'货架
		"""
		["无规格商品1", "无规格商品2"]
		"""

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
	When bill使用支付方式'微信支付'进行支付订单'001'于2016-01-01 10:00:00::apiserver

	Given zhouxun登录系统
	When zhouxun申请退款出货单'001-zhouxun'
		"""
		{
			"cash":10.00,
			"weizoom_card_money":0.00,
			"coupon_money":40.11,
			"integral":0,
			"member_card_money":0.00,
			"time": "2016-01-02 10:00:00"
		}
		"""
	When zhouxun退款成功出货单'001-zhouxun'
		"""
		{
			"time": "2016-01-02 11:00:00"
		}
		"""

	Then zhouxun获得订单列表
		"""
		[{
			"bid": "001",
			"status_code": "refunded",
			"pay_interface_type_code": "weixin_pay"
			"pay_money": 40.11,
			"product_price": 50.11,
			"postage":0.00,
			"save_money": 0.00,
			"origin_final_price": 50.11,
			"origin_weizoom_card_money": 0.00,
			"origin_member_card_money": 0.00,
			"final_price": 40.11,
			"weizoom_card_money": 0.00,
			"member_card_money": 0.00,
			"refunding_info": {
				"cash": 10.00,
				"weizoom_card_money": 0.00,
				"member_card_money": 0.00,
				"coupon_money": 40.11,
				"integral": 0,
				"integral_money": 0.00,
				"total": 50.11
			},
			"delivery_items": [{
				"bid": "001-zhouxun",
				"status_code": "refunded",
				"refunding_info": {
					"finished": true,
					"total_can_refund": 50.11,
					"cash": 10.00,
					"weizoom_card_money": 0.00,
					"member_card_money":0.00,
					"coupon_money": 40.11,
					"integral": 0,
					"integral_money": 0.00,
					"total": 50.11
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
		[{
			"bid": "001",
			"status_code": "refunded",
			"status_logs":[{
				"from_status_code":"",
				"to_status_code":"created",
				"time":"2016-01-01 00:00:00"
			},{
				"from_status_code":"created",
				"to_status_code":"paid",
				"time":"2016-01-01 10:00:00"
			},{
				"from_status_code":"paid",
				"to_status_code":"refunding",
				"time":"2016-01-02 10:00:00"
			},{
				"from_status_code":"refunding",
				"to_status_code":"refunded",
				"time":"2016-01-02 11:00:00"
			}],
			"operation_logs":[{
				"action_text":"下单",
				"operator":"客户",
				"time":"2016-01-01 00:00:00"
			},{
				"action_text":"支付",
				"operator":"客户",
				"time":"2016-01-01 10:00:00"
			},{
				"action_text":"退款",
				"operator":"zhouxun",
				"time":"2016-01-02 10:00:00"
			},{
				"action_text":"退款完成",
				"operator":"zhouxun",
				"time":"2016-01-02 11:00:00"
			}],
			"pay_interface_type_code": "weixin_pay"
			"pay_money": 40.11,
			"product_price": 50.11,
			"postage":0.00,
			"save_money": 0.00,
			"origin_final_price": 50.11,
			"origin_weizoom_card_money": 0.00,
			"final_price": 40.11,
			"weizoom_card_money": 0.00,
			"refunding_info": {
				"cash": 10.00,
				"weizoom_card_money": 0.00,
				"member_card_money": 0.00,
				"coupon_money": 40.11,
				"integral": 0,
				"integral_money": 0.00,
				"total": 50.11
			},
			"delivery_items": [{
				"bid": "001-zhouxun",
				"status_code": "refunding",
				"operation_logs":[{
					"action_text":"下单",
					"operator":"客户",
					"time":"2016-01-01 00:00:00"
				},{
					"action_text":"支付",
					"operator":"zhouxun",
					"time":"2016-01-01 10:00:00"
				},{
					"action_text":"退款",
					"operator":"zhouxun",
					"time":"2016-01-02 10:00:00"
				},{
					"action_text":"退款完成",
					"operator":"zhouxun",
					"time":"2016-01-02 11:00:00"
				}],
				"postage": 0.00,
				"refunding_info": {
					"finished": true,
					"cash": 10.00,
					"weizoom_card_money": 0.00,
					"member_card_money":0.00,
					"coupon_money": 40.11,
					"integral": 0,
					"integral_money": 0.00,
					"total": 50.11
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

@order
Scenario:2 管理员退款成功多供货商的订单-已发货
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
	Given zhouxun设定会员积分策略
		"""
		{
			"integral_each_yuan": 20
		}
		"""
	And zhouxun已添加商品规格
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
	When zhouxun添加支付方式
		"""
		[{
			"type": "支付宝",
			"is_active": "启用"
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
		["无规格商品1-zhouxun", "多规格商品2-zhouxun","无规格商品1-yangmi"]
		"""

	Given bill关注zhouxun的公众号::apiserver
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
			"pay_type": "支付宝",
			"products": [{
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
	When bill使用支付方式'支付宝'进行支付订单'002'于2016-02-01 10:00:00::apiserver

	Given zhouxun登录系统
	When zhouxun对出货单进行发货
		"""
		[{
			"delivery_item_bid":"002-zhouxun",
			"with_logistics":true,
			"with_logistics_trace":true,
			"express_company_name_value":"顺丰速运",
			"express_number":"147258369",
			"leader_name":"zhouxun|002",
			"time":"2016-02-01 11:00:00"
		}]
		"""
	When zhouxun申请退款出货单'002-zhouxun'
		"""
		{
			"cash":0.00,
			"weizoom_card_money":0.00,
			"coupon_money":40.10,
			"integral":229,
			"member_card_money":0.00,
			"time": "2016-02-02 10:00:00"
		}
		"""
	When zhouxun退款成功出货单'002-zhouxun'
		"""
		{
			,
			"time": "2016-02-02 11:00:00"
		}
		"""

	Then zhouxun获得订单列表
		"""
		[{
			"bid": "002",
			"status_code": "paid",
			"pay_interface_type_code": "alipay"
			"pay_money": 61.55,
			"product_price": 61.55,
			"postage":0.00,
			"save_money": 0.00,
			"origin_final_price": 61.55,
			"origin_weizoom_card_money": 0.00,
			"origin_member_card_money": 0.00,
			"final_price": 61.55,
			"weizoom_card_money": 0.00,
			"member_card_money": 0.00,
			"refunding_info": {
				"cash": 0.00,
				"weizoom_card_money": 0.00,
				"member_card_money": 0.00,
				"coupon_money": 40.10,
				"integral": 229,
				"integral_money": 11.45,
				"total": 51.55
			},
			"delivery_items": [{
				"bid": "002-yangmi",
				"status_code": "paid",
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
				"status_code": "refunded",
				"refunding_info": {
					"finished": true,
					"total_can_refund": 51.55,
					"cash": 0.00,
					"weizoom_card_money": 0.00,
					"member_card_money":0.00,
					"coupon_money": 40.10,
					"integral": 229,
					"integral_money": 11.45,
					"total": 51.55
					},
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "zhouxun"
				},
				"products": [{
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
				}]
			}]
		}]
		"""

	Then zhouxun获得订单'002'
		"""
		[{
			"bid": "002",
			"status_code": "paid",
			"status_logs":[{
				"from_status_code":"",
				"to_status_code":"created",
				"time":"2016-02-01 00:00:00"
			},{
				"from_status_code":"created",
				"to_status_code":"paid",
				"time":"2016-02-01 10:00:00"
			}],
			"operation_logs":[{
				"action_text":"下单",
				"operator":"客户",
				"time":"2016-02-01 00:00:00"
			},{
				"action_text":"支付",
				"operator":"客户",
				"time":"2016-02-01 10:00:00"
			}],
			"pay_interface_type_code": "alipay"
			"pay_money": 61.55,
			"product_price": 61.55,
			"postage":0.00,
			"save_money": 0.00,
			"origin_final_price": 61.55,
			"origin_weizoom_card_money": 0.00,
			"final_price": 61.55,
			"weizoom_card_money": 0.00,
			"refunding_info": {
				"cash": 0.00,
				"weizoom_card_money": 0.00,
				"member_card_money": 0.00,
				"coupon_money": 40.10,
				"integral": 229,
				"integral_money": 11.45,
				"total": 51.55
			},
			"delivery_items": [{
				"bid": "002-yangmi",
				"status_code": "paid",
				"operation_logs":[{
					"action_text":"下单",
					"operator":"客户",
					"time":"2016-02-01 00:00:00"
				},{
					"action_text":"支付",
					"operator":"客户",
					"time":"2016-02-01 10:00:00"
				}],
				"postage": 0.00,
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
				"status_code": "refunded",
				"operation_logs":[{
					"action_text":"下单",
					"operator":"客户",
					"time":"2016-02-01 00:00:00"
				},{
					"action_text":"支付",
					"operator":"客户",
					"time":"2016-02-01 10:00:00"
				},{
					"action_text":"订单发货",
					"operator":"zhouxun",
					"time":"2016-02-01 11:00:00"
				},{
					"action_text":"退款",
					"operator":"zhouxun",
					"time":"2016-02-02 10:00:00"
				},{
					"action_text":"退款完成",
					"operator":"zhouxun",
					"time":"2016-02-02 11:00:00"
				}],
				"postage": 0.00,
				"refunding_info": {
					"finished": true,
					"cash": 0.00,
					"weizoom_card_money": 0.00,
					"member_card_money":0.00,
					"coupon_money": 40.10,
					"integral": 229,
					"integral_money": 11.45,
					"total": 51.55
					},
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "zhouxun"
				},
				"products": [{
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
				}]
			}]
		}]
		"""

@order
Scenario:3 管理员退款成功多供货商的订单-带运费-待发货，已完成
	Given 重置'apiserver'的bdd环境
	Given 重置'weapp'的bdd环境

	Given yangmi登录系统
	When yangmi添加商品
		"""
		[{
			"name": "无规格商品1-yangmi",
			"postage_type": "统一运费",
			"unified_postage_money": 10.00,
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
	Given zhouxun设定会员积分策略
		"""
		{
			"integral_each_yuan": 20
		}
		"""
	And zhouxun已添加商品规格
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
	When zhouxun添加支付方式
		"""
		[{
			"type": "支付宝",
			"is_active": "启用"
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
			"postage_type": "统一运费",
			"unified_postage_money": 10.00,
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
		["无规格商品1-zhouxun", "多规格商品2-zhouxun","无规格商品1-yangmi"]
		"""

	Given bill关注zhouxun的公众号::apiserver
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
			"pay_type": "支付宝",
			"products": [{
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
			"postage": 20.00
		}
		"""
	When bill使用支付方式'支付宝'进行支付订单'003'于2016-03-01 10:00:00::apiserver

	Given zhouxun登录系统
	When zhouxun对出货单进行发货
		"""
		[{
			"delivery_item_bid":"003-zhouxun",
			"with_logistics":true,
			"with_logistics_trace":true,
			"express_company_name_value":"顺丰速运",
			"express_number":"147258369",
			"leader_name":"zhouxun|003",
			"time":"2016-03-02 10:00:00"
		}]
		"""
	When zhouxun完成出货单'003-zhouxun'
		"""
		{
			"time":"2016-02-02 11:00:00"
		}
		"""
	When zhouxun申请退款出货单'003-zhouxun'
		"""
		{
			"cash":0.00,
			"weizoom_card_money":0.00,
			"coupon_money":50.10,
			"integral":229,
			"member_card_money":0.00,
			"time":"2016-03-04 10:00:00"
		}
		"""
	When zhouxun申请退款出货单'003-yangmi'于'2016-03-04 11:00:00'
		"""
		{
			"cash":10.00,
			"weizoom_card_money":0.00,
			"coupon_money":10.00,
			"integral":0,
			"member_card_money":0.00,
			"time":"2016-03-04 11:00:00"
		}
		"""
	When zhouxun退款成功出货单'003-zhouxun'
		"""
		{
			"time":"2016-03-04 12:00:00"
		}
		"""
	When zhouxun退款成功出货单'003-yangmi'
		"""
		{
			"time":"2016-03-04 13:00:00"
		}
		"""

	Then zhouxun获得订单列表
		"""
		[{
			"bid": "003",
			"status_code": "refunded",
			"pay_interface_type_code": "alipay"
			"pay_money": 71.55,
			"product_price": 61.55,
			"postage":20.00,
			"save_money": 0.00,
			"origin_final_price": 81.55,
			"origin_weizoom_card_money": 0.00,
			"origin_member_card_money": 0.00,
			"final_price": 71.55,
			"weizoom_card_money": 0.00,
			"member_card_money": 0.00,
			"refunding_info": {
				"cash": 10.00,
				"weizoom_card_money": 0.00,
				"member_card_money": 0.00,
				"coupon_money": 10.00,
				"integral": 0,
				"integral_money": 0.00,
				"total": 0.00
			},
			"delivery_items": [{
				"bid": "003-yangmi",
				"status_code": "refunded",
				"refunding_info": {
					"finished": true,
					"total_can_refund": 20.00,
					"cash": 10.00,
					"weizoom_card_money": 0.00,
					"member_card_money":0.00,
					"coupon_money": 60.10,
					"integral": 229,
					"integral_money": 11.45,
					"total": 81.55
					},
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "yangmi"
				},
				"products": [{
					"name": "无规格商品1-yangmi",
					"count": 1
				}]
			},{
				"bid": "003-zhouxun",
				"status_code": "refunded",
				"refunding_info": {
					"finished": true,
					"total_can_refund": 61.55,
					"cash": 0.00,
					"weizoom_card_money": 0.00,
					"member_card_money":0.00,
					"coupon_money": 50.10,
					"integral": 229,
					"integral_money": 11.45,
					"total": 61.55
					},
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "zhouxun"
				},
				"products": [{
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
				}]
			}]
		}]
		"""

	Then zhouxun获得订单'003'
		"""
		[{
			"bid": "003",
			"status_code": "refunding",
			"status_logs":[{
				"from_status_code":"",
				"to_status_code":"created",
				"time":"2016-03-01 00:00:00"
			},{
				"from_status_code":"created",
				"to_status_code":"paid",
				"time":"2016-03-01 10:00:00"
			},{
				"from_status_code":"paid",
				"to_status_code":"refunding",
				"time":"2016-03-04 11:00:00"
			},{
				"from_status_code":"refunding",
				"to_status_code":"refunded",
				"time":"2016-03-04 13:00:00"
			}],
			"operation_logs":[{
				"action_text":"下单",
				"operator":"客户",
				"time":"2016-03-01 00:00:00"
			},{
				"action_text":"支付",
				"operator":"客户",
				"time":"2016-03-01 10:00:00"
			},{
				"action_text":"退款",
				"operator":"zhouxun",
				"time":"2016-03-04 11:00:00"
			},{
				"action_text":"退款完成",
				"operator":"zhouxun",
				"time":"2016-03-04 13:00:00"
			}],
			"pay_interface_type_code": "alipay"
			"pay_money": 71.55,
			"product_price": 61.55,
			"postage":20.00,
			"save_money": 0.00,
			"origin_final_price": 81.55,
			"origin_weizoom_card_money": 0.00,
			"final_price": 71.55,
			"weizoom_card_money": 0.00,
			"refunding_info": {
				"cash": 10.00,
				"weizoom_card_money": 0.00,
				"member_card_money": 0.00,
				"coupon_money": 60.11,
				"integral": 229,
				"integral_money": 11.45,
				"total": 81.55
			},
			"delivery_items": [{
				"bid": "003-yangmi",
				"status_code": "refunded",
				"refunding_info": {
					"finished": true,
					"cash": 10.00,
					"weizoom_card_money": 0.00,
					"member_card_money":0.00,
					"coupon_money": 10.00,
					"integral": 0,
					"integral_money": 0.00,
					"total": 20.00
					},
				"operation_logs":[{
					"action_text":"下单",
					"operator":"客户",
					"time":"2016-03-01 00:00:00"
				},{
					"action_text":"支付",
					"operator":"客户",
					"time":"2016-03-01 10:00:00"
				},{
					"action_text":"退款",
					"operator":"zhouxun",
					"time":"2016-03-04 11:00:00"
				},{
					"action_text":"退款完成",
					"operator":"zhouxun",
					"time":"2016-03-04 12:00:00"
				}],
				"postage": 10.00,
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "yangmi"
				},
				"products": [{
					"name": "无规格商品1-yangmi",
					"count": 1
				}]
			},{
				"bid": "003-zhouxun",
				"status_code": "refunded",
				"operation_logs":[{
					"action_text":"下单",
					"operator":"客户",
					"time":"2016-03-01 00:00:00"
				},{
					"action_text":"支付",
					"operator":"客户",
					"time":"2016-03-01 10:00:00"
				},{
					"action_text":"订单发货",
					"operator":"zhouxun",
					"time":"2016-03-02 10:00:00"
				},{
					"action_text":"完成",
					"operator":"zhouxun",
					"time":"2016-03-03 10:00:00"
				},{
					"action_text":"退款",
					"operator":"zhouxun",
					"time":"2016-03-04 10:00:00"
				},{
					"action_text":"退款完成",
					"operator":"zhouxun",
					"time":"2016-03-04 13:00:00"
				}],
				"postage": 10.00,
				"refunding_info": {
					"finished": true,
					"cash": 0.00,
					"weizoom_card_money": 0.00,
					"member_card_money":0.00,
					"coupon_money": 50.10,
					"integral": 229,
					"integral_money": 11.45,
					"total": 61.55
					},
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "zhouxun"
				},
				"products": [{
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
				}]
			}]
		}]
		"""

@order
Scenario:4 管理员退款成功使用微众卡全额支付的订单
	Given 重置'weizoom_card'的bdd环境
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
	Given zhouxun设定会员积分策略
		"""
		{
			"integral_each_yuan": 20
		}
		"""
	And zhouxun已添加商品规格
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
	And zhouxun开通使用微众卡权限::weapp
	When zhouxun添加支付方式
		"""
		[{
			"type": "支付宝",
			"is_active": "启用"
		},{
			"type":"微众卡支付"
		}]
		"""
	#创建微众卡
		Given test登录管理系统::weizoom_card
		When test新建通用卡::weizoom_card
			"""
			[{
				"name":"100元微众卡",
				"prefix_value":"100",
				"type":"virtual",
				"money":"100.00",
				"num":"2",
				"comments":"微众卡"
			}]
			"""
		#微众卡审批出库
		When test下订单::weizoom_card
			"""
			[{
				"card_info":[{
					"name":"100元微众卡",
					"order_num":"2",
					"start_date":"2015-04-07 00:00",
					"end_date":"2019-10-07 00:00"
				}],
				"order_info":{
					"order_id":"0001"
					}
			}]
			"""
		#激活微众
		When test激活卡号'100000001'的卡::weizoom_card

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
		["无规格商品1-zhouxun", "多规格商品2-zhouxun","无规格商品1-yangmi"]
		"""

	Given bill关注zhouxun的公众号::apiserver
	When bill访问zhouxun的webapp::apiserver 
	When bill绑定微众卡::apiserver
		"""
		{
			"binding_date":"2016-01-01",
			"binding_shop":"zhouxun",
			"weizoom_card_info":
				{
					"id":"100000001",
					"password":"1234567"
				}
		}
		"""
	When bill购买zhouxun的商品::apiserver
		"""
		{
			"order_id":"004",
			"date":"2016-04-01",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type": "支付宝",
			"weizoom_card":[{
				"card_name":"100000001",
				"card_pass":"1234567"
				}],
			"products": [{
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

	#查看微众卡余额
		When bill访问zhouxun的webapp::weapp
		When bill进行微众卡余额查询::weapp
			"""
			{
				"id":"100000001",
				"password":"1234567"
			}
			"""
		Then bill获得微众卡余额查询结果::weapp
			"""
			{
				"card_remaining":38.45
			}
			"""
	#查看会员使用微众卡数据
		Given zhouxun登录系统
		Then zhouxun获得'bill'的购买信息::weapp
			"""
			{
				"purchase_amount":61.55,
				"purchase_number":1,
				"customer_price":61.55,
				"money_wcard":61.55
			}
			"""

	When zhouxun申请退款出货单'004-zhouxun'于'2016-04-02 10:00:00'
		"""
		{
			"cash":0.00,
			"weizoom_card_money":20.35,
			"coupon_money":10.00,
			"integral":424,
			"member_card_money":0.00,
			"time":"2016-04-02 10:00:00"
		}
		"""
	When zhouxun退款成功出货单'004-zhouxun'
		"""
		{
			"time":"2016-04-02 11:00:00"
		}
		"""

	#查看微众卡余额
		When bill访问zhouxun的webapp::weapp
		When bill进行微众卡余额查询::weapp
			"""
			{
				"id":"100000001",
				"password":"1234567"
			}
			"""
		Then bill获得微众卡余额查询结果::weapp
			"""
			{
				"card_remaining":38.45
			}
			"""
	#查看会员使用微众卡数据
		Given zhouxun登录系统
		Then zhouxun获得'bill'的购买信息::weapp
			"""
			{
				"purchase_amount":0.00,
				"purchase_number":0,
				"customer_price":0.00,
				"money_wcard":0.00
			}
			"""

	Then zhouxun获得订单列表
		"""
		[{
			"bid": "004",
			"status_code": "paid",
			"pay_interface_type_code": "preference"
			"pay_money": 41.20,
			"product_price": 61.55,
			"postage":0.00,
			"save_money": 0.00,
			"origin_final_price": 0.00,
			"origin_weizoom_card_money": 61.55,
			"origin_member_card_money": 0.00,
			"final_price": 0.00,
			"weizoom_card_money": 41.20,
			"member_card_money": 0.00,
			"refunding_info": {
				"cash": 0.00,
				"weizoom_card_money": 20.35,
				"member_card_money": 0.00,
				"coupon_money": 10.00,
				"integral": 424,
				"integral_money": 21.20,
				"total": 51.55
			},
			"delivery_items": [{
				"bid": "004-yangmi",
				"status_code": "paid",
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
				"status_code": "refunded",
				"refunding_info": {
					"finished": true,
					"total_can_refund": 51.55,
					"cash": 0.00,
					"weizoom_card_money": 20.35,
					"member_card_money":0.00,
					"coupon_money": 10.00,
					"integral": 424,
					"integral_money": 21.20,
					"total": 51.55
					},
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "zhouxun"
				},
				"products": [{
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
				}]
			}]
		}]
		"""

	Then zhouxun获得订单'004'
		"""
		[{
			"bid": "004",
			"status_code": "paid",
			"status_logs":[{
				"from_status_code":"",
				"to_status_code":"created",
				"time":"2016-04-01 00:00:00"
			},{
				"from_status_code":"created",
				"to_status_code":"paid",
				"time":"2016-04-01 00:00:00"
			}],
			"operation_logs":[{
				"action_text":"下单",
				"operator":"客户",
				"time":"2016-04-01 00:00:00"
			},{
				"action_text":"支付",
				"operator":"客户",
				"time":"2016-04-01 00:00:00"
			}],
			"pay_interface_type_code": "preference"
			"pay_money": 41.20,
			"product_price": 61.55,
			"postage":0.00,
			"save_money": 0.00,
			"origin_final_price": 0.00,
			"origin_weizoom_card_money": 61.55,
			"final_price": 0.00,
			"weizoom_card_money": 41.20,
			"weizoom_card_info": {
				"used_card": ["100000001"]
			},
			"refunding_info": {
				"cash": 0.00,
				"weizoom_card_money": 20.35,
				"member_card_money": 0.00,
				"coupon_money": 10.00,
				"integral": 424,
				"integral_money": 21.20,
				"total": 51.55
			},
			"delivery_items": [{
				"bid": "004-yangmi",
				"status_code": "paid",
				"operation_logs":[{
					"action_text":"下单",
					"operator":"客户",
					"time":"2016-04-01 00:00:00"
				},{
					"action_text":"支付",
					"operator":"客户",
					"time":"2016-04-01 00:00:00"
				}],
				"postage": 0.00,
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
				"status_code": "refunded",
				"operation_logs":[{
					"action_text":"下单",
					"operator":"客户",
					"time":"2016-04-01 00:00:00"
				},{
					"action_text":"支付",
					"operator":"客户",
					"time":"2016-04-01 00:00:00"
				},{
					"action_text":"退款",
					"operator":"zhouxun",
					"time":"2016-04-02 10:00:00"
				},{
					"action_text":"退款完成",
					"operator":"zhouxun",
					"time":"2016-04-02 11:00:00"
				}],
				"postage": 0.00,
				"refunding_info": {
					"finished": true,
					"cash": 0.00,
					"weizoom_card_money": 20.35,
					"member_card_money":0.00,
					"coupon_money": 10.00,
					"integral": 424,
					"integral_money": 21.20,
					"total": 51.55
					},
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "zhouxun"
				},
				"products": [{
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
				}]
			}]
		}]
		"""

@order
Scenario:5 管理员退款成功使用积分的订单
	Given 重置'apiserver'的bdd环境
	Given 重置'weapp'的bdd环境

	Given zhouxun登录系统
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
		}]
		"""
	When zhouxun将商品移动到'在售'货架
		"""
		["无规格商品1", "无规格商品2"]
		"""

	Given zhouxun设定会员积分策略
		"""
		{
			"integral_each_yuan": 20
		}
		"""
	When zhouxun创建积分应用活动::weapp
		"""
		[{
			"name": "积分应用活动1",
			"start_date": "2015-10-10",
			"end_date": "1天后",
			"product_name": "无规格商品2",
			"is_permanant_active": false,
			"rules": [{
				"member_grade": "全部",
				"discount": 50,
				"discount_money": 10.00
			}]
		}]
		"""

	Given bill关注zhouxun的公众号::apiserver

	Given zhouxun登录系统
	When zhouxun给"bill"加积分::weapp
		"""
		{
			"integral":500,
			"reason":""
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
			"products":[{
				"name":"无规格商品1",
				"count":1
			},{
				"name":"无规格商品2",
				"count":2,
				"integral": 400,
				"integral_money": 20.00
			}],
			"postage": 0.00
		}
		"""
	When bill使用支付方式'微信支付'进行支付订单'005'于2016-05-01 10:00:00::apiserver

	Given zhouxun登录系统
	Then bill在zhouxun的webapp中拥有100会员积分::weapp

	When zhouxun申请退款出货单'005-zhouxun'
		"""
		{
			"cash":10.00,
			"weizoom_card_money":0.00,
			"coupon_money":30.11,
			"integral":200,
			"member_card_money":0.00,
			"time":"2016-05-02 10:00:00"
		}
		"""
	When zhouxun退款成功出货单'005-zhouxun'
		"""
		{
			"time":"2016-05-02 11:00:00"
		}
		"""

	Then bill在zhouxun的webapp中拥有100会员积分::weapp

	Then zhouxun获得订单列表
		"""
		[{
			"bid": "005",
			"status_code": "refunded",
			"pay_interface_type_code": "weixin_pay"
			"pay_money": 20.11,
			"product_price": 50.11,
			"postage":0.00,
			"save_money": 20.00,
			"origin_final_price": 30.11,
			"origin_weizoom_card_money": 0.00,
			"origin_member_card_money": 0.00,
			"final_price": 20.11,
			"weizoom_card_money": 0.00,
			"member_card_money": 0.00,
			"integral": 400,
			"integral_money": 20.00,
			"refunding_info": {
				"cash": 10.00,
				"weizoom_card_money": 0.00,
				"member_card_money": 0.00,
				"coupon_money": 30.11,
				"integral": 200,
				"integral_money": 10.00,
				"total": 50.11
			},
			"delivery_items": [{
				"bid": "005-zhouxun",
				"status_code": "refunded",
				"refunding_info": {
					"finished": true,
					"total_can_refund": 50.11,
					"cash": 10.00,
					"weizoom_card_money": 0.00,
					"member_card_money":0.00,
					"coupon_money": 30.11,
					"integral": 200,
					"integral_money": 10.00,
					"total": 50.11
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

	Then zhouxun获得订单'005'
		"""
		[{
			"bid": "005",
			"status_code": "refunded",
			"pay_interface_type_code": "weixin_pay"
			"pay_money": 20.11,
			"product_price": 50.11,
			"postage":0.00,
			"save_money": 20.00,
			"origin_final_price": 20.11,
			"origin_weizoom_card_money": 0.00,
			"final_price": 20.11,
			"weizoom_card_money": 0.00,
			"integral": 400,
			"integral_money": 20.00,
			"weizoom_card_info": {
				"used_card": []
			},
			"refunding_info": {
				"cash": 10.00,
				"weizoom_card_money": 0.00,
				"member_card_money": 0.00,
				"coupon_money": 30.11,
				"integral": 200,
				"integral_money": 10.00,
				"total": 0.00
			},
			"delivery_items": [{
				"bid": "005-zhouxun",
				"status_code": "refunded",
				"postage": 0.00,
				"refunding_info": {
					"finished": true,
					"cash": 10.00,
					"weizoom_card_money": 0.00,
					"member_card_money":0.00,
					"coupon_money": 30.11,
					"integral": 200,
					"integral_money": 10.00,
					"total": 50.11
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

@order
Scenario:6 管理员退款成功使用优惠券的订单
	Given 重置'apiserver'的bdd环境
	Given 重置'weapp'的bdd环境

	Given zhouxun登录系统
	When zhouxun添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}]
		"""
	#创建优惠券-全体券10元
	When zhouxun添加优惠券规则::weapp
		"""
		[{
			"name": "全店通用券1",
			"money": 10.00,
			"limit_counts": "无限",
			"count": 3,
			"start_date": "2013-10-10",
			"end_date": "10天后",
			"description":"使用说明",
			"coupon_id_prefix": "coupon1_id_"
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
		}]
		"""
	When zhouxun将商品移动到'在售'货架
		"""
		["无规格商品1", "无规格商品2"]
		"""

	Given bill关注zhouxun的公众号::apiserver

	Given zhouxun登录系统
	When zhouxun创建优惠券发放规则发放优惠券::weapp
		"""
		{
			"name": "全店通用券1",
			"count": 1,
			"members": ["bill"]
		}
		"""

	When bill访问zhouxun的webapp::apiserver 
	When bill购买zhouxun的商品::apiserver
		"""
		{
			"order_id":"006",
			"date":"2016-06-01",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type": "微信支付",
			"coupon": "coupon1_id_1",
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
	When bill使用支付方式'微信支付'进行支付订单'001'于2016-06-01 10:00:00::apiserver

	Given zhouxun登录系统
	Then zhouxun能获得优惠券'全体券1'的码库::weapp
		"""
		{
			"coupon1_id_1": {
				"money": 10.00,
				"status": "已使用",
				"consumer": "bill",
				"target": "bill"
			},
			"coupon1_id_2": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon1_id_3": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""

	When zhouxun申请退款出货单'006-zhouxun'
		"""
		{
			"cash":10.00,
			"weizoom_card_money":0.00,
			"coupon_money":40.11,
			"integral":0,
			"member_card_money":0.00,
			"time": "2016-06-02 10:00:00"
		}
		"""
	When zhouxun退款成功出货单'006-zhouxun'
		"""
		{
			"time": "2016-06-02 11:00:00"
		}
		"""

	Then zhouxun能获得优惠券'全体券1'的码库::weapp
		"""
		{
			"coupon1_id_1": {
				"money": 10.00,
				"status": "已使用",
				"consumer": "bill",
				"target": "bill"
			},
			"coupon1_id_2": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			},
			"coupon1_id_3": {
				"money": 10.00,
				"status": "未领取",
				"consumer": "",
				"target": ""
			}
		}
		"""

	Then zhouxun获得订单列表
		"""
		[{
			"bid": "006",
			"status_code": "refunded",
			"pay_interface_type_code": "weixin_pay"
			"pay_money": 30.11,
			"product_price": 50.11,
			"postage":0.00,
			"save_money": 10.00,
			"origin_final_price": 40.11,
			"origin_weizoom_card_money": 0.00,
			"origin_member_card_money": 0.00,
			"final_price": 30.11,
			"weizoom_card_money": 0.00,
			"member_card_money": 0.00,
			"coupon_money": 10.00,
			"refunding_info": {
				"cash": 10.00,
				"weizoom_card_money": 0.00,
				"member_card_money": 0.00,
				"coupon_money": 40.11,
				"integral": 0,
				"integral_money": 0.00,
				"total": 50.11
			},
			"delivery_items": [{
				"bid": "006-zhouxun",
				"status_code": "refunded",
				"refunding_info": {
					"finished": true,
					"total_can_refund": 50.11,
					"cash": 10.00,
					"weizoom_card_money": 0.00,
					"member_card_money":0.00,
					"coupon_money": 40.11,
					"integral": 0,
					"integral_money": 0.00,
					"total": 50.11
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

	Then zhouxun获得订单'006'
		"""
		[{
			"bid": "006",
			"status_code": "refunded",
			"pay_interface_type_code": "weixin_pay"
			"couponMoney": 10.00,
			"pay_money": 30.11,
			"product_price": 50.11,
			"postage":0.00,
			"save_money": 10.00,
			"origin_final_price": 40.11,
			"origin_weizoom_card_money": 0.00,
			"final_price": 30.11,
			"weizoom_card_money": 0.00,
			"refunding_info": {
				"cash": 10.00,
				"weizoom_card_money": 0.00,
				"member_card_money": 0.00,
				"coupon_money": 40.11,
				"integral": 0,
				"integral_money": 0.00,
				"total": 50.11
			},
			"delivery_items": [{
				"bid": "006-zhouxun",
				"status_code": "refunded",
				"postage": 0.00,
				"refunding_info": {
					"finished": true,
					"cash": 10.00,
					"weizoom_card_money": 0.00,
					"member_card_money":0.00,
					"coupon_money": 40.11,
					"integral": 0,
					"integral_money": 0.00,
					"total": 50.11
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

@order
Scenario:7 管理员退款成功出货单，对商品销量和库存的影响
	Given 重置'apiserver'的bdd环境
	Given 重置'weapp'的bdd环境

	Given yangmi登录系统
	When yangmi添加商品
		"""
		[{
			"name": "无规格商品1-yangmi",
			"postage_type": "统一运费",
			"unified_postage_money": 10.00,
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
	Given zhouxun设定会员积分策略
		"""
		{
			"integral_each_yuan": 20
		}
		"""
	And zhouxun已添加商品规格
		"""
		[{
			"name": "颜色",
			"type": "图片",
			"values": [{
				"name": "黑色",
				"image": "/static/test_resource_img/icon_color/black.png"
			}, {
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
	When zhouxun添加支付方式
		"""
		[{
			"type": "支付宝",
			"is_active": "启用"
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
			"postage_type": "统一运费",
			"unified_postage_money": 10.00,
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
		["无规格商品1-zhouxun", "多规格商品2-zhouxun","无规格商品1-yangmi"]
		"""

	#商品销量和库存
	Then zhouxun能获得'在售'商品列表
		"""
		[{
			"name":"无规格商品1-zhouxun",
			"stock_type": "有限",
			"stocks": 100,
			"sales": 0
		},{
			"name":"多规格商品2-zhouxun",
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
			"sales": 0
		},{
			"name":"无规格商品1-yangmi",
			"stock_type": "有限",
			"stocks": 100,
			"sales": 0
		}]
		"""

	Given bill关注zhouxun的公众号::apiserver
	When bill访问zhouxun的webapp::apiserver 
	When bill购买zhouxun的商品::apiserver
		"""
		{
			"order_id":"007",
			"date":"2016-07-01",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type": "支付宝",
			"products": [{
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
			"postage": 20.00
		}
		"""
	When bill使用支付方式'支付宝'进行支付订单'007'于2016-07-01 10:00:00::apiserver

	Given zhouxun登录系统
	When zhouxun对出货单进行发货
		"""
		[{
			"delivery_item_bid":"007-zhouxun",
			"with_logistics":true,
			"with_logistics_trace":true,
			"express_company_name_value":"顺丰速运",
			"express_number":"147258369",
			"leader_name":"zhouxun|007",
			"time":"2016-07-02 10:00:00"
		}]
		"""
	When zhouxun完成出货单'007-zhouxun'
		"""
		{
			"time": "2016-07-03 10:00:00"
		}
		"""

	#商品销量和库存
	Then zhouxun能获得'在售'商品列表
		"""
		[{
			"name":"无规格商品1-zhouxun",
			"stock_type": "有限",
			"stocks": 99,
			"sales": 1
		},{
			"name":"多规格商品2-zhouxun",
			"model":{
				"models": {
					"黑色 M": {
						"price": 20.22,
						"purchase_price": 19.22,
						"stock_type": "有限",
						"stocks": 99
					},
					"白色 S": {
						"price": 21.22,
						"purchase_price": 20.22,
						"stock_type": "有限",
						"stocks": 99
					}
				}
			}
			"sales": 2
		},{
			"name":"无规格商品1-yangmi",
			"stock_type": "有限",
			"stocks": 99,
			"sales": 1
		}]
		"""

	When zhouxun申请退款出货单'007-zhouxun'
		"""
		{
			"cash":0.00,
			"weizoom_card_money":0.00,
			"coupon_money":50.10,
			"integral":229,
			"member_card_money":0.00,
			"time": "2016-07-04 10:00:00"
		}
		"""
	When zhouxun申请退款出货单'007-yangmi'
		"""
		{
			"cash":10.00,
			"weizoom_card_money":0.00,
			"coupon_money":10.00,
			"integral":0,
			"member_card_money":0.00,
			"time": "2016-07-04 11:00:00"
		}
		"""
	When zhouxun退款成功出货单'007-zhouxun'
		"""
		{
			"time": "2016-07-04 12:00:00"
		}
		"""
	When zhouxun退款成功出货单'007-yangmi'
		"""
		{
			"time": "2016-07-04 13:00:00"
		}
		"""

	#商品销量和库存
	Then zhouxun能获得'在售'商品列表
		"""
		[{
			"name":"无规格商品1-zhouxun",
			"stock_type": "有限",
			"stocks": 100,
			"sales": 0
		},{
			"name":"多规格商品2-zhouxun",
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
			"sales": 0
		},{
			"name":"无规格商品1-yangmi",
			"stock_type": "有限",
			"stocks": 100,
			"sales": 0
		}]
		"""

@order
Scenario:8 管理员退款成功出货单，对会员信息的影响
	Given 重置'apiserver'的bdd环境
	Given 重置'weapp'的bdd环境

	Given yangmi登录系统
	When yangmi添加商品
		"""
		[{
			"name": "无规格商品1-yangmi",
			"postage_type": "统一运费",
			"unified_postage_money": 10.00,
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
	Given zhouxun设定会员积分策略
		"""
		{
			"integral_each_yuan": 20
		}
		"""
	And zhouxun已添加商品规格
		"""
		[{
			"name": "颜色",
			"type": "图片",
			"values": [{
				"name": "黑色",
				"image": "/static/test_resource_img/icon_color/black.png"
			}, {
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
	When zhouxun添加支付方式
		"""
		[{
			"type": "支付宝",
			"is_active": "启用"
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
			"postage_type": "统一运费",
			"unified_postage_money": 10.00,
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
		["无规格商品1-zhouxun", "多规格商品2-zhouxun","无规格商品1-yangmi"]
		"""

	Given bill关注zhouxun的公众号::apiserver
	When bill访问zhouxun的webapp::apiserver 
	When bill购买zhouxun的商品::apiserver
		"""
		{
			"order_id":"007",
			"date":"2016-07-01",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type": "支付宝",
			"products": [{
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
			"postage": 20.00
		}
		"""
	When bill使用支付方式'支付宝'进行支付订单'008'于2016-08-01 10:00:00::apiserver

	Given zhouxun登录系统
	When zhouxun对出货单进行发货
		"""
		[{
			"delivery_item_bid":"008-zhouxun",
			"with_logistics":true,
			"with_logistics_trace":true,
			"express_company_name_value":"顺丰速运",
			"express_number":"147258369",
			"leader_name":"zhouxun|008",
			"time":"2016-08-02 10:00:00"
		}]
		"""
	When zhouxun完成出货单'008-zhouxun'
		"""
		{
			"time": "2016-08-03 10:00:00"
		}
		"""
	When zhouxun对出货单进行发货
		"""
		[{
			"delivery_item_bid":"008-yangmi",
			"with_logistics":true,
			"with_logistics_trace":true,
			"express_company_name_value":"顺丰速运",
			"express_number":"147258369",
			"leader_name":"yangmi|008",
			"time":"2016-08-02 10:00:00"
		}]
		"""
	When zhouxun完成出货单'008-yangmi'
		"""
		{
			"time": "2016-08-03 10:00:00"
		}
		"""

	#会员列表数据
	Then zhouxun可以获得会员列表::weapp
		"""
		[{
			"name": "bill",
			"pay_money": 81.55,
			"unit_price": 81.55,
			"pay_times": 1
		}]
		"""

	When zhouxun申请退款出货单'008-zhouxun'
		"""
		{
			"cash":0.00,
			"weizoom_card_money":0.00,
			"coupon_money":50.10,
			"integral":229,
			"member_card_money":0.00,
			"time": "2016-08-04 10:00:00"
		}
		"""
	When zhouxun申请退款出货单'008-yangmi'
		"""
		{
			"cash":10.00,
			"weizoom_card_money":0.00,
			"coupon_money":10.00,
			"integral":0,
			"member_card_money":0.00,
			"time": "2016-08-04 11:00:00"
		}
		"""
	When zhouxun退款成功出货单'008-zhouxun'
		"""
		{
			"time": "2016-08-04 12:00:00"
		}
		"""
	When zhouxun退款成功出货单'008-yangmi'
		"""
		{
			"time": "2016-08-04 13:00:00"
		}
		"""

	#会员列表数据
	Then zhouxun可以获得会员列表::weapp
		"""
		[{
			"name": "bill",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"pay_times": 0
		}]
		"""

@order
Scenario:9 管理员退款出货单，积分设置为1元=0积分
	Given 重置'apiserver'的bdd环境

	Given zhouxun登录系统
	When zhouxun添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}]
		"""
	Given zhouxun设定会员积分策略
		"""
		{
			"integral_each_yuan": 20
		}
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
		}]
		"""
	When zhouxun将商品移动到'在售'货架
		"""
		["无规格商品1", "无规格商品2"]
		"""

	Given bill关注zhouxun的公众号::apiserver
	When bill访问zhouxun的webapp::apiserver 
	When bill购买zhouxun的商品::apiserver
		"""
		{
			"order_id":"009",
			"date":"2016-09-01",
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
	When bill使用支付方式'微信支付'进行支付订单'009'于2016-09-01 10:00:00::apiserver

	Given zhouxun登录系统
	Given zhouxun设定会员积分策略
		"""
		{
			"integral_each_yuan": 0
		}
		"""
	When zhouxun申请退款出货单'009-zhouxun'
		"""
		{
			"cash":10.00,
			"weizoom_card_money":0.00,
			"coupon_money":40.11,
			"integral":20,
			"member_card_money":0.00,
			"time": "2016-09-02 10:00:00"
		}
		"""
	When zhouxun退款成功出货单'009-zhouxun'
		"""
		{
			"time": "2016-09-02 11:00:00"
		}
		"""

	Then zhouxun获得订单列表
		"""
		[{
			"bid": "009",
			"status_code": "refunded",
			"pay_interface_type_code": "weixin_pay"
			"coupon_money": 0.00,
			"pay_money": 40.11,
			"product_price": 50.11,
			"postage":0.00,
			"save_money": 0.00,
			"origin_final_price": 50.11,
			"origin_weizoom_card_money": 0.00,
			"origin_member_card_money": 0.00,
			"final_price": 40.11,
			"weizoom_card_money": 0.00,
			"member_card_money": 0.00,
			"integral": 0,
			"integral_money": 0.00,
			"refunding_info": {
				"cash": 10.00,
				"weizoom_card_money": 0.00,
				"member_card_money": 0.00,
				"coupon_money": 40.11,
				"integral": 20,
				"integral_money": 0.00,
				"total": 50.11
			},
			"delivery_items": [{
				"bid": "009-zhouxun",
				"status_code": "refunded",
				"refunding_info": {
					"finished": true,
					"total_can_refund": 50.11,
					"cash": 10.00,
					"weizoom_card_money": 0.00,
					"member_card_money":0.00,
					"coupon_money": 40.11,
					"integral": 20,
					"integral_money": 0.00,
					"total": 50.11
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

	Then zhouxun获得订单'009'
		"""
		[{
			"bid": "009",
			"status_code": "refunded",
			"status_logs":[{
				"from_status_code":"",
				"to_status_code":"created",
				"time":"2016-09-01 00:00:00"
			},{
				"from_status_code":"created",
				"to_status_code":"paid",
				"time":"2016-09-01 10:00:00"
			},{
				"from_status_code":"paid",
				"to_status_code":"refunding",
				"time":"2016-09-02 10:00:00"
			},{
				"from_status_code":"refunding",
				"to_status_code":"refunded",
				"time":"2016-09-02 11:00:00"
			}],
			"operation_logs":[{
				"action_text":"下单",
				"operator":"客户",
				"time":"2016-09-01 00:00:00"
			},{
				"action_text":"支付",
				"operator":"客户",
				"time":"2016-09-01 10:00:00"
			},{
				"action_text":"退款-zhouxun",
				"operator":"zhouxun",
				"time":"2016-09-02 10:00:00"
			},{
				"action_text":"退款完成-zhouxun",
				"operator":"zhouxun",
				"time":"2016-09-02 11:00:00"
			}],
			"pay_interface_type_code": "weixin_pay"
			"couponMoney": 0.00,
			"pay_money": 40.11,
			"product_price": 50.11,
			"postage":0.00,
			"save_money": 0.00,
			"origin_final_price": 50.11,
			"origin_weizoom_card_money": 0.00,
			"final_price": 40.11,
			"weizoom_card_money": 0.00,
			"integral": 0,
			"integral_money": 0.00,
			"weizoom_card_info": {
				"used_card": []
			},
			"refunding_info": {
				"cash": 10.00,
				"weizoom_card_money": 0.00,
				"member_card_money": 0.00,
				"coupon_money": 40.11,
				"integral": 20,
				"integral_money": 0.00,
				"total": 50.11
			},
			"delivery_items": [{
				"bid": "009-zhouxun",
				"status_code": "refunded",
				"operation_logs":[{
					"action_text":"下单",
					"operator":"客户",
					"time":"2016-09-01 00:00:00"
				},{
					"action_text":"支付",
					"operator":"zhouxun",
					"time":"2016-09-01 10:00:00"
				},{
					"action_text":"退款-zhouxun",
					"operator":"zhouxun",
					"time":"2016-09-02 10:00:00"
				},{
					"action_text":"退款完成-zhouxun",
					"operator":"zhouxun",
					"time":"2016-09-02 11:00:00"
				}],
				"postage": 0.00,
				"refunding_info": {
					"finished": true,
					"cash": 10.00,
					"weizoom_card_money": 0.00,
					"member_card_money":0.00,
					"coupon_money": 40.11,
					"integral": 20,
					"integral_money": 0.00,
					"total": 50.11
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
