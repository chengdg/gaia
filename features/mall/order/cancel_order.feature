# __author__ : "冯雪静"

Feature: 管理员在weapp中取消订单
	"""
	管理员取消待支付订单
		1.管理员取消多规格商品的订单，多规格商品库存退回正确
		2.管理员取消多供货商商品的订单，商品库存退回正确
		3.管理员取消使用订单积分的订单，积分退回正确
		4.管理员取消使用通用券的订单，通用券退回正确
		5.管理员取消使用多商品券的订单，多商品券退回正确
		6.管理员取消使用微众卡的订单，微众卡退回正确
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
	When zhouxun更新积分规则为
		"""
		{
			"integral_each_yuan": 2,
			"be_member_increase_count": 50
		}
		"""
	Given zhouxun已添加商品规格
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

@gaiax @order
Scenario: 1 管理员取消多规格商品的订单
	1.zhouxun取消待支付订单，多规格商品的库存退回

	When bill访问zhouxun的webapp::apiserver
	When bill购买zhouxun的商品::apiserver
		"""
		{
			"order_id":"001",
			"date":"2017-01-20 00:00:00",
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
						"price": 10.00,
						"stock_type": "有限",
						"stocks": 9
					},
					"白色 S": {
						"price": 20.00,
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
		}
		"""
	Then zhouxun获得订单列表
		"""
		[{
			"bid": "001",
			"status_code": "cancelled",
			"created_at": "2017-01-20 00:00:00",
			"delivery_items": [{
				"bid": "001-zhouxun",
				"status_code": "cancelled",
				"created_at": "2017-01-20 00:00:00"
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
				"time":"2017-01-20 00:00:00"
			},{
				"from_status_code":"created",
				"to_status_code":"cancelled",
				"time":"2017-01-20 10:10:00"
			}],
			"operation_logs": [{
				"action_text":"下单",
				"operator":"客户",
				"time":"2017-01-20 00:00:00"
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

@gaiax @order
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
						"price": 10.01,
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
						"price": 11.00,
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
			"created_at": "2017-01-20 00:00:00",
			"delivery_items": [{
				"bid": "001-zhouxun",
				"status_code": "cancelled",
				"created_at": "2017-01-20 00:00:00"
			},{
				"bid": "001-jobs",
				"status_code": "cancelled",
				"created_at": "2017-01-20 00:00:00"
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
				"time":"2017-01-20 00:00:00"
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
			"delivery_items":
			[{
				"bid": "001-zhouxun",
				"status_code": "cancelled",
				"operation_logs": [{
					"action_text": "下单",
					"operator": "客户",
					"time": "2017-01-20 00:00:00"
				}, {
					"action_text": "取消订单",
					"operator": "zhouxun",
					"time": "2017-01-20 10:10:00"
				}]},
				{
					"bid": "001-jobs",
					"status_code": "cancelled",
					"operation_logs": [{
						"action_text": "下单",
						"operator": "客户",
						"time": "2017-01-20 00:00:00"
					}, {
						"action_text": "取消订单",
						"operator": "zhouxun",
						"time": "2017-01-20 10:10:00"
					}]}
			]
		}
		"""

@gaiax @order
Scenario: 3 管理员取消使用了微众卡的订单
	1.zhouxun取消待支付订单，微众卡退回


	Given 重置'weizoom_card'的bdd环境
	Given zhouxun登录系统::weapp
	When zhouxun开通使用微众卡权限::weapp
	When zhouxun添加支付方式::weapp
		"""
		[{
			"type": "微众卡支付",
			"is_active": "启用"
		}]
		"""
	Given test登录管理系统::weizoom_card
	When test新建通用卡::weizoom_card
		"""
		[{
			"name":"10元微众卡",
			"prefix_value":"100",
			"type":"virtual",
			"money":"10.00",
			"num":"1",
			"comments":"微众卡"
		}]
		"""
	When test下订单::weizoom_card
			"""
			[{
				"card_info":[{
					"name":"10元微众卡",
					"order_num":"1",
					"start_date":"2016-04-07 00:00",
					"end_date":"2019-10-07 00:00"
				}],
				"order_info":{
					"order_id":"0001"
				}
			}]
			"""
	And test批量激活订单'0001'的卡::weizoom_card
	When bill访问zhouxun的webapp::apiserver
	When bill绑定微众卡::apiserver
		"""
		{
			"binding_date":"2017-01-01",
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
				"name": "zhouxun商品1",
				"count": 1
			}, {
				"name": "jobs商品1",
				"count": 1
			}],
			"weizoom_card":[{
				"card_name":"100000001",
				"card_pass":"1234567"
			}]
		}
		"""
	Then bill能获得微众卡'100000001'的详情信息::apiserver
		"""
		{
			"card_remain_value": 0.00
		}
		"""
	When zhouxun取消订单'001'
	Then zhouxun获得订单列表
		"""
		[{
			"bid": "001",
			"status_code": "cancelled",
			"origin_weizoom_card_money": 10.00,
			"weizoom_card_money": 10.00,
			"delivery_items":[
			{
				"bid": "001-zhouxun",
				"status_code": "cancelled"
			},{
				"bid": "001-jobs",
				"status_code": "cancelled"
			}]
		}]
		"""
	Then zhouxun获得订单'001'
		"""
		{
			"bid": "001",
			"status_code": "cancelled",
			"origin_weizoom_card_money": 10.00,
			"weizoom_card_money": 10.00,
			"weizoom_card_info": {
				"used_card": ["100000001"]
			},
			"delivery_items": [{
				"bid": "001-zhouxun",
				"status_code": "cancelled"
			},{
				"bid": "001-jobs",
				"status_code": "cancelled"
			}]
		}
		"""
	When bill访问zhouxun的webapp::apiserver
	Then bill能获得微众卡'100000001'的详情信息::apiserver
		"""
		{
			"card_remain_value": 10.00
		}
		"""
