Feature: 搜索会员

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
		"""
		{
			"source": "会员分享"
		}
		"""
	Given bigs成为'jobs'的会员
		"""
		{
			"source": "会员分享"
		}
		"""
	Given zhaowei成为'jobs'的会员
		"""
		{
			"source": "推广扫码"
		}
		"""


@gaia @member @wip
Scenario: 无搜索条件，获得全部会员
	获得会员列表时：
	1. 会员按id倒序排列

	Given jobs登录系统
	When jobs能获得会员列表
		"""
		[{
			"name": "zhaowei",
			"source": "推广扫码"
		}, {
			"name": "bigs",
			"source": "会员分享"
		}, {
			"name": "yaochen",
			"source": "会员分享"
		}, {
			"name": "yangmi",
			"source": "直接关注"
		}, {
			"name": "zhouxun",
			"source": "直接关注"
		}]
		"""