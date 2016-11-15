Feature: 管理商品货架


@gaia @mall @mall.product @mall.product_management
Scenario:1 管理自建商品的货架状态

	Given jobs登录系统
	When jobs添加商品
		"""
		[{
			"name": "东坡肘子"
		}, {
			"name": "叫花鸡"
		}, {
			"name": "黄桥烧饼"
		}, {
			"name": "莲藕排骨汤"
		}, {
			"name": "水晶虾仁"
		}]
		"""
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "水晶虾仁"
		}, {
			"name": "莲藕排骨汤"
		}, {
			"name": "黄桥烧饼"
		}, {
			"name": "叫花鸡"
		}, {
			"name": "东坡肘子"
		}]
		"""
	#移动单个商品
	When jobs将商品移动到'在售'货架
		"""
		["东坡肘子"]
		"""
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "水晶虾仁"
		}, {
			"name": "莲藕排骨汤"
		}, {
			"name": "黄桥烧饼"
		}, {
			"name": "叫花鸡"
		}]
		"""
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "东坡肘子"
		}]
		"""
	#移动多个商品
	When jobs将商品移动到'在售'货架
		"""
		["叫花鸡", "水晶虾仁"]
		"""
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "莲藕排骨汤"
		}, {
			"name": "黄桥烧饼"
		}]
		"""
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "水晶虾仁"
		}, {
			"name": "叫花鸡"
		}, {
			"name": "东坡肘子"
		}]
		"""
	#从货架删除商品
	When jobs从货架删除商品
		"""
		["叫花鸡", "黄桥烧饼"]
		"""
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "莲藕排骨汤"
		}]
		"""
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "水晶虾仁"
		}, {
			"name": "东坡肘子"
		}]
		"""

@gaia @mall @mall.product @mall.product_management
Scenario:1 管理代销商品的货架状态

	Given weizoom登录系统
	When weizoom添加商品
		"""
		[{
			"name": "东坡肘子"
		}, {
			"name": "叫花鸡"
		}, {
			"name": "黄桥烧饼"
		}, {
			"name": "莲藕排骨汤"
		}, {
			"name": "水晶虾仁"
		}]
		"""
	Given zhouxun登录系统
	When zhouxun添加代销商品
		"""
		["东坡肘子", "叫花鸡", "黄桥烧饼", "莲藕排骨汤", "水晶虾仁"]
		"""
	Then zhouxun能获得'zhouxun商品池'商品列表
		"""
		[{
			"name": "水晶虾仁"
		}, {
			"name": "莲藕排骨汤"
		}, {
			"name": "黄桥烧饼"
		}, {
			"name": "叫花鸡"
		}, {
			"name": "东坡肘子"
		}]
		"""
	Then zhouxun能获得'在售'商品列表
		"""
		[]
		"""
	Then zhouxun能获得'待售'商品列表
		"""
		[]
		"""
	#移动到在售货架
	When zhouxun将商品移动到'在售'货架
		"""
		["东坡肘子", "叫花鸡", "水晶虾仁"]
		"""
	Then zhouxun能获得'待售'商品列表
		"""
		[]
		"""
	Then jobs能获得'在售'商品列表
		"""
		[{
			"name": "水晶虾仁"
		}, {
			"name": "叫花鸡"
		}, {
			"name": "东坡肘子"
		}]
		"""
	Then zhouxun能获得'zhouxun商品池'商品列表
		"""
		[{
			"name": "莲藕排骨汤"
		}, {
			"name": "黄桥烧饼"
		}]
		"""
	#移动到待售货架
	When jobs将商品移动到'待售'货架
		"""
		["叫花鸡", "水晶虾仁"]
		"""
	Then zhouxun能获得'待售'商品列表
		"""
		[{
			"name": "水晶虾仁"
		}, {
			"name": "叫花鸡"
		}]
		"""
	Then zhouxun能获得'在售'商品列表
		"""
		[{
			"name": "东坡肘子"
		}]
		"""
	Then zhouxun能获得'zhouxun商品池'商品列表
		"""
		[{
			"name": "莲藕排骨汤"
		}, {
			"name": "黄桥烧饼"
		}]
		"""
	#从货架删除商品
	When zhouxun从货架删除商品
		"""
		["叫花鸡", "东坡肘子"]
		"""
	Then zhouxun能获得'待售'商品列表
		"""
		[{
			"name": "水晶虾仁"
		}]
		"""
	Then zhouxun能获得'在售'商品列表
		"""
		[]
		"""
	Then zhouxun能获得'zhouxun商品池'商品列表
		"""
		[{
			"name": "莲藕排骨汤"
		}, {
			"name": "黄桥烧饼"
		}, {
			"name": "叫花鸡"
		}, {
			"name": "东坡肘子"
		}]
		"""