Feature: 更新优惠券规则
	Jobs能通过管理系统添加"优惠券规则"
	未下单用户指没有待发货、已发货和已完成订单的用户
	
Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 200.00
		}]
		"""


@gaia @promotion @coupon
Scenario:1 更新优惠券规则
	更新优惠券规则后：
	1. 能获得更新后的优惠券规则详情
	2. 能获得正确的优惠券规则列表

	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "全店通用券1",
			"description":"全店通用券1使用说明",
			"note": "全店通用券1的备注"
		}, {
			"name": "全店通用券2",
			"description":"全店通用券2使用说明",
			"note": "全店通用券2的备注"
		}]
		"""
	When jobs更新优惠券规则'全店通用券1'为
		"""
		{
			"name": "全店通用券1*",
			"description":"全店通用券1使用说明*",
			"note": "全店通用券1的备注*"
		}
		"""
	Then jobs获得优惠券规则'全店通用券1*'
		"""
		{
			"name": "全店通用券1*",
			"description":"全店通用券1使用说明*",
			"note": "全店通用券1的备注*"
		}
		"""
	Then jobs能获得优惠券规则列表
		"""
		[{
			"name": "全店通用券2",
			"description":"全店通用券2使用说明",
			"note": "全店通用券2的备注"
		}, {
			"name": "全店通用券1*",
			"description":"全店通用券1使用说明*",
			"note": "全店通用券1的备注*"
		}]
		"""