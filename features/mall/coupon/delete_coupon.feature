Feature: 删除优惠券
	Jobs能通过管理系统删除"优惠券规则"中的优惠券

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
Scenario:1 删除优惠券
	删除优惠券后:
	1. 优惠券规则的码库中不再出现此优惠券

	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		{
			"name": "单品券",
			"coupon_product": "商品1",
			"money": 10.00,
			"count": 5,
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
			},
			"coupon1_id_4": {
				"money": 10.00
			},
			"coupon1_id_5": {
				"money": 10.00
			}
		}
		"""
	When jobs批量删除优惠券
		"""
		["coupon1_id_1", "coupon1_id_3"]
		"""
	Then jobs能获得优惠券'单品券'的码库
		"""
		{
			"coupon1_id_2": {
				"money": 10.00
			},
			"coupon1_id_4": {
				"money": 10.00
			},
			"coupon1_id_5": {
				"money": 10.00
			}
		}
		"""
