Feature: 搜索优惠券规则
	Jobs能通过管理系统搜索"优惠券规则"

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

@gaia @promotion @coupon
Scenario:1 按优惠券名称搜索
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "通用券1"
		}, {
			"name": "通用券2"
		}, {
			"name": "单品券"
		}]
		"""
	When jobs搜索优惠券规则
		"""
		{
			"name": "通用券"
		}
		"""
	Then jobs能获得优惠券规则搜索结果
		"""
		[{
			"name": "通用券2"
		}, {
			"name": "通用券1"
		}]
		"""

@gaia @promotion @coupon
Scenario:1 按优惠券的状态搜索
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "通用券1",
			"start_date": "2017-01-01 11:00",
			"end_date": "2017-01-02 12:00"
		}, {
			"name": "通用券2",
			"start_date": "2017-02-01 12:00",
			"end_date": "2017-02-02 13:11"
		}, {
			"name": "通用券3",
			"start_date": "昨天",
			"end_date": "1天后"
		}, {
			"name": "通用券4",
			"start_date": "明天",
			"end_date": "3天后"
		}]
		"""
	When jobs搜索优惠券规则
		"""
		{
			"status": "not_start"
		}
		"""
	Then jobs能获得优惠券规则搜索结果
		"""
		[{
			"name": "通用券4"
		}]
		"""
	When jobs搜索优惠券规则
		"""
		{
			"status": "running"
		}
		"""
	Then jobs能获得优惠券规则搜索结果
		"""
		[{
			"name": "通用券3"
		}]
		"""
	When jobs搜索优惠券规则
		"""
		{
			"status": "finished"
		}
		"""
	Then jobs能获得优惠券规则搜索结果
		"""
		[{
			"name": "通用券2"
		}, {
			"name": "通用券1"
		}]
		"""


@gaia @promotion @coupon
Scenario:1 按优惠券的时间搜索
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "通用券1",
			"start_date": "2017-01-01 11:00",
			"end_date": "2017-03-02 12:00"
		}, {
			"name": "通用券2",
			"start_date": "2017-02-01 12:00",
			"end_date": "2017-02-02 13:11"
		}]
		"""
	#时间范围只包含通用券2
	When jobs搜索优惠券规则
		"""
		{
			"promotion_date": ["2017-01-01 00:00", "2017-03-01 00:00"]
		}
		"""
	Then jobs能获得优惠券规则搜索结果
		"""
		[{
			"name": "通用券2"
		}]
		"""
	#时间范围包含通用券1和通用券2
	When jobs搜索优惠券规则
		"""
		{
			"promotion_date": ["2017-01-01 00:00", "2017-03-03 00:00"]
		}
		"""
	Then jobs能获得优惠券规则搜索结果
		"""
		[{
			"name": "通用券2"
		}, {
			"name": "通用券1"
		}]
		"""
	#只指定开始时间，只包含通用券2
	When jobs搜索优惠券规则
		"""
		{
			"promotion_date": ["2017-01-30 00:00", null]
		}
		"""
	Then jobs能获得优惠券规则搜索结果
		"""
		[{
			"name": "通用券2"
		}]
		"""
	#只指定结束时间，只包含通用券2
	When jobs搜索优惠券规则
		"""
		{
			"promotion_date": [null, "2017-03-01 00:00"]
		}
		"""
	Then jobs能获得优惠券规则搜索结果
		"""
		[{
			"name": "通用券2"
		}]
		"""

@gaia @promotion @coupon
Scenario:1 按优惠券类型搜索
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "通用券1"
		}, {
			"name": "通用券2"
		}, {
			"name": "多品券1",
			"coupon_product": "商品1"
		}, {
			"name": "多品券2",
			"coupon_product": "商品2,商品3"
		}]
		"""
	#搜索通用券
	When jobs搜索优惠券规则
		"""
		{
			"rule_type": "general"
		}
		"""
	Then jobs能获得优惠券规则搜索结果
		"""
		[{
			"name": "通用券2"
		}, {
			"name": "通用券1"
		}]
		"""
	#搜索通用券
	When jobs搜索优惠券规则
		"""
		{
			"rule_type": "specific"
		}
		"""
	Then jobs能获得优惠券规则搜索结果
		"""
		[{
			"name": "多品券2"
		}, {
			"name": "多品券1"
		}]
		"""

@gaia @promotion @coupon @wip
Scenario:1 按优惠券码库中的bid搜索
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "通用券1",
			"coupon_id_prefix": "coupon1_id_"
		}, {
			"name": "通用券2",
			"coupon_id_prefix": "coupon2_id_"
		}]
		"""
	#搜索通用券1
	When jobs搜索优惠券规则
		"""
		{
			"bid": "coupon1_id_3"
		}
		"""
	Then jobs能获得优惠券规则搜索结果
		"""
		[{
			"name": "通用券1"
		}]
		"""
	#搜索通用券2
	When jobs搜索优惠券规则
		"""
		{
			"bid": "coupon2_id_1"
		}
		"""
	Then jobs能获得优惠券规则搜索结果
		"""
		[{
			"name": "通用券2"
		}]
		"""