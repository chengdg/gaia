Feature: 删除商品分组
"""
	Jobs能通过管理系统为商城删除的"商品分类"
"""

Background:
	Given jobs登录系统
	When jobs已添加商品分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]
		"""
	Given bill登录系统
	When bill已添加商品分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]
		"""


@mall @mall.product @mall.product_category @hermes @wip
Scenario:1 Jobs删除已存在的商品分类
	Given jobs登录系统
	When jobs删除商品分类'分类2'
	Then jobs能获取商品分类列表
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类3"
		}]
		"""
	Given bill登录系统
	Then bill能获取商品分类列表
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]
		"""
