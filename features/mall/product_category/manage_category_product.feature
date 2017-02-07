Feature: 管理分组中的商品
"""
	Jobs能通过管理系统管理分组中的商品
"""

@gaia @mall @mall.product @mall.product_category
Scenario:1 从分组中删除商品

	Given jobs登录系统
	When jobs添加商品
		"""
		[{
			"name": "东坡肘子"
		}, {
			"name": "叫花鸡"
		}, {
			"name": "莲藕排骨汤"
		}]
		"""
	When jobs添加商品分组
		"""
		[{
			"name": "分组1",
			"products": ["东坡肘子", "叫花鸡", "莲藕排骨汤"]
		}]
		"""
	Then jobs能获取商品分组列表
		"""
		[{
			"name": "分组1",
			"products": [{
				"name": "莲藕排骨汤"
			}, {
				"name": "叫花鸡"
			}, {
				"name": "东坡肘子"
			}]
		}]
		"""
	When jobs从商品分组'分组1'中删除商品'叫花鸡'
	Then jobs能获取商品分组列表
		"""
		[{
			"name": "分组1",
			"products": [{
				"name": "莲藕排骨汤"
			}, {
				"name": "东坡肘子"
			}]
		}]
		"""

@gaia @mall @mall.product @mall.product_category
Scenario:2 调整分组中商品排序

	Given jobs登录系统
	When jobs添加商品
		"""
		[{
			"name": "东坡肘子"
		}, {
			"name": "叫花鸡"
		}, {
			"name": "莲藕排骨汤"
		}]
		"""
	When jobs添加商品分组
		"""
		[{
			"name": "分组1",
			"products": ["东坡肘子", "叫花鸡", "莲藕排骨汤"]
		}]
		"""
	Then jobs能获取商品分组列表
		"""
		[{
			"name": "分组1",
			"products": [{
				"name": "莲藕排骨汤",
				"display_index": 0
			}, {
				"name": "叫花鸡",
				"display_index": 0
			}, {
				"name": "东坡肘子",
				"display_index": 0
			}]
		}]
		"""
	When jobs更新商品分组'分组1'中商品'叫花鸡'的排序为'2'
	Then jobs能获取商品分组列表
		"""
		[{
			"name": "分组1",
			"products": [{
				"name": "叫花鸡",
				"display_index": 2
			}, {
				"name": "莲藕排骨汤",
				"display_index": 0
			}, {
				"name": "东坡肘子",
				"display_index": 0
			}]
		}]
		"""
	When jobs更新商品分组'分组1'中商品'莲藕排骨汤'的排序为'1'
	Then jobs能获取商品分组列表
		"""
		[{
			"name": "分组1",
			"products": [{
				"name": "莲藕排骨汤",
				"display_index": 1
			}, {
				"name": "叫花鸡",
				"display_index": 2
			}, {
				"name": "东坡肘子",
				"display_index": 0
			}]
		}]
		"""
	#更新一个商品为new_position，会重置之前diaplay_index为new_position的商品
	When jobs更新商品分组'分组1'中商品'东坡肘子'的排序为'1'
	Then jobs能获取商品分组列表
		"""
		[{
			"name": "分组1",
			"products": [{
				"name": "东坡肘子",
				"display_index": 1
			}, {
				"name": "叫花鸡",
				"display_index": 2
			}, {
				"name": "莲藕排骨汤",
				"display_index": 0
			}]
		}]
		"""

@gaia @mall @mall.product @mall.product_category @ztqb
Scenario:3 向分组中增加商品
	向分组中添加商品后，能获得新的分组信息

	Given jobs登录系统
	When jobs添加商品
		"""
		[{
			"name": "东坡肘子"
		}, {
			"name": "叫花鸡"
		}, {
			"name": "莲藕排骨汤"
		}, {
			"name": "黄桥烧饼"
		}]
		"""
	When jobs添加商品分组
		"""
		[{
			"name": "分组1",
			"products": ["东坡肘子", "叫花鸡"]
		}]
		"""
	Then jobs能获取商品分组列表
		"""
		[{
			"name": "分组1",
			"products": [{
				"name": "叫花鸡"
			}, {
				"name": "东坡肘子"
			}]
		}]
		"""
	When jobs向商品分组'分组1'中添加商品
		"""
		["莲藕排骨汤", "黄桥烧饼"]
		"""
	Then jobs能获取商品分组列表
		"""
		[{
			"name": "分组1",
			"products": [{
				"name": "黄桥烧饼"
			}, {
				"name": "莲藕排骨汤"
			}, {
				"name": "叫花鸡"
			}, {
				"name": "东坡肘子"
			}]
		}]
		"""
	#重复添加，不会加入重复的记录
	When jobs向商品分组'分组1'中添加商品
		"""
		["莲藕排骨汤", "黄桥烧饼"]
		"""
	Then jobs能获取商品分组列表
		"""
		[{
			"name": "分组1",
			"products": [{
				"name": "黄桥烧饼"
			}, {
				"name": "莲藕排骨汤"
			}, {
				"name": "叫花鸡"
			}, {
				"name": "东坡肘子"
			}]
		}]
		"""


@gaia @mall @mall.product @mall.product_category
Scenario:4 向分组中增加商品，影响商品的分组信息

	Given jobs登录系统
	When jobs添加商品
		"""
		[{
			"name": "东坡肘子"
		}, {
			"name": "叫花鸡"
		}, {
			"name": "莲藕排骨汤"
		}, {
			"name": "黄桥烧饼"
		}]
		"""
	When jobs添加商品分组
		"""
		[{
			"name": "分组1",
			"products": ["东坡肘子", "叫花鸡"]
		}]
		"""
	Then jobs能获取商品分组列表
		"""
		[{
			"name": "分组1",
			"products": [{
				"name": "叫花鸡"
			}, {
				"name": "东坡肘子"
			}]
		}]
		"""
	When jobs向商品分组'分组1'中添加商品
		"""
		["莲藕排骨汤", "黄桥烧饼", "东坡肘子"]
		"""
	Then jobs能获取商品'东坡肘子'
		"""
		{
			"name": "东坡肘子",
			"categories": ["分组1"]
		}
		"""
	Then jobs能获取商品'黄桥烧饼'
		"""
		{
			"name": "黄桥烧饼",
			"categories": ["分组1"]
		}
		"""
	#重复添加，不会加入重复的记录
	When jobs向商品分组'分组1'中添加商品
		"""
		["莲藕排骨汤", "黄桥烧饼"]
		"""
	Then jobs能获取商品'黄桥烧饼'
		"""
		{
			"name": "黄桥烧饼",
			"categories": ["分组1"]
		}
		"""
	#添加黄桥烧饼到新的分组
	When jobs添加商品分组
		"""
		[{
			"name": "分组2",
			"products": ["黄桥烧饼"]
		}]
		"""
	When jobs添加商品分组
		"""
		[{
			"name": "分组3"
		}]
		"""
	When jobs向商品分组'分组3'中添加商品
		"""
		["黄桥烧饼"]
		"""
	Then jobs能获取商品'黄桥烧饼'
		"""
		{
			"name": "黄桥烧饼",
			"categories": ["分组1", "分组2", "分组3"]
		}
		"""
	