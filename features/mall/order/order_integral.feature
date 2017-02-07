# __author__ : "冯雪静"

Feature: 使用整单抵扣积分的相关订单

Background:
	Given 重置'weapp'的bdd环境
	Given 重置'apiserver'的bdd环境
	Given zhouxun登录系统
	When zhouxun添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}]
		"""
	When zhouxun更新积分规则为
		"""
		{
			"integral_each_yuan": 2,
			"be_member_increase_count": 50,
			"use_ceiling": 50
		}
		"""
	Given bill关注zhouxun的公众号::apiserver

@gaiax @order
Scenario: 1 管理员取消使用了订单积分的订单
	1.zhouxun取消待支付订单，积分退回

	Given jobs登录系统
	When jobs添加商品
		"""
		[{
			"name": "jobs商品1",
			"model": {
				"models": {
					"standard": {
						"price": 11.00,
						"stock_type": "有限",
						"stocks": 30
					}
				}
			}
		}]
		"""
	Given zhouxun登录系统
	When zhouxun添加商品
		"""
		[{
			"name": "zhouxun商品3",
			"model": {
				"models": {
					"standard": {
						"price": 10.01,
						"stock_type": "有限",
						"stocks": 30
					}
				}
			}
		}]
		"""
	When zhouxun添加代销商品
		"""
		["jobs商品1"]
		"""
	When zhouxun将商品移动到'在售'货架
		"""
		["zhouxun商品3", "jobs商品1"]
		"""
	When bill访问zhouxun的webapp::apiserver
	When bill获得zhouxun的50会员积分::apiserver
	Then bill在zhouxun的webapp中拥有50会员积分::apiserver
	When bill购买zhouxun的商品::apiserver
		"""
		{
			"order_id":"001",
			"date":"2017-01-20 10:00:00",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type": "微信支付",
			"integral_money": 10.50,
			"integral": 21,
			"products": [{
				"name": "zhouxun商品3",
				"count": 1
			}, {
				"name": "jobs商品1",
				"count": 1
			}]
		}
		"""
	Then bill在zhouxun的webapp中拥有29会员积分::apiserver
	Given zhouxun登录系统
	When zhouxun取消订单'001'
	Then zhouxun获得订单列表
		"""
		[{
			"bid": "001",
			"status_code": "cancelled",
			"integral_money": 10.50,
			"integral": 21,
			"delivery_items": [{
				"bid": "001-zhouxun",
				"status_code": "cancelled",
				"products": [{
					"name": "zhouxun商品3",
					"count": 1,
					"sale_price": 10.01,
					"origin_price": 10.01,
					"promotion_info": {
						"type": "",
						"integral_count": 0,
						"integral_money": 0
					}
				}]
			},{
				"bid": "001-jobs",
				"status_code": "cancelled",
				"products": [{
					"name": "jobs商品1",
					"count": 1,
					"sale_price": 11.00,
					"origin_price": 11.00,
					"promotion_info": {
						"type": "",
						"integral_count": 0,
						"integral_money": 0
					}
				}]
			}]
		}]
		"""
	Then zhouxun获得订单'001'
		"""
		{
			"bid": "001",
			"status_code": "cancelled",
			"integral_type": "整单抵扣",
			"integral_money": 10.50,
			"integral": 21,
			"delivery_items": [{
				"bid": "001-zhouxun",
				"status_code": "cancelled",
				"products": [{
					"name": "zhouxun商品3",
					"count": 1,
					"sale_price": 10.01,
					"origin_price": 10.01,
					"promotion_info": {
						"type": "",
						"integral_count": 0,
						"integral_money": 0
					}
				}]
			},{
				"bid": "001-jobs",
				"status_code": "cancelled",
				"products": [{
					"name": "jobs商品1",
					"count": 1,
					"sale_price": 11.00,
					"origin_price": 11.00,
					"promotion_info": {
						"type": "",
						"integral_count": 0,
						"integral_money": 0
					}
				}]
			}]
		}
		"""
	When bill访问zhouxun的webapp::apiserver
	Then bill在zhouxun的webapp中拥有50会员积分::apiserver
	Given zhouxun登录系统::weapp
#	Then zhouxun能获得bill的积分日志::weapp
#		"""
#		[{
#			"content": "取消订单 返还积分",
#			"integral": 21
#		}, {
#			"content": "购物抵扣",
#			"integral": -21
#		}, {
#			"content": "首次关注",
#			"integral": 50
#		}]
#		"""
	Then zhouxun能获得bill的积分日志::weapp
		"""
		[{
			"content": "取消订单 返还积分",
			"integral": 21
		}, {
			"content": "购物抵扣",
			"integral": -21
		}]
		"""

@order
Scenario: 2 管理员退款使用订单积分的订单

	Given zhouxun登录系统
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
	When bill访问zhouxun的webapp::apiserver
	When bill获得zhouxun的50会员积分::apiserver
	Then bill在zhouxun的webapp中拥有50会员积分::apiserver
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
				"count":1
			}],
			"integral": 31,
			"integral_money": 15.05,
			"postage": 0.00
		}
		"""
	When bill使用支付方式'微信支付'进行支付订单'005'于2016-05-01 10:00:00::apiserver
	Then bill在zhouxun的webapp中拥有19会员积分::apiserver
	Given zhouxun登录系统
	When zhouxun申请退款出货单'005-zhouxun'
		"""
		{
			"cash":10.00,
			"weizoom_card_money":0.00,
			"coupon_money":10.11,
			"integral":20,
			"member_card_money":0.00,
			"time": "2016-05-02 10:00:00"
		}
		"""
	Then zhouxun获得订单列表
		"""
		[{
			"bid": "005",
			"status_code": "refunding",
			"pay_interface_type_code": "weixin_pay",
			"pay_money": 15.06,
			"product_price": 30.11,
			"save_money": 15.05,
			"origin_final_price": 15.06,
			"origin_weizoom_card_money": 0.00,
			"origin_member_card_money": 0.00,
			"final_price": 15.06,
			"weizoom_card_money": 0.00,
			"member_card_money": 0.00,
			"integral": 31,
			"integral_money": 15.05,
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
				"bid": "005-zhouxun",
				"status_code": "refunding",
				"refunding_info": {
					"finished": false,
					"total_can_refund": 30.11,
					"cash": 10.00,
					"weizoom_card_money": 0.00,
					"member_card_money":0.00,
					"coupon_money": 10.11,
					"integral": 20,
					"integral_money": 10.00,
					"total": 30.11
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
					"count": 1
				}]
			}]
		}]
		"""

	Then zhouxun获得订单'005'
		"""
		{
			"bid": "005",
			"status_code": "refunding",
			"pay_interface_type_code": "weixin_pay",
			"pay_money": 15.06,
			"product_price": 30.11,
			"save_money": 15.05,
			"origin_final_price": 15.06,
			"origin_weizoom_card_money": 0.00,
			"final_price": 15.06,
			"weizoom_card_money": 0.00,
			"integral": 31,
			"integral_money": 15.05,
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
				"bid": "005-zhouxun",
				"status_code": "refunding",
				"refunding_info": {
					"finished": false,
					"cash": 10.00,
					"weizoom_card_money": 0.00,
					"member_card_money":0.00,
					"coupon_money": 10.11,
					"integral": 20,
					"integral_money": 10.00,
					"total": 30.11
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
					"count": 1
				}]
			}]
		}
		"""
	When bill访问zhouxun的webapp::apiserver
	Then bill在zhouxun的webapp中拥有19会员积分::apiserver

@order
Scenario: 3 管理员退款成功使用订单积分的订单

	Given zhouxun登录系统
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


	When bill访问zhouxun的webapp::apiserver
	When bill获得zhouxun的50会员积分::apiserver
	Then bill在zhouxun的webapp中拥有50会员积分::apiserver
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
				"count":1
			}],
			"integral": 31,
			"integral_money": 15.05,
			"postage": 0.00
		}
		"""
	When bill使用支付方式'微信支付'进行支付订单'005'于2016-05-01 10:00:00::apiserver
	Then bill在zhouxun的webapp中拥有19会员积分::apiserver
	Given zhouxun登录系统
	When zhouxun申请退款出货单'005-zhouxun'
		"""
		{
			"cash":10.00,
			"weizoom_card_money":0.00,
			"coupon_money":10.11,
			"integral":20,
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
	Then zhouxun获得订单列表
		"""
		[{
			"bid": "005",
			"status_code": "refunded",
			"pay_interface_type_code": "weixin_pay",
			"pay_money": 5.06,
			"product_price": 30.11,
			"save_money": 15.05,
			"origin_final_price": 15.06,
			"origin_weizoom_card_money": 0.00,
			"origin_member_card_money": 0.00,
			"final_price": 5.06,
			"weizoom_card_money": 0.00,
			"member_card_money": 0.00,
			"integral": 31,
			"integral_money": 15.05
			"refunding_info": {
				"cash": 10.00,
				"weizoom_card_money": 0.00,
				"member_card_money": 0.00,
				"coupon_money": 10.11,
				"integral": 20,
				"integral_money": 10.00,
				"total": 30.11
			},
			"delivery_items": [{
				"bid": "005-zhouxun",
				"status_code": "refunded",
				"refunding_info": {
					"finished": true,
					"total_can_refund": 30.11,
					"cash": 10.00,
					"weizoom_card_money": 0.00,
					"member_card_money":0.00,
					"coupon_money": 10.11,
					"integral": 20,
					"integral_money": 10.00,
					"total": 30.11
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
					"count": 1
				}]
			}]
		}]
		"""

	Then zhouxun获得订单'005'
		"""
		{
			"bid": "005",
			"status_code": "refunded",
			"pay_interface_type_code": "weixin_pay",
			"pay_money": 5.06,
			"product_price": 30.11,
			"save_money": 15.05,
			"origin_final_price": 15.06,
			"origin_weizoom_card_money": 0.00,
			"final_price": 5.06,
			"weizoom_card_money": 0.00,
			"integral": 31,
			"integral_money": 15.05,
			"weizoom_card_info": {
				"used_card": []
			},
			"refunding_info": {
				"cash": 10.00,
				"weizoom_card_money": 0.00,
				"member_card_money": 0.00,
				"coupon_money": 10.11,
				"integral": 20,
				"integral_money": 10.00,
				"total": 30.11
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
					"coupon_money": 10.11,
					"integral": 20,
					"integral_money": 10.00,
					"total": 30.11
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
					"count": 1
				}]
			}]
		}
		"""
	When bill访问zhouxun的webapp::apiserver
	Then bill在zhouxun的webapp中拥有100会员积分::apiserver