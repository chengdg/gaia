# __author__ : "冯雪静"

Feature: 管理员在weapp中取消订单
"""

"""
Background:
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
		}, {
			"name": "尺寸",
			"type": "文字",
			"values": [{
				"name": "M"
			}, {
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
			"name": "zhouxun商品1",
			"model": {
				"models": {
					"standard": {
						"price": 19.00,
						"stock_type": "无限"
					}
				}
			}
		},{
			"name": "zhouxun商品2",
			"model": {
				"models": {
					"黑色 M": {
						"price": 10.00,
						"stock_type": "有限",
						"stocks": 10
					},
					"白色 S": {
						"price": 20.00,
						"stock_type": "有限",
						"stocks": 20
					}
				}
			}
		},{
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
		["zhouxun商品3", "zhouxun商品2", "zhouxun商品1", "jobs商品1"]
		"""
	Given bill关注zhouxun的公众号::apiserver


Scenario: 1 管理员取消多规格商品的订单
	1.zhouxun取消待支付订单，多规格商品的库存退回

	When bill访问zhouxun的webapp::apiserver
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
			"products": [{
				"name": "zhouxun商品2",
				"model":"黑色 M",
				"count": 1
			}, {
				"name": "zhouxun商品2",
				"model":"白色 S",
				"count": 1
			}]
		}
		"""
	Given zhouxun登录系统
	Then zhouxun能获取商品'zhouxun商品2'
		"""
		{
			"name": "zhouxun商品2",
			"model": {
				"models": {
					"黑色 M": {
						"price": 10.1,
						"stock_type": "有限",
						"stocks": 9
					},
					"白色 S": {
						"price": 20.2,
						"stock_type": "有限",
						"stocks": 19
					}
				}
			}
		}
		"""
	When zhouxun取消订单'001'
		"""
		{
			"time":"2017-01-20 10:10:00"
		}
		"""
	Then zhouxun能获取商品'zhouxun商品2'
		"""
		{
			"name": "zhouxun商品2",
			"model": {
				"models": {
					"黑色 M": {
						"price": 10.1,
						"stock_type": "有限",
						"stocks": 10
					},
					"白色 S": {
						"price": 20.2,
						"stock_type": "有限",
						"stocks": 20
					}
				}
			}
		}
		"""
	Then zhouxun获得订单列表
		"""
		[{
			"bid": "001",
			"status_code": "cancelled",
			"created_at": "2017-01-20 10:00:00",
			"delivery_items": [{
				"bid": "001-zhouxun",
				"status_code": "cancelled",
				"created_at": "2017-01-20 10:00:00"
			}]
		}]
		"""
	Then zhouxun获得订单'001'
		"""
		{
			"bid": "001",
			"status_code": "cancelled",
			"status_logs": [{
				"from_status_code":"",
				"to_status_code":"created",
				"time":"2017-01-20 10:00:00"
			},{
				"from_status_code":"created",
				"to_status_code":"cancelled",
				"time":"2017-01-20 10:10:00"
			}],
			"operation_logs": [{
				"action_text":"下单",
				"operator":"客户",
				"time":"2017-01-20 10:00:00"
			},{
				"action_text":"取消订单",
				"operator":"zhouxun",
				"time":"2017-01-20 10:10:00"
			}],
			"delivery_items": [{
				"bid": "001-zhouxun",
				"status_code": "cancelled",
				"operation_logs": [{
					"action_text":"下单",
					"operator":"客户",
					"time":"2017-01-20 10:00:00"
				},{
					"action_text":"取消订单",
					"operator":"zhouxun",
					"time":"2017-01-20 10:10:00"
				}]
			}]
		}
		"""


Scenario: 2 管理员取消多个供货商商品的订单
	1.zhouxun取消待支付订单，供货商的商品库存退回

	When bill访问zhouxun的webapp::apiserver
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
			"products": [{
				"name": "zhouxun商品3",
				"count": 1
			}, {
				"name": "jobs商品1",
				"count": 1
			}]
		}
		"""
	Given zhouxun登录系统
	When zhouxun取消订单'001'
		"""
		{
			"time":"2017-01-20 10:10:00"
		}
		"""
	Then zhouxun能获取商品'zhouxun商品3'
		"""
		{
			"name": "zhouxun商品3",
			"model": {
				"models": {
					"standard": {
						"price": 30.1,
						"stock_type": "有限",
						"stocks": 30
					}
				}
			}
		}
		"""
	Then zhouxun能获取商品'jobs商品1'
		"""
		{
			"name": "jobs商品1",
			"model": {
				"models": {
					"standard": {
						"price": 11.1,
						"stock_type": "有限",
						"stocks": 30
					}
				}
			}
		}
		"""
	Then zhouxun获得订单列表
		"""
		[{
			"bid": "001",
			"status_code": "cancelled",
			"created_at": "2017-01-20 10:00:00",
			"delivery_items": [{
				"bid": "001-zhouxun",
				"status_code": "cancelled",
				"created_at": "2017-01-20 10:00:00"
			},{
				"bid": "001-jobs",
				"status_code": "cancelled",
				"created_at": "2017-01-20 10:00:00"
			}]
		}]
		"""
	Then zhouxun获得订单'001'
		"""
		{
			"bid": "001",
			"status_code": "cancelled",
			"status_logs": [{
				"from_status_code":"",
				"to_status_code":"created",
				"time":"2017-01-20 10:00:00"
			},{
				"from_status_code":"created",
				"to_status_code":"cancelled",
				"time":"2017-01-20 10:10:00"
			}],
			"operation_logs": [{
				"action_text":"下单",
				"operator":"客户",
				"time":"2017-01-20 10:00:00"
			},{
				"action_text":"取消订单",
				"operator":"zhouxun",
				"time":"2017-01-20 10:10:00"
			}],
			"delivery_items": [{
				"bid": "001-zhouxun",
				"status_code": "cancelled",
				"operation_logs": [{
					"action_text":"下单",
					"operator":"客户",
					"time":"2017-01-20 10:00:00"
				},{
					"action_text":"取消订单",
					"operator":"zhouxun",
					"time":"2017-01-20 10:10:00"
				}],
				"bid": "001-jobs",
				"status_code": "cancelled",
				"operation_logs": [{
					"action_text":"下单",
					"operator":"客户",
					"time":"2017-01-20 10:00:00"
				},{
					"action_text":"取消订单",
					"operator":"zhouxun",
					"time":"2017-01-20 10:10:00"
				}]
			}]
		}
		"""


Scenario: 3 管理员取消使用了订单积分的订单
	1.zhouxun取消待支付订单，积分退回

	Given zhouxun登录系统
	And zhouxun设定会员积分策略
		"""
		{
			"integral_each_yuan": 2,
			"use_ceiling": 50
		}
		"""
	When bill访问zhouxun的webapp::weapp
	When bill获得zhouxun的50会员积分::weapp
	Then bill在zhouxun的webapp中拥有50会员积分::weapp
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
	Then bill在zhouxun的webapp中拥有29会员积分::weapp
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
	When bill获得zhouxun的50会员积分::weapp
	Then bill在zhouxun的webapp中拥有50会员积分::weapp
	Then zhouxun能获得bill的积分日志::weapp
		"""
		[{
			"content": "取消订单 返还积分",
			"integral": 21
		}, {
			"content": "购物抵扣",
			"integral": 21
		}, {
			"content": "首次关注",
			"integral": 50
		}]
		"""


Scenario: 4 管理员取消使用了商品积分的订单
	1.zhouxun取消待支付订单，积分退回

	Given zhouxun登录系统
	And zhouxun设定会员积分策略
		"""
		{
			"integral_each_yuan": 2
		}
		"""
	When jobs创建积分应用活动::weapp
		"""
		[{
			"name": "多商品积分应用1",
			"start_date": "今天",
			"end_date": "1天后",
			"product_name": "jobs商品1,zhouxun商品3",
			"is_permanant_active": false,
			"rules": [{
				"member_grade": "全部",
				"discount": 80,
				"discount_money": 5.00
			}]
		}]
		"""