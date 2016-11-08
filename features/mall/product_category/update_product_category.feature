Feature: 添加商品分组
"""
	Jobs能通过管理系统为管理商城添加的"商品分组"
"""

@gaia @mall @mall.product @mall.product_category @hermes
Scenario:1 修改商品分组名

	Given jobs登录系统
	When jobs添加商品分组
		"""
		[{
			"name": "分组1"
		}, {
			"name": "分组2"
		}, {
			"name": "分组3"
		}]
		"""
	Then jobs能获取商品分组列表
		"""
		[{
			"name": "分组1"
		}, {
			"name": "分组2"
		}, {
			"name": "分组3"
		}]
		"""
	When jobs更新商品分组'分组1'为
		"""
		{
			"name": "分组1*"
		}
		"""
	Then jobs能获取商品分组列表
		"""
		[{
			"name": "分组1*"
		}, {
			"name": "分组2"
		}, {
			"name": "分组3"
		}]
		"""
