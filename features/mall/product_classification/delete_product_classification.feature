Feature: 删除商品分类
"""
	weizoom能删除"商品分类"
"""

Background:
	Given weizoom登录系统
	When weizoom已添加商品分类
		"""
		[{
			"分类11": [{
				"分类21": [],
				"分类22": [],
				"分类23": []
			}]
		},{
			"分类12": [{
				"分类24": []
			}]
		},{
			"分类13": []
		}]
		"""

@gaia @mall @mall.product @mall.product_classification
Scenario:1 Jobs删除已存在的商品分类
	Given weizoom登录系统
	When weizoom删除商品分类'分类12'
	Then weizoom查看商品分类列表
		|classfication_name|      operation      |
		|   分类11  |修改,删除,配置标签|
		|   分类13  |修改,删除,配置标签|

	When weizoom删除商品分类'分类21'
	Then weizoom能获得'分类11'的子分类集合
		"""
		["分类22", "分类23"]
		"""