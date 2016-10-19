Feature: 从微众商品池中选择商品进行上架
"""
	zhouxun能通过管理系统从微众商品池中选择商品进行上架
"""

Background:
	Given weizoom登录系统
	And weizoom已添加商品分组
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]
		"""
	And weizoom已添加商品规格
		"""
		[{
			"name": "颜色",
			"type": "图片",
			"values": [{
				"name": "黑色",
				"image": "/static/test_resource_img/icon_color/black.png"
			}, {
				"name": "白色",
				"image": "/static/test_resource_img/icon_color/white.png"
			}]
		}, {
			"name": "尺寸",
			"type": "文字",
			"values": [{
				"name": "M"
			}, {
				"name": "S"
			}]
		}]
		"""
	When weizoom添加商品分类
		"""
		[
			["分类11", "分类12"],
			["分类21", "分类22"]
		]
		"""
	When weizoom添加供应商
		"""
		[{
			"name": "苹果"
		}, {
			"name": "微软"
		}, {
			"name": "谷歌"
		}]
		"""

@mall @mall.product @mall.product_management @hermes
Scenario:1 创建供应商供应的商品
	job添加商品后：
	1、能获得商品详情
	2、在待售商品列表能看到商品

	Given weizoom登录系统
	When weizoom添加商品
		"""
		[{
			"name": "东坡肘子",
			"supplier": "苹果"
		}, {
			"name": "叫花鸡",
			"supplier": "微软"
		}, {
			"name": "黄桥烧饼"
		}]
		"""
	Then weizoom能获取商品'东坡肘子'
		"""
		{
			"name": "东坡肘子",
			"supplier": "苹果"
		}
		"""
	Then weizoom能获取商品'叫花鸡'
		"""
		{
			"name": "叫花鸡",
			"supplier": "微软"
		}
		"""
	Then weizoom能获取商品'黄桥烧饼'
		"""
		{
			"name": "黄桥烧饼",
			"supplier": ""
		}
		"""
	Then weizoom能获得'待售'商品列表
		"""
		[{
			"name": "东坡肘子",
			"create_type": "create",
			"supplier": "苹果"
		}, {
			"name": "叫花鸡",
			"create_type": "create",
			"supplier": "微软"
		}, {
			"name": "黄桥烧饼",
			"create_type": "create",
			"supplier": ""
		}]
		"""

@mall @mall.product @mall.product_management @hermes
Scenario:1 创建供应商供应的商品
	job添加商品后：
	1、能获得商品详情
	2、在待售商品列表能看到商品

	Given weizoom登录系统
	When weizoom添加商品
		"""
		[{
			"name": "东坡肘子",
			"supplier": "苹果",
			"model": {
				"models": {
					"standard": {
						"price": 11.12,
						"purchase_price": 1.1,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "叫花鸡",
			"supplier": "微软",
			"model": {
				"models": {
					"黑色 M": {
						"price": 10.1,
						"purchase_price": 1.2,
						"stock_type": "有限",
						"stocks": 10
					},
					"白色 S": {
						"price": 20.2,
						"purchase_price": 1.2,
						"stock_type": "有限",
						"stocks": 20
					}
				}
			}
		}, {
			"name": "黄桥烧饼",
			"model": {
				"models": {
					"standard": {
						"price": 30.1,
						"purchase_price": 1.0,
						"stock_type": "有限",
						"stocks": 30
					}
				}
			}
		}]
		"""
	Given jobs登录系统
	When jobs能够获取微众商品池商品列表
		"""
		[{

		}]
		"""