Feature: 管理分组中的商品
"""
	Jobs能通过管理系统管理分组中的商品
"""

@mall @mall.product @mall.product_category @hermes
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
				"name": "东坡肘子"
			}, {
				"name": "叫花鸡"
			}, {
				"name": "莲藕排骨汤"
			}]
		}]
		"""
	When jobs从商品分组'分组1'中删除商品'叫花鸡'
	Then jobs能获取商品分组列表
		"""
		[{
			"name": "分组1",
			"products": [{
				"name": "东坡肘子"
			}, {
				"name": "莲藕排骨汤"
			}]
		}]
		"""

@mall @mall.product @mall.product_category @hermes
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
				"name": "东坡肘子"
			}, {
				"name": "叫花鸡"
			}, {
				"name": "莲藕排骨汤"
			}]
		}]
		"""
	When jobs更新商品分组'分组1'中商品'叫花鸡'的排序为'2'
	Then jobs能获取商品分组列表
		"""
		[{
			"name": "分组1",
			"products": [{
				"name": "叫花鸡"
			}, {
				"name": "东坡肘子"
			}, {
				"name": "莲藕排骨汤"
			}]
		}]
		"""
	When jobs更新商品分组'分组1'中商品'莲藕排骨汤'的排序为'1'
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

@mall @mall.product @mall.product_category @hermes
Scenario:3 向分组中增加商品

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
				"name": "东坡肘子"
			}, {
				"name": "叫花鸡"
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
				"name": "东坡肘子"
			}, {
				"name": "叫花鸡"
			}, {
				"name": "莲藕排骨汤"
			}, {
				"name": "黄桥烧饼"
			}]
		}]
		"""