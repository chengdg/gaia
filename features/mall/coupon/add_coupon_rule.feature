#author: 冯雪静
#editor: 张三香 2015.10.15
#editor: 王丽 2016.04.15

Feature: 添加优惠券规则
	Jobs能通过管理系统添加"优惠券规则"

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 200.00
		},{
			"name": "商品2",
			"price": 200.00
		},{
			"name": "商品3",
			"price": 200.00
		}]
		"""

@gaia @promotion @coupon @wip
Scenario:1 添加优惠券规则-添加通用券
	添加优惠券规则后：
	1. 能获得优惠券规则详情
	2. 能获得正确的优惠券规则列表
	添加两个规则，分别覆盖不同的using limit场景

	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "全店通用券1",
			"money": 100.00,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"count": 5,
			"start_date": "2017-01-01 11:00",
			"end_date": "2017-01-02 12:00",
			"description":"全店通用券1使用说明",
			"note": "全店通用券1的备注",
			"is_no_order_user_only": true,
			"coupon_id_prefix": "coupon1_id_"
		}, {
			"name": "全店通用券2",
			"money": 200.00,
			"limit_counts": 2,
			"count": 10,
			"start_date": "2017-02-01 12:00",
			"end_date": "2017-02-02 13:11",
			"description":"全店通用券2使用说明",
			"note": "全店通用券2的备注",
			"coupon_id_prefix": "coupon2_id_"
		}, {
			"name": "全店通用券3",
			"start_date": "昨天",
			"end_date": "1天后"
		}]
		"""
	Then jobs获得优惠券规则'全店通用券1'
		"""
		{
			"name": "全店通用券1",
			"status": "expired",
			"money": 100.00,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"count": 5,
			"remained_count": 5,
			"use_count": 0,
			"receive_count": 0,
			"receive_user_count": 0,
			"start_date": "2017-01-01 11:00",
			"end_date": "2017-01-02 12:00",
			"description":"全店通用券1使用说明",
			"note": "全店通用券1的备注",
			"is_no_order_user_only": true,
			"is_for_specific_products": false
		}
		"""
	Then jobs获得优惠券规则'全店通用券2'
		"""
		{
			"name": "全店通用券2",
			"status": "expired",
			"money": 200.00,
			"limit_counts": 2,
			"using_limit": "无限制",
			"count": 10,
			"remained_count": 10,
			"use_count": 0,
			"receive_count": 0,
			"receive_user_count": 0,
			"start_date": "2017-02-01 12:00",
			"end_date": "2017-02-02 13:11",
			"description":"全店通用券2使用说明",
			"note": "全店通用券2的备注",
			"is_no_order_user_only": false,
			"is_for_specific_products": false
		}
		"""
	Then jobs获得优惠券规则'全店通用券3'
		"""
		{
			"name": "全店通用券3",
			"status": "active"
		}
		"""
	Then jobs能获得优惠券规则列表
		"""
		[{
			"name": "全店通用券3",
			"status": "active"
		}, {
			"name": "全店通用券2",
			"status": "expired",
			"money": 200.00,
			"limit_counts": 2,
			"using_limit": "无限制",
			"count": 10,
			"remained_count": 10,
			"use_count": 0,
			"receive_count": 0,
			"receive_user_count": 0,
			"start_date": "2017-02-01 12:00",
			"end_date": "2017-02-02 13:11",
			"description":"全店通用券2使用说明",
			"note": "全店通用券2的备注",
			"is_no_order_user_only": false,
			"is_for_specific_products": false
		}, {
			"name": "全店通用券1",
			"status": "expired",
			"money": 100.00,
			"limit_counts": 1,
			"using_limit": "满50元可以使用",
			"count": 5,
			"remained_count": 5,
			"use_count": 0,
			"receive_count": 0,
			"receive_user_count": 0,
			"start_date": "2017-01-01 11:00",
			"end_date": "2017-01-02 12:00",
			"description":"全店通用券1使用说明",
			"note": "全店通用券1的备注",
			"is_no_order_user_only": true,
			"is_for_specific_products": false
		}]
		"""

@gaia @promotion @coupon
Scenario:2 添加优惠券规则-多商品券
	只覆盖商品的信息，其他信息在上面的scenario中已测试

	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "多商品券1",
			"coupon_product": "商品1"
		}, {
			"name": "多商品券2",
			"coupon_product": "商品2,商品3"
		}]
		"""
	Then jobs获得优惠券规则'多商品券1'
		"""
		{
			"name": "多商品券1",
			"is_for_specific_products": true,
			"coupon_product": "商品1"
		}
		"""
	Then jobs获得优惠券规则'多商品券2'
		"""
		{
			"name": "多商品券2",
			"is_for_specific_products": true,
			"coupon_product": "商品2,商品3"
		}
		"""
	Then jobs能获得优惠券规则列表
		"""
		[{
			"name": "多商品券2",
			"is_for_specific_products": true,
			"coupon_product": "商品2,商品3"
		}, {
			"name": "多商品券1",
			"is_for_specific_products": true,
			"coupon_product": "商品1"
		}]
		"""


@gaia @promotion @coupon
Scenario:3 添加优惠券规则后，获得码库
	添加优惠券规则后，能获得码库

	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		{
			"name": "单品券",
			"coupon_product": "商品1",
			"money": 10.00,
			"count": 3,
			"coupon_id_prefix": "coupon1_id_"
		}
		"""
	Then jobs能获得优惠券'单品券'的码库
		"""
		{
			"coupon1_id_1": {
				"money": 10.00,
				"status": "未领取",
				"consumer": ""
			},
			"coupon1_id_2": {
				"money": 10.00,
				"status": "未领取",
				"consumer": ""
			},
			"coupon1_id_3": {
				"money": 10.00,
				"status": "未领取",
				"consumer": ""
			}
		}
		"""