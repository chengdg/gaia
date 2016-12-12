Feature: 删除商品分组
"""
	运营能够删除"商品分类"
"""

Background:
	Given manager登录系统
	When manager已添加商品分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]
		"""


@gaia @mall @mall.product @mall.product_classification
Scenario:1 Jobs删除已存在的商品分类
	Given manager登录系统
	When manager删除商品分组'分类2'
	Then manager能获取商品分组列表
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类3"
		}]
		"""