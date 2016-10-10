Feature: 更新商品
"""
	Jobs能通过管理系统更新"商品"
"""

Background:
	Given jobs登录系统
	And jobs已添加商品分组
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]
		"""
	And jobs已添加商品规格
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
	When jobs已添加支付方式
		"""
		[{
			"type": "货到付款",
			"is_active": "启用"
		},{
			"type": "微信支付",
			"is_active": "启用"
		},{
			"type": "支付宝",
			"is_active": "启用"
		}]
		"""
	When jobs添加邮费配置
		"""
		[{
			"name":"顺丰",
			"first_weight":1,
			"first_weight_price":15.00,
			"added_weight":1,
			"added_weight_price":5.00
		}, {
			"name" : "圆通",
			"first_weight":1,
			"first_weight_price":10.00
		}]
		"""
	When jobs选择'顺丰'运费配置
	Given jobs已添加商品
		"""
		[{
			"name": "东坡肘子",
			"bar_code": "zhouzi_1",
			"min_limit": 10,
			"promotion_title": "促销的东坡肘子",
			"categories": ["分类1"],
			"detail": "东坡肘子的详情",
			"swipe_images": [{
				"url": "/static/test_resource_img/hangzhou1.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 11.12,
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "叫花鸡",
			"swipe_images": [{
				"url": "/static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/static/test_resource_img/hangzhou2.jpg"
			}, {
				"url": "/static/test_resource_img/hangzhou3.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 12.00,
						"weight": 5.5,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		}, {
			"name": "莲藕排骨汤",
			"model": {
				"models": {
					"黑色 M": {
						"price": 1.1,
						"weight": 1.1,
						"stock_type": "无限"
					},
					"黑色 S": {
						"price": 2.2,
						"weight": 2.2,
						"stock_type": "有限",
						"stocks": 99
					}
				}
			}
		}]
		"""

@mall @mall.product @mall.product_management @hermes
Scenario:1 修改商品基本信息
	job修改商品基本信息后：
	1、能获得修改后的商品信息(name, bar_code, min_limit, promotion_title, detail)

	Given jobs登录系统
	Then jobs能获取商品'东坡肘子'
		"""
		{
			"name": "东坡肘子",
			"bar_code": "zhouzi_1",
			"min_limit": 10,
			"promotion_title": "促销的东坡肘子",
			"detail": "东坡肘子的详情",
			"is_member_product": false,
			"is_enable_bill": false
		}
		"""
	When jobs更新商品'东坡肘子'
		#东坡肘子(有分类，上架，无限库存，多轮播图), 叫花鸡(无分类，下架，有限库存，单轮播图)
		"""
		{
			"name": "东坡肘子*",
			"bar_code": "zhouzi_1*",
			"min_limit": 20,
			"promotion_title": "促销的东坡肘子*",
			"detail": "东坡肘子的详情*",
			"is_member_product": true,
			"is_enable_bill": true
		}
		"""
	Then jobs能获取商品'东坡肘子*'
		"""
		{
			"name": "东坡肘子*",
			"bar_code": "zhouzi_1*",
			"categories": ["分类1"],
			"min_limit": 20,
			"promotion_title": "促销的东坡肘子*",
			"detail": "东坡肘子的详情*",
			"swipe_images": [{
				"url": "/static/test_resource_img/hangzhou1.jpg"
			}],
			"is_member_product": true,
			"is_enable_bill": true,
			"model": {
				"models": {
					"standard": {
						"price": 11.12,
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			}
		}
		"""
	
	
@mall @mall.product @mall.product_management @hermes
Scenario:2 修改商品图片信息
	jobs进行如下的图片操作：
	1. 增加图片
	2. 删除图片

	Given jobs登录系统
	When jobs更新商品'东坡肘子'
		#增加图片
		"""
		{
			"swipe_images": [{
				"url": "/static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/static/test_resource_img/hangzhou2.jpg"
			}]
		}
		"""
	Then jobs能获取商品'东坡肘子'
		"""
		{
			"name": "东坡肘子",
			"thumbnails_url": "/static/test_resource_img/hangzhou1.jpg",
			"swipe_images": [{
				"url": "/static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/static/test_resource_img/hangzhou2.jpg"
			}]
		}
		"""
	When jobs更新商品'东坡肘子'
		#删除图片
		"""
		{
			"swipe_images": [{
				"url": "/static/test_resource_img/hangzhou2.jpg"
			}]
		}
		"""
	Then jobs能获取商品'东坡肘子'
		"""
		{
			"name": "东坡肘子",
			"thumbnails_url": "/static/test_resource_img/hangzhou2.jpg",
			"swipe_images": [{
				"url": "/static/test_resource_img/hangzhou2.jpg"
			}]
		}
		"""

@mall @mall.product @mall.product_management @hermes
Scenario:3 修改商品的标准规格
	
	Given jobs登录系统
	When jobs更新商品'东坡肘子'
		#改变price, weight, stock_type从有限变为无限
		"""
		{
			"model": {
				"models": {
					"standard": {
						"price": 22.00,
						"weight": 25.5,
						"stock_type": "无限"
					}
				}
			}
		}
		"""
	Then jobs能获取商品'东坡肘子'
		"""
		{
			"name": "东坡肘子",
			"model": {
				"models": {
					"standard": {
						"price": 22.00,
						"weight": 25.5,
						"stock_type": "无限"
					}
				}
			}
		}
		"""
	When jobs更新商品'东坡肘子'
		#stock_type从无限变为有限
		"""
		{
			"model": {
				"models": {
					"standard": {
						"price": 32.00,
						"weight": 35.5,
						"stock_type": "有限",
						"stocks": 99
					}
				}
			}
		}
		"""
	Then jobs能获取商品'东坡肘子'
		"""
		{
			"name": "东坡肘子",
			"model": {
				"models": {
					"standard": {
						"price": 32.00,
						"weight": 35.5,
						"stock_type": "有限",
						"stocks": 99
					}
				}
			}
		}
		"""

@mall @mall.product @mall.product_management @hermes
Scenario:4 修改商品的商品规格，在标准规格和定制规格之间切换

	Given jobs登录系统
	When jobs更新商品'东坡肘子'
		#切换到定制规格
		"""
		{
			"model": {
				"models": {
					"黑色 M": {
						"price": 22.00,
						"weight": 25.5,
						"stock_type": "无限"
					},
					"白色 M": {
						"price": 32.00,
						"weight": 35.5,
						"stock_type": "有限",
						"stocks": 36
					}
				}
			}
		}
		"""
	Then jobs能获取商品'东坡肘子'
		"""
		{
			"name": "东坡肘子",
			"model": {
				"models": {
					"黑色 M": {
						"price": 22.00,
						"weight": 25.5,
						"stock_type": "无限"
					},
					"白色 M": {
						"price": 32.00,
						"weight": 35.5,
						"stock_type": "有限",
						"stocks": 36
					}
				}
			}
		}
		"""
	When jobs更新商品'东坡肘子'
		#切换到标准规格
		"""
		{
			"model": {
				"models": {
					"standard": {
						"price": 122.00,
						"weight": 125.5,
						"stock_type": "有限",
						"stocks": 100
					}
				}
			}
		}
		"""
	Then jobs能获取商品'东坡肘子'
		"""
		{
			"name": "东坡肘子",
			"model": {
				"models": {
					"standard": {
						"price": 122.00,
						"weight": 125.5,
						"stock_type": "有限",
						"stocks": 100
					}
				}
			}
		}
		"""

@mall @mall.product @mall.product_management @hermes
Scenario:5 修改商品的定制商品规格
	jobs进行以下操作
	1. 添加定制规格
	2. 删除定制规格
	3. 修改定制规格的属性

	Given jobs登录系统
	When jobs更新商品'莲藕排骨汤'
		#切换到定制规格
		"""
		{
			"model": {
				"models": {
					"黑色 M": {
						"price": 10.10,
						"weight": 10.10,
						"stock_type": "有限",
						"stocks": 10
					},
					"白色 S": {
						"price": 3,
						"weight": 3,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		}
		"""
	Then jobs能获取商品'莲藕排骨汤'
		"""
		{
			"name": "莲藕排骨汤",
			"model": {
				"models": {
					"黑色 M": {
						"price": 10.10,
						"weight": 10.10,
						"stock_type": "有限",
						"stocks": 10
					},
					"白色 S": {
						"price": 3,
						"weight": 3,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		}
		"""


@mall @mall.product @mall.product_management @hermes
Scenario:6 修改商品分组信息
	jobs进行如下操作：
	1. 对已经有分组的商品，对分组进行删除、新增
	2. 对无分组的商品，添加分组

	Given jobs登录系统
	When jobs更新商品'东坡肘子'
		#有分组的修改分组
		"""
		{
			"categories": ["分类2", "分类3"]
		}
		"""
	Then jobs能获取商品'东坡肘子'
		"""
		{
			"name": "东坡肘子",
			"categories": ["分类2", "分类3"]
		}
		"""
	When jobs更新商品'叫花鸡'
		#无分组的增加分组
		"""
		{
			"categories": ["分类2"]
		}
		"""
	Then jobs能获取商品'叫花鸡'
		"""
		{
			"name": "叫花鸡",
			"categories": ["分类2"]
		}
		"""

@mall @mall.product @mall.product_management @hermes
Scenario:7 修改物流信息
	jobs进行如下操作：
	1. 修改邮费配置

	Given jobs登录系统
	When jobs更新商品'东坡肘子'
		#有分组的修改分组
		"""
		{
			"postage_type": "运费模板"
		}
		"""
	Then jobs能获取商品'东坡肘子'
		"""
		{
			"name": "东坡肘子",
			"postage_type": "运费模板"
		}
		"""
	When jobs更新商品'东坡肘子'
		"""
		{
			"postage_type": "统一运费",
			"unified_postage_money": 12.34
		}
		"""
	Then jobs能获取商品'东坡肘子'
		"""
		{
			"name": "东坡肘子",
			"postage_type": "统一运费",
			"unified_postage_money": 12.34
		}
		"""

@mall @mall.product @mall.product_management @hermes
Scenario:7 修改商品属性信息
	jobs进行如下操作：
	1. 修改邮费配置

	Given jobs登录系统
	When jobs更新商品'东坡肘子'
		"""
		{
			"properties": [{
				"name": "n1",
				"value": "n2"
			}, {
				"name": "n3",
				"value": "n4"
			}]
		}
		"""
	Then jobs能获取商品'东坡肘子'
		"""
		{
			"name": "东坡肘子",
			"properties": [{
				"name": "n1",
				"value": "n2"
			}, {
				"name": "n3",
				"value": "n4"
			}]
		}
		"""

@ignore
Scenario:2 添加商品时选择分类，能在分类中看到该商品
	Jobs添加一组"商品分类"后，"商品分类列表"会按照添加的顺序倒序排列

	Given jobs登录系统
	When jobs已添加商品分类
		"""
		[{
			"name": "分类1"
		}, {
			"name": "分类2"
		}, {
			"name": "分类3"
		}]
		"""
	Given jobs已添加商品
		#东坡肘子(有分类，上架，无限库存，多轮播图), 叫花鸡(无分类，下架，有限库存，单轮播图)
		"""
		[{
			"name": "东坡肘子",
			"status": "待售",
			"categories": "分类1,分类2",
			"model": {
				"models": {
					"standard": {
						"price": 11.12,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "叫花鸡",
			"status": "待售",
			"categories": "分类1",
			"model": {
				"models": {
					"standard": {
						"price": 12.00,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		}, {
			"name": "水晶虾仁",
			"status": "待售",
			"categories": "",
			"model": {
				"models": {
					"standard": {
						"price": 3.00
					}
				}
			}
		}]
		"""
	Then jobs能获取商品分类列表
		"""
		[{
			"name": "分类1",
			"products": [{
				"name": "叫花鸡",
				"display_price": 12.00,
				"status": "待售"
			}, {
				"name": "东坡肘子",
				"display_price": 11.12,
				"status": "待售"
			}]
		}, {
			"name": "分类2",
			"products": [{
				"name": "东坡肘子",
				"display_price": 11.12,
				"status": "待售"
			}]
		}, {
			"name": "分类3",
			"products": []
		}]
		"""
