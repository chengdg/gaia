Feature: 为会员发放优惠券

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
	Given zhouxun成为'jobs'的会员
	Given yangmi成为'jobs'的会员
	Given yaochen成为'jobs'的会员
	Given bigs成为'jobs'的会员


@gaia @member
Scenario: 为会员发放优惠券
	向会员发放优惠券后
	1. 会员信息中携带正确的优惠券列表
	2. 优惠券规则的信息发生变化
	3. 优惠券的信息发生变化

	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "多商品券1",
			"coupon_product": "商品1",
			"money": 10,
			"count": 5,
			"coupon_id_prefix": "coupon1_id_"
		}, {
			"name": "通用券2",
			"money": 5,
			"count": 3
		}]
		"""
	Then jobs能获得会员'zhouxun'的优惠券集合
		"""
		[]
		"""
	Then jobs能获得优惠券规则列表
		"""
		[{
			"name": "通用券2",
			"count": 3,
			"remained_count": 3
		}, {
			"name": "多商品券1",
			"count": 5,
			"remained_count": 5
		}]
		"""
	Then jobs能获得优惠券'多商品券1'的码库
		"""
		{
			"coupon1_id_1": {
				"status": "未领取"
			},
			"coupon1_id_2": {
				"status": "未领取"
			}, 
			"coupon1_id_3": {
				"status": "未领取"
			}, 
			"coupon1_id_4": {
				"status": "未领取"
			}, 
			"coupon1_id_5": {
				"status": "未领取"
			}
		}
		"""
	#发放第一张优惠券
	When jobs为会员每人发放'1'张优惠券'多商品券1'
		"""
		["zhouxun", "yangmi"]
		"""
	Then jobs能获得会员'zhouxun'的优惠券集合
		"""
		[{
			"name": "多商品券1",
			"money": 10,
			"is_for_specific_products": true,
			"status": "unused"
		}]
		"""
	Then jobs能获得会员'yangmi'的优惠券集合
		"""
		[{
			"name": "多商品券1",
			"money": 10,
			"is_for_specific_products": true,
			"status": "unused"
		}]
		"""
	#发放第二张优惠券
	When jobs为会员每人发放'1'张优惠券'通用券2'
		"""
		["zhouxun"]
		"""
	Then jobs能获得会员'zhouxun'的优惠券集合
		"""
		[{
			"name": "通用券2",
			"money": 5,
			"is_for_specific_products": false,
			"status": "unused"
		}, {
			"name": "多商品券1",
			"money": 10,
			"is_for_specific_products": true,
			"status": "unused"
		}]
		"""
	Then jobs能获得会员'yangmi'的优惠券集合
		"""
		[{
			"name": "多商品券1",
			"money": 10,
			"is_for_specific_products": true,
			"status": "unused"
		}]
		"""
	Then jobs能获得优惠券规则列表
		"""
		[{
			"name": "通用券2",
			"count": 3,
			"remained_count": 2
		}, {
			"name": "多商品券1",
			"count": 5,
			"remained_count": 3
		}]
		"""
	Then jobs能获得优惠券'多商品券1'的码库
		"""
		{
			"coupon1_id_1": {
				"status": "未使用",
				"receiver": "zhouxun"
			},
			"coupon1_id_2": {
				"status": "未使用",
				"receiver": "yangmi"
			}, 
			"coupon1_id_3": {
				"status": "未领取"
			}, 
			"coupon1_id_4": {
				"status": "未领取"
			}, 
			"coupon1_id_5": {
				"status": "未领取"
			}
		}
		"""

@gaia @member
Scenario: 为会员发放领取数量不为1的优惠券
	向会员发放优惠券后
	1. 会员信息中携带正确的优惠券列表
	2. 优惠券的信息发生变化

	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		{
			"name": "多商品券1",
			"coupon_product": "商品1",
			"money": 10,
			"count": 5,
			"limit_counts": 2
		}
		"""
	Then jobs能获得会员'zhouxun'的优惠券集合
		"""
		[]
		"""
	Then jobs能获得优惠券规则列表
		"""
		[{
			"name": "多商品券1",
			"count": 5,
			"remained_count": 5
		}]
		"""
	When jobs为会员每人发放'2'张优惠券'多商品券1'
		"""
		["zhouxun"]
		"""
	Then jobs能获得会员'zhouxun'的优惠券集合
		"""
		[{
			"name": "多商品券1",
			"money": 10,
			"is_for_specific_products": true,
			"status": "unused"
		}, {
			"name": "多商品券1",
			"money": 10,
			"is_for_specific_products": true,
			"status": "unused"
		}]
		"""
	Then jobs能获得优惠券规则列表
		"""
		[{
			"name": "多商品券1",
			"count": 5,
			"remained_count": 3
		}]
		"""