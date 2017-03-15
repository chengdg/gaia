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

@gaia @promotion @coupon @wip
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
			"name": "通用券1"
		}, {
			"name": "通用券2"
		}]
		"""