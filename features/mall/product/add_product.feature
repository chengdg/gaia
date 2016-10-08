Feature: 添加新商品
"""
	Jobs能通过管理系统添加"商品"
"""

Background:
	Given jobs登录系统
	And jobs已添加商品分类
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

@mall @mall.product @mall.product_management @hermes
Scenario:1 添加标准规格商品
	job添加商品后：
	1、能获得商品详情
	2、在待售商品列表能看到商品

	Given jobs登录系统
	When jobs添加商品
		#东坡肘子(有分类，上架，无限库存，多轮播图), 叫花鸡(无分类，下架，有限库存，单轮播图)
		"""
		[{
			"name": "东坡肘子",
			"bar_code": "zhouzi_1",
			"min_limit": 10,
			"promotion_title": "促销的东坡肘子",
			"categories": "分类1,分类2,分类3",
			"detail": "东坡肘子的详情",
			"status": "待售",
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
						"price": 11.12,
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "叫花鸡",
			"detail": "叫花鸡的详情",
			"status": "待售",
			"swipe_images": [{
				"url": "/static/test_resource_img/hangzhou2.jpg"
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
		}]
		"""
	Then jobs能获取商品'东坡肘子'
		"""
		{
			"name": "东坡肘子",
			"bar_code": "zhouzi_1",
			"min_limit": 10,
			"promotion_title": "促销的东坡肘子",
			"categories": "分类1,分类2,分类3",
			"detail": "东坡肘子的详情",
			"swipe_images": [{
				"url": "/static/test_resource_img/hangzhou1.jpg"
			}, {
				"url": "/static/test_resource_img/hangzhou2.jpg"
			}, {
				"url": "/static/test_resource_img/hangzhou3.jpg"
			}],
			"is_use_custom_model": "否",
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
	Then jobs能获取商品'叫花鸡'
		"""
		{
			"name": "叫花鸡",
			"swipe_images": [{
				"url": "/static/test_resource_img/hangzhou2.jpg"
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
		}
		"""
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "东坡肘子",
			"bar_code": "zhouzi_1",
			"categories": "分类1,分类2,分类3",
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"image": "/static/test_resource_img/hangzhou1.jpg"
		}, {
			"name": "叫花鸡",
			"price": 12.00,
			"stocks": 3,
			"sales": 0,
			"image": "/static/test_resource_img/hangzhou2.jpg"
		}]
		"""

@mall @mall.product @mall.product_management @hermes
Scenario:1 添加定制规格商品
	job添加商品后：
	1、能获得商品详情
	2、在待售商品列表能看到商品

	Given jobs登录系统
	When jobs添加商品
		#东坡肘子：多个定制规格，包含有限和无限库存
		#叫花鸡：单个定制规格
		"""
		[{
			"name": "东坡肘子",
			"model": {
				"models": {
					"黑色 M": {
						"price": 11.12,
						"weight": 5.0,
						"stock_type": "无限"
					},
					"白色 S": {
						"price": 21.12,
						"weight": 25.0,
						"stock_type": "有限",
						"stocks": 99
					}
				}
			}
		}, {
			"name": "叫花鸡",
			"model": {
				"models": {
					"黑色 S": {
						"price": 3.14,
						"weight": 3.14,
						"stock_type": "无限"
					}
				}
			}
		}]
		"""
	Then jobs能获取商品'东坡肘子'
		"""
		{
			"name": "东坡肘子",
			"is_use_custom_model": "是",
			"model": {
				"models": {
					"黑色 M": {
						"price": 11.12,
						"weight": 5.0,
						"stock_type": "无限"
					},
					"白色 S": {
						"price": 21.12,
						"weight": 25.0,
						"stock_type": "有限",
						"stocks": 99
					}
				}
			}
		}
		"""
	Then jobs能获取商品'叫花鸡'
		"""
		{
			"name": "叫花鸡",
			"is_use_custom_model": "是",
			"model": {
				"models": {
					"黑色 S": {
						"price": 3.14,
						"weight": 3.14,
						"stock_type": "无限"
					}
				}
			}
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
