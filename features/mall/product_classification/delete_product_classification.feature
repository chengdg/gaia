Feature: 删除商品分类
"""
	manager能删除"商品分类"
"""

Background:
	Given manager登录系统
	When manager已添加商品分类
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

@gaia @mall @mall.product @mall.product_classification @aix
Scenario:1 Jobs删除已存在的商品分类
	Given manager登录系统
	When manager删除商品分类'分类12'
#	Then manager查看商品分类列表
#		|   分类11  |修改,删除,配置标签|
#		|   分类13  |修改,删除,配置标签|

	When manager删除商品分类'分类21'
	Then manager能获得'分类11'的子分类集合
		"""
		["分类22", "分类23"]
		"""