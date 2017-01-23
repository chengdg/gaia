# __author__ : "冯雪静"

Feature: 管理员在weapp中标记完成订单
	"""
	管理员标记完成已发货订单
		1.管理员完成一个供货商的订单，查看列表、详情和会员列表(母订单状态已完成会员购买数据增加)
		2.管理员完成多个供货商的订单，查看列表、详情和会员列表(母订单状态已完成会员购买数据增加)
		3.管理员完成多个供货商的订单，查看会员积分日志(母订单状态已完成会员积分增加)
		4.管理员完成多个供货商使用微众卡的订单，查看会员详情和积分日志(购买返积分额外奖励的金额(金额不包含微众卡只计算现金)*比例)
		5.管理员完成多个供货商的订单，满足一个会员等级升级条件，会员等级自动升级
		6.管理员完成多个供货商的订单，必须满足全部条件会员等级升级条件，会员等级自动升级
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
	#1.关注公众账号
	#2.购买商品返积分
	#3.购买商品返积分额外积分奖励
	When zhouxun更新积分规则为
		"""
		{
			"be_member_increase_count": 20,
			"buy_award_count_for_buyer":21,
			"order_money_percentage_for_each_buy":0.5
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

@order
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
	Then zhouxun可以获得会员列表::weapp
		"""
		[{
			"name": "bill",
			"pay_money": 30.00,
			"unit_price": 30.00,
			"pay_times": 1
		}]
		"""

@order
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
	Then zhouxun可以获得会员列表::weapp
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
	Then zhouxun可以获得会员列表::weapp
		"""
		[{
			"name": "bill",
			"pay_money": 21.01,
			"unit_price": 21.01,
			"pay_times": 1
		}]
		"""

@order
Scenario: 3 管理员标记完成订单，会员获得购物返积分
	1.zhouxun完成多个供货商的1个出货单，查看会员积分(不变)
	2.zhouxun完成多个供货商的订单，查看会员积分(增加)

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
	When zhouxun标记完成出货单'001-jobs'
		"""
		{
			"time":"2017-01-20 11:11:10"
		}
		"""
	Then zhouxun能获得bill的积分日志::weapp
		"""
		[{
			"content":"购物返利",
			"integral":10
		},{
			"content":"购物返利",
			"integral":21
		},{
			"content": "首次关注",
			"integral": 20
		}]
		"""

@order
Scenario: 4 管理员标记完成使用微众卡的订单
	1.zhouxun完成使用微众卡多个供货商的订单，查看会员详情
	查看会员积分(增加，但是购买商品返积分额外积分奖励-金额计算不包含微众卡的金额)

	Given 重置'weizoom_card'的bdd环境
	Given zhouxun登录系统
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
			"prefix_value":"10",
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
					"id":"000000001",
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
				"name": "jobs商品1",
				"count": 1
			}],
			"weizoom_card":[{
				"card_name":"000000001",
				"card_pass":"1234567"
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
	When zhouxun访问'bill'会员详情::weapp
	Then zhouxun获得'bill'的购买信息::weapp
		"""
		{
			"purchase_amount":0.00,
			"purchase_number":0,
			"customer_price":0.00,
			"money_wcard":0.00
		}
		"""
	When zhouxun标记完成出货单'001-jobs'
		"""
		{
			"time":"2017-01-20 11:11:10"
		}
		"""
	When zhouxun访问'bill'会员详情::weapp
	Then zhouxun获得'bill'的购买信息::weapp
		"""
		{
			"purchase_amount":21.01,
			"purchase_number":1,
			"customer_price":21.01,
			"money_wcard":10.00
		}
		"""
	#购买返积分额外奖励的金额(金额不包含微众卡只计算现金)*比例
	Then zhouxun能获得bill的积分日志::weapp
		"""
		[{
			"content":"购物返利",
			"integral":5
		},{
			"content":"购物返利",
			"integral":21
		},{
			"content": "首次关注",
			"integral": 20
		}]
		"""

@order
Scenario: 5 管理员标记完成订单，满足一个条件会员等级自动升级
	1.zhouxun完成使用微众卡多个供货商的订单，查看会员等级

	Given zhouxun登录系统
	When zhouxun开启自动升级::weapp
		"""
		{
			"upgrade": "自动升级",
			"condition": ["满足一个条件即可"]
		}
		"""
	When zhouxun添加会员等级::weapp
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "自动升级",
			"pay_money": 10.00,
			"pay_times": 2,
			"discount": "9"
		}]
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
	Then zhouxun可以获得会员列表::weapp
		"""
		[{
			"name": "bill",
			"member_rank": "普通会员"
		}]
		"""
	When zhouxun标记完成出货单'001-jobs'
		"""
		{
			"time":"2017-01-20 11:11:10"
		}
		"""
	Then zhouxun可以获得会员列表::weapp
		"""
		[{
			"name": "bill",
			"member_rank": "铜牌会员"
		}]
		"""

@order
Scenario: 6 管理员标记完成订单，必须满足全部条件会员等级自动升级
	1.zhouxun完成使用微众卡多个供货商的订单，查看会员等级

	Given zhouxun登录系统
	When zhouxun开启自动升级::weapp
		"""
		{
			"upgrade": "自动升级",
			"condition": ["必须满足全部条件"]
		}
		"""
	When zhouxun添加会员等级::weapp
		"""
		[{
			"name": "铜牌会员",
			"upgrade": "自动升级",
			"pay_money": 10.00,
			"pay_times": 2,
			"discount": "9"
		}]
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
	When zhouxun标记完成出货单'001-jobs'
		"""
		{
			"time":"2017-01-20 11:11:10"
		}
		"""
	Then zhouxun可以获得会员列表::weapp
		"""
		[{
			"name": "bill",
			"member_rank": "普通会员"
		}]
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
	Then zhouxun可以获得会员列表::weapp
		"""
		[{
			"name": "bill",
			"member_rank": "铜牌会员"
		}]
		"""






