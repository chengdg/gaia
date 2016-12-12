Feature: 删除商品分组
"""
	Jobs能通过管理系统为商城删除的"商品分组"
"""

Background:
	Given jobs登录系统
	When jobs已添加商品分组
		"""
		{
			"分类11": {
				"分类21": null,
				"分类22": null,
				"分类23": null
			},
			"分类12": {
				"分类24": null
			},
			"分类13": null
		}
		"""

@gaia @mall @mall.product @mall.product_category
Scenario:1 Jobs删除已存在的商品分组
	Given jobs登录系统
	When jobs删除商品分组'分类12'
	Then jobs能获取商品分组列表
		"""
		{
			"分类11": {
				"分类21": null,
				"分类22": null,
				"分类23": null
			},
			"分类13": null
		}
		"""
	When jobs删除商品分组'分类21'
	Then jobs能获取商品分组列表
		"""
		{
			"分类11": {
				"分类22": null,
				"分类23": null
			},
			"分类13": null
		}
		"""

