Feature: 管理商品，影响商品分组

@gaia @mall @mall.product @mall.product_category
Scenario:1 改变自建商品货架状态，影响分组内商品排序

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
	When jobs添加商品分组
		"""
		[{
			"name": "分组1",
			"products": ["东坡肘子", "叫花鸡", "莲藕排骨汤", "水晶虾仁"]
		}]
		"""
	Then jobs能获取商品分组列表
		"""
		[{
			"name": "分组1",
			"products": [{
				"name": "水晶虾仁",
				"status": "待售"
			}, {
				"name": "莲藕排骨汤",
				"status": "待售"
			}, {
				"name": "叫花鸡",
				"status": "待售"
			}, {
				"name": "东坡肘子",
				"status": "待售"
			}]
		}]
		"""
	Then jobs能获得商品分组'分组1'详情
		"""
		{
			"name": "分组1",
			"products": [{
				"name": "水晶虾仁",
				"status": "待售"
			}, {
				"name": "莲藕排骨汤",
				"status": "待售"
			}, {
				"name": "叫花鸡",
				"status": "待售"
			}, {
				"name": "东坡肘子",
				"status": "待售"
			}]
		}
		"""
	#将商品移动到'在售'货架
	When jobs将商品移动到'在售'货架
		"""
		["东坡肘子", "莲藕排骨汤"]
		"""
	Then jobs能获取商品分组列表
		"""
		[{
			"name": "分组1",
			"products": [{
				"name": "莲藕排骨汤",
				"status": "在售"
			}, {
				"name": "东坡肘子",
				"status": "在售"
			}, {
				"name": "水晶虾仁",
				"status": "待售"
			}, {
				"name": "叫花鸡",
				"status": "待售"
			}]
		}]
		"""
	Then jobs能获得商品分组'分组1'详情
		"""
		{
			"name": "分组1",
			"products": [{
				"name": "莲藕排骨汤",
				"status": "在售"
			}, {
				"name": "东坡肘子",
				"status": "在售"
			}, {
				"name": "水晶虾仁",
				"status": "待售"
			}, {
				"name": "叫花鸡",
				"status": "待售"
			}]
		}
		"""
	#将商品移动到'待售'货架
	When jobs将商品移动到'待售'货架
		"""
		["东坡肘子"]
		"""
	Then jobs能获取商品分组列表
		"""
		[{
			"name": "分组1",
			"products": [{
				"name": "莲藕排骨汤",
				"status": "在售"
			}, {
				"name": "水晶虾仁",
				"status": "待售"
			}, {
				"name": "叫花鸡",
				"status": "待售"
			}, {
				"name": "东坡肘子",
				"status": "待售"
			}]
		}]
		"""
	Then jobs能获得商品分组'分组1'详情
		"""
		{
			"name": "分组1",
			"products": [{
				"name": "莲藕排骨汤",
				"status": "在售"
			}, {
				"name": "水晶虾仁",
				"status": "待售"
			}, {
				"name": "叫花鸡",
				"status": "待售"
			}, {
				"name": "东坡肘子",
				"status": "待售"
			}]
		}
		"""
	#从货架中删除商品
	When jobs从货架删除商品
		"""
		["莲藕排骨汤", "叫花鸡"]
		"""
	Then jobs能获取商品分组列表
		"""
		[{
			"name": "分组1",
			"products": [{
				"name": "水晶虾仁",
				"status": "待售"
			}, {
				"name": "东坡肘子",
				"status": "待售"
			}]
		}]
		"""
	Then jobs能获得商品分组'分组1'详情
		"""
		{
			"name": "分组1",
			"products": [{
				"name": "水晶虾仁",
				"status": "待售"
			}, {
				"name": "东坡肘子",
				"status": "待售"
			}]
		}
		"""


@gaia @mall @mall.product @mall.product_category
Scenario:1 改变代销商品货架状态，影响分组内商品排序

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
	When zhouxun将商品移动到'待售'货架
		"""
		["东坡肘子", "叫花鸡", "黄桥烧饼", "莲藕排骨汤", "水晶虾仁"]
		"""
	When zhouxun添加商品分组
		"""
		[{
			"name": "分组1",
			"products": ["东坡肘子", "叫花鸡", "莲藕排骨汤", "水晶虾仁"]
		}]
		"""
	Then zhouxun能获取商品分组列表
		"""
		[{
			"name": "分组1",
			"products": [{
				"name": "水晶虾仁",
				"status": "待售"
			}, {
				"name": "莲藕排骨汤",
				"status": "待售"
			}, {
				"name": "叫花鸡",
				"status": "待售"
			}, {
				"name": "东坡肘子",
				"status": "待售"
			}]
		}]
		"""
	Then zhouxun能获得商品分组'分组1'详情
		"""
		{
			"name": "分组1",
			"products": [{
				"name": "水晶虾仁",
				"status": "待售"
			}, {
				"name": "莲藕排骨汤",
				"status": "待售"
			}, {
				"name": "叫花鸡",
				"status": "待售"
			}, {
				"name": "东坡肘子",
				"status": "待售"
			}]
		}
		"""
	Given yangmi登录系统
	When yangmi添加代销商品
		"""
		["东坡肘子", "叫花鸡", "黄桥烧饼", "莲藕排骨汤"]
		"""
	When yangmi将商品移动到'待售'货架
		"""
		["东坡肘子", "叫花鸡", "黄桥烧饼", "莲藕排骨汤"]
		"""
	When yangmi添加商品分组
		"""
		[{
			"name": "分组1",
			"products": ["东坡肘子", "叫花鸡", "莲藕排骨汤", "黄桥烧饼"]
		}]
		"""
	Then yangmi能获取商品分组列表
		"""
		[{
			"name": "分组1",
			"products": [{
				"name": "黄桥烧饼",
				"status": "待售"
			}, {
				"name": "莲藕排骨汤",
				"status": "待售"
			}, {
				"name": "叫花鸡",
				"status": "待售"
			}, {
				"name": "东坡肘子",
				"status": "待售"
			}]
		}]
		"""
	#zhouxun移动货架，不影响yangmi
	Given zhouxun登录系统
	When zhouxun将商品移动到'在售'货架
		"""
		["叫花鸡"]
		"""
	Then zhouxun能获取商品分组列表
		"""
		[{
			"name": "分组1",
			"products": [{
				"name": "叫花鸡",
				"status": "在售"
			}, {
				"name": "水晶虾仁",
				"status": "待售"
			}, {
				"name": "莲藕排骨汤",
				"status": "待售"
			}, {
				"name": "东坡肘子",
				"status": "待售"
			}]
		}]
		"""
	Then zhouxun能获得商品分组'分组1'详情
		"""
		{
			"name": "分组1",
			"products": [{
				"name": "叫花鸡",
				"status": "在售"
			}, {
				"name": "水晶虾仁",
				"status": "待售"
			}, {
				"name": "莲藕排骨汤",
				"status": "待售"
			}, {
				"name": "东坡肘子",
				"status": "待售"
			}]
		}
		"""
	Given yangmi登录系统
	Then yangmi能获取商品分组列表
		"""
		[{
			"name": "分组1",
			"products": [{
				"name": "黄桥烧饼",
				"status": "待售"
			}, {
				"name": "莲藕排骨汤",
				"status": "待售"
			}, {
				"name": "叫花鸡",
				"status": "待售"
			}, {
				"name": "东坡肘子",
				"status": "待售"
			}]
		}]
		"""
	#zhouxun从货架删除商品，不影响yangmi
	Given zhouxun登录系统
	When zhouxun从货架删除商品
		"""
		["叫花鸡"]
		"""
	Then zhouxun能获取商品分组列表
		"""
		[{
			"name": "分组1",
			"products": [{
				"name": "水晶虾仁",
				"status": "待售"
			}, {
				"name": "莲藕排骨汤",
				"status": "待售"
			}, {
				"name": "东坡肘子",
				"status": "待售"
			}]
		}]
		"""
	Then zhouxun能获得商品分组'分组1'详情
		"""
		{
			"name": "分组1",
			"products": [{
				"name": "水晶虾仁",
				"status": "待售"
			}, {
				"name": "莲藕排骨汤",
				"status": "待售"
			}, {
				"name": "东坡肘子",
				"status": "待售"
			}]
		}
		"""
	Given yangmi登录系统
	Then yangmi能获取商品分组列表
		"""
		[{
			"name": "分组1",
			"products": [{
				"name": "黄桥烧饼",
				"status": "待售"
			}, {
				"name": "莲藕排骨汤",
				"status": "待售"
			}, {
				"name": "叫花鸡",
				"status": "待售"
			}, {
				"name": "东坡肘子",
				"status": "待售"
			}]
		}]
		"""
	