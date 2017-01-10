Feature: 管理代销商品的分组信息

@gaia @mall @mall.product @mall.product_category @aix11
Scenario:1 多个渠道为商品创建代销商品，各自管理商品分组
	多个渠道创建代销商品后，各自独立维护分组信息

	Given weizoom登录系统
	When weizoom添加商品
		"""
		[{
			"name": "东坡肘子"
		}, {
			"name": "叫花鸡"
		}, {
			"name": "莲藕排骨汤"
		}]
		"""
	Given zhouxun登录系统
	When zhouxun添加代销商品
		"""
		["东坡肘子", "叫花鸡", "莲藕排骨汤"]
		"""
	When zhouxun添加商品分组
		"""
		[{
			"name": "zhouxun分组1",
			"products": ["东坡肘子", "叫花鸡", "莲藕排骨汤"]
		}]
		"""
	When zhouxun添加商品分组
		"""
		[{
			"name": "zhouxun分组2",
			"products": ["东坡肘子"]
		}]
		"""
	Given yangmi登录系统
	When yangmi添加代销商品
		"""
		["东坡肘子", "叫花鸡"]
		"""
	When yangmi添加商品分组
		"""
		[{
			"name": "yangmi分组1",
			"products": ["东坡肘子", "叫花鸡"]
		}]
		"""
	Then yangmi能获取商品'东坡肘子'
		"""
		{
			"name": "东坡肘子",
			"categories": ["yangmi分组1"]
		}
		"""
	Given zhouxun登录系统
	Then zhouxun能获取商品'东坡肘子'
		"""
		{
			"name": "东坡肘子",
			"categories": ["zhouxun分组1", "zhouxun分组2"]
		}
		"""

	