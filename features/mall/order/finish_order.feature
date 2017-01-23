# __author__ : "冯雪静"

Feature: 管理员在weapp中标记完成订单
	"""

	"""

Background:
	Given 重置'weapp'的bdd环境
	Given 重置'apiserver'的bdd环境
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
	And jobs设定会员积分策略
		"""
		{
			"be_member_increase_count": 20
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


Scenario: 1 管理员标记完成一个供货商的订单
	1.zhouxun完成一个供货商的订单，查看会员列表

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
	When bill使用支付方式'微信支付'进行支付订单'001'于2017-01-20 10:10:00::apiserver
	Given zhouxun登录系统
	When zhouxun对出货单进行发货
		"""
		[{
			"delivery_item_bid":"001-zhouxun",
			"time":"2017-01-20 10:10:10"
		}]
		"""
	When zhouxun标记完成出货单'001-zhouxun'
		"""
		{
			"time":"2017-01-20 11:10:10"
		}
		"""
	Then zhouxun获得订单列表
		"""
		[{
			"bid": "001",
			"status_code": "finished",
			"created_at": "2017-01-20 10:00:00",
			"payment_time": "2017-01-20 10:10:00",
			"delivery_items": [{
				"bid": "001-zhouxun",
				"status_code": "finished",
				"created_at": "2017-01-20 10:00:00"
			}]
		}]
		"""
	Then zhouxun获得订单'001'
		"""
		{
			"bid": "001",
			"status_code": "finished",
			"status_logs": [{
				"from_status_code":"",
				"to_status_code":"created",
				"time":"2017-01-20 10:00:00"
			},{
				"from_status_code":"created",
				"to_status_code":"paid",
				"time":"2017-01-20 10:10:00"
			},{
				"from_status_code":"paid",
				"to_status_code":"shipped",
				"time":"2017-01-20 10:10:10"
			},{
				"from_status_code":"shipped",
				"to_status_code":"finished",
				"time":"2017-01-20 11:10:10"
			}],
			"operation_logs": [{
				"action_text":"下单",
				"operator":"客户",
				"time":"2017-01-20 10:00:00"
			},{
				"action_text":"支付",
				"operator":"客户",
				"time":"2017-01-20 10:10:00"
			},{
				"action_text":"订单发货-zhouxun",
				"operator":"zhouxun",
				"time":"2017-01-20 10:10:10"
			},{
				"action_text":"完成-zhouxun",
				"operator":"zhouxun",
				"time":"2017-01-20 11:10:10"
			}],
			"delivery_items": [{
				"bid": "001-zhouxun",
				"status_code": "finished",
				"operation_logs": [{
					"action_text":"下单",
					"operator":"客户",
					"time":"2017-01-20 10:00:00"
				},{
					"action_text":"支付",
					"operator":"客户",
					"time":"2017-01-20 10:10:00"
				},{
					"action_text":"订单发货-zhouxun",
					"operator":"zhouxun",
					"time":"2017-01-20 10:10:10"
				},{
					"action_text":"完成-zhouxun",
					"operator":"zhouxun",
					"time":"2017-01-20 11:10:10"
				}]
			}]
		}
		"""
	Then zhouxun可以获得会员列表
		"""
		[{
			"name": "bill",
			"pay_money": 30.00,
			"unit_price": 30.00,
			"pay_times": 1
		}]
		"""


Scenario: 2 管理员标记完成多个供货商的订单
	1.zhouxun完成多个供货商的1个出货单，查看会员列表(消费总额-客单价-购买次数 不变)
	2.zhouxun完成多个供货商的订单，查看会员列表(消费总额-客单价-购买次数 增加)

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
	When bill使用支付方式'微信支付'进行支付订单'001'于2017-01-20 10:10:00::apiserver
	Given zhouxun登录系统
	When zhouxun对出货单进行发货
		"""
		[{
			"delivery_item_bid":"001-zhouxun",
			"time":"2017-01-20 10:10:10"
		}, {
			"delivery_item_bid":"001-jobs",
			"time":"2017-01-20 10:10:10"
		}]
		"""
	When zhouxun标记完成出货单'001-zhouxun'
		"""
		{
			"time":"2017-01-20 11:10:10"
		}
		"""
	Then zhouxun获得订单列表
		"""
		[{
			"bid": "001",
			"status_code": "shipped",
			"created_at": "2017-01-20 10:00:00",
			"payment_time": "2017-01-20 10:10:00",
			"delivery_items": [{
				"bid": "001-zhouxun",
				"status_code": "finished",
				"created_at": "2017-01-20 10:00:00"
			},{
				"bid": "001-jobs",
				"status_code": "shipped",
				"created_at": "2017-01-20 10:00:00"
			}]
		}]
		"""
	Then zhouxun获得订单'001'
		"""
		{
			"bid": "001",
			"status_code": "shipped",
			"status_logs": [{
				"from_status_code":"",
				"to_status_code":"created",
				"time":"2017-01-20 10:00:00"
			},{
				"from_status_code":"created",
				"to_status_code":"paid",
				"time":"2017-01-20 10:10:00"
			},{
				"from_status_code":"paid",
				"to_status_code":"shipped",
				"time":"2017-01-20 10:10:10"
			}],
			"delivery_items": [{
				"bid": "001-zhouxun",
				"status_code": "finished",
				"operation_logs": [{
					"action_text":"下单",
					"operator":"客户",
					"time":"2017-01-20 10:00:00"
				},{
					"action_text":"支付",
					"operator":"客户",
					"time":"2017-01-20 10:10:00"
				},{
					"action_text":"订单发货-zhouxun",
					"operator":"zhouxun",
					"time":"2017-01-20 10:10:10"
				},{
					"action_text":"完成-zhouxun",
					"operator":"zhouxun",
					"time":"2017-01-20 11:10:10"
				}],
				"bid": "001-jobs",
				"status_code": "shipped",
				"operation_logs": [{
					"action_text":"下单",
					"operator":"客户",
					"time":"2017-01-20 10:00:00"
				},{
					"action_text":"支付",
					"operator":"客户",
					"time":"2017-01-20 10:10:00"
				},{
					"action_text":"订单发货-jobs",
					"operator":"zhouxun",
					"time":"2017-01-20 10:10:10"
				}]
			}]
		}
		"""
	Then zhouxun可以获得会员列表
		"""
		[{
			"name": "bill",
			"pay_money": 0.00,
			"unit_price": 0.00,
			"pay_times": 0
		}]
		"""
	When zhouxun标记完成出货单'001-jobs'
		"""
		{
			"time":"2017-01-20 11:11:10"
		}
		"""
	Then zhouxun获得订单列表
		"""
		[{
			"bid": "001",
			"status_code": "finished",
			"created_at": "2017-01-20 10:00:00",
			"payment_time": "2017-01-20 10:10:00",
			"delivery_items": [{
				"bid": "001-zhouxun",
				"status_code": "finished",
				"created_at": "2017-01-20 10:00:00"
			},{
				"bid": "001-jobs",
				"status_code": "finished",
				"created_at": "2017-01-20 10:00:00"
			}]
		}]
		"""
	Then zhouxun获得订单'001'
		"""
		{
			"bid": "001",
			"status_code": "finished",
			"status_logs": [{
				"from_status_code":"",
				"to_status_code":"created",
				"time":"2017-01-20 10:00:00"
			},{
				"from_status_code":"created",
				"to_status_code":"paid",
				"time":"2017-01-20 10:10:00"
			},{
				"from_status_code":"paid",
				"to_status_code":"shipped",
				"time":"2017-01-20 10:10:10"
			},{
				"from_status_code":"shipped",
				"to_status_code":"finished",
				"time":"2017-01-20 11:11:10"
			}],
			"delivery_items": [{
				"bid": "001-zhouxun",
				"status_code": "finished",
				"operation_logs": [{
					"action_text":"下单",
					"operator":"客户",
					"time":"2017-01-20 10:00:00"
				},{
					"action_text":"支付",
					"operator":"客户",
					"time":"2017-01-20 10:10:00"
				},{
					"action_text":"订单发货-zhouxun",
					"operator":"zhouxun",
					"time":"2017-01-20 10:10:10"
				},{
					"action_text":"完成-zhouxun",
					"operator":"zhouxun",
					"time":"2017-01-20 11:10:10"
				}],
				"bid": "001-jobs",
				"status_code": "shipped",
				"operation_logs": [{
					"action_text":"下单",
					"operator":"客户",
					"time":"2017-01-20 10:00:00"
				},{
					"action_text":"支付",
					"operator":"客户",
					"time":"2017-01-20 10:10:00"
				},{
					"action_text":"订单发货-jobs",
					"operator":"zhouxun",
					"time":"2017-01-20 10:10:10"
				},{
					"action_text":"完成-jobs",
					"operator":"zhouxun",
					"time":"2017-01-20 11:11:10"
				}]
			}]
		}
		"""
	Then zhouxun可以获得会员列表
		"""
		[{
			"name": "bill",
			"pay_money": 21.01,
			"unit_price": 21.01,
			"pay_times": 1
		}]
		"""


Scenario: 3 管理员标记完成订单，会员获得购物返积分
	1.zhouxun完成多个供货商的1个出货单，查看会员积分(不变)
	2.zhouxun完成多个供货商的订单，查看会员积分(增加)

	Given zhouxun登录系统
	And jobs设定会员积分策略
		"""
		{

			"buy_award_count_for_buyer":21,
			"order_money_percentage_for_each_buy":0.5,
		}
		"""
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
	When bill使用支付方式'微信支付'进行支付订单'001'于2017-01-20 10:10:00::apiserver
	Given zhouxun登录系统
	When zhouxun对出货单进行发货
		"""
		[{
			"delivery_item_bid":"001-zhouxun",
			"time":"2017-01-20 10:10:10"
		}, {
			"delivery_item_bid":"001-jobs",
			"time":"2017-01-20 10:10:10"
		}]
		"""
	When zhouxun标记完成出货单'001-zhouxun'
		"""
		{
			"time":"2017-01-20 11:10:10"
		}
		"""
	Then zhouxun能获得bill的积分日志::weapp
		"""
		[{
			"content": "首次关注",
			"integral": 20
		}]
		"""



