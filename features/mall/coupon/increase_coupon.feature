Feature: 增加优惠券码库数量
	Jobs能通过管理系统为优惠券增加码库数量

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
Scenario:1 增加优惠券码库数量
	增加优惠券码库数量后:
	1. 优惠券规则的码库中出现增加优惠券
	2. 优惠券规则的库存信息发生变化

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
				"money": 10.00
			},
			"coupon1_id_2": {
				"money": 10.00
			},
			"coupon1_id_3": {
				"money": 10.00
			}
		}
		"""
	Then jobs能获得优惠券规则列表
		"""
		[{
			"name": "单品券",
			"count": 3,
			"remained_count": 3
		}]
		"""
	When jobs为优惠券'单品券'增加'2'个库存
	Then jobs能获得优惠券'单品券'的码库
		"""
		{
			"coupon1_id_1": {
				"money": 10.00
			},
			"coupon1_id_2": {
				"money": 10.00
			},
			"coupon1_id_3": {
				"money": 10.00
			},
			"coupon1_id_4": {
				"money": 10.00,
				"status": "未领取"
			},
			"coupon1_id_5": {
				"money": 10.00,
				"status": "未领取"
			}
		}
		"""
	Then jobs能获得优惠券规则列表
		"""
		[{
			"name": "单品券",
			"count": 5,
			"remained_count": 5
		}]
		"""
