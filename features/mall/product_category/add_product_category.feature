Feature: 添加商品分组
"""
	Jobs能通过管理系统为管理商城添加的"商品分组"
"""

@gaia @mall @mall.product @mall.product_category
Scenario:1 添加无商品的商品分组
	Jobs添加一组"商品分组"后，"商品分组列表"会按照添加的顺序倒序排列

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
	Given bill登录系统
	Then bill能获取商品分组列表
		"""
		[]
		"""


@gaia @mall @mall.product @mall.product_category
Scenario:2 添加包含商品的商品分组

	Given jobs登录系统
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
	When jobs添加商品
		#东坡肘子(有分类，上架，无限库存，多轮播图), 包含其他所有信息
		#叫花鸡(无分类，下架，有限库存，单轮播图)
		"""
		[{
			"name": "东坡肘子",
			"model": {
				"models": {
					"standard": {
						"price": 11.12
					}
				}
			}
		}, {
			"name": "叫花鸡",
			"model": {
				"models": {
					"standard": {
						"price": 12.00
					}
				}
			}
		}, {
			"name": "莲藕排骨汤",
			"model": {
				"models": {
					"standard": {
						"price": 1.1
					}
				}
			}
		}]
		"""
	When jobs添加商品分组
		"""
		[{
			"name": "分组1",
			"products": ["东坡肘子", "叫花鸡", "莲藕排骨汤"]
		}, {
			"name": "分组2",
			"products": ["东坡肘子"]
		}, {
			"name": "分组3",
			"products": ["东坡肘子"]
		}]
		"""
	Then jobs能获取商品分组列表
		"""
		[{
			"name": "分组1",
			"products": [{
				"name": "东坡肘子",
				"price": 11.12,
				"sales": 0,
				"status": "待售"
			}, {
				"name": "叫花鸡",
				"price": 12.00,
				"sales": 0,
				"status": "待售"
			}, {
				"name": "莲藕排骨汤",
				"price": 1.1,
				"sales": 0,
				"status": "待售"
			}]
		}, {
			"name": "分组2"
		}, {
			"name": "分组3"
		}]
		"""
	Then jobs能获得商品分组'分组1'详情
		"""
		{
			"name": "分组1",
			"products": [{
				"name": "东坡肘子",
				"price": 11.12,
				"sales": 0,
				"status": "待售",
				"categories": ["分组1", "分组2", "分组3"]
			}, {
				"name": "叫花鸡",
				"price": 12.00,
				"sales": 0,
				"status": "待售",
				"categories": ["分组1"]
			}, {
				"name": "莲藕排骨汤",
				"price": 1.1,
				"sales": 0,
				"status": "待售",
				"categories": ["分组1"]
			}]
		}
		"""


@gaia @mall @mall.product @mall.product_category
Scenario:3 添加商品时获取分组的可选商品集合
	#TODO: 加上在售、待售的排序特性

	Given jobs登录系统
	When jobs添加商品
		"""
		[{
			"name": "东坡肘子",
			"model": {
				"models": {
					"standard": {
						"price": 11.12
					}
				}
			}
		}, {
			"name": "叫花鸡",
			"model": {
				"models": {
					"standard": {
						"price": 12.00
					}
				}
			}
		}, {
			"name": "莲藕排骨汤",
			"model": {
				"models": {
					"standard": {
						"price": 1.1
					}
				}
			}
		}]
		"""
	When jobs添加商品分组
		"""
		[{
			"name": "分组1"
		}, {
			"name": "分组2",
			"products": ["东坡肘子"]
		}]
		"""
	Then jobs能获得商品分组'分组3'的可选商品集合为
		#还没有创建的分组，可以获取全部商品
		"""
		[{
			"name": "东坡肘子",
			"price": 11.12,
			"sales": 0,
			"status": "待售"
		}, {
			"name": "叫花鸡",
			"price": 12.00,
			"sales": 0,
			"status": "待售"
		}, {
			"name": "莲藕排骨汤",
			"price": 1.1,
			"sales": 0,
			"status": "待售"
		}]
		"""
	Then jobs能获得商品分组'分组1'的可选商品集合为
		#没有商品的分组，可以获取全部商品
		"""
		[{
			"name": "东坡肘子",
			"price": 11.12,
			"sales": 0,
			"status": "待售"
		}, {
			"name": "叫花鸡",
			"price": 12.00,
			"sales": 0,
			"status": "待售"
		}, {
			"name": "莲藕排骨汤",
			"price": 1.1,
			"sales": 0,
			"status": "待售"
		}]
		"""
	Then jobs能获得商品分组'分组2'的可选商品集合为
		#有商品的分组，可以获取剩余商品
		"""
		[{
			"name": "叫花鸡",
			"price": 12.00,
			"sales": 0,
			"status": "待售"
		}, {
			"name": "莲藕排骨汤",
			"price": 1.1,
			"sales": 0,
			"status": "待售"
		}]
		"""


@ignore
Scenario:2 添加商品时选择分组，能在分组中看到该商品
	Jobs添加一组"商品分组"后，"商品分组列表"会按照添加的顺序倒序排列

	Given jobs登录系统
	When jobs已添加商品分组
		"""
		[{
			"name": "分组1"
		}, {
			"name": "分组2"
		}, {
			"name": "分组3"
		}]
		"""
	Given jobs已添加商品
		#东坡肘子(有分组，上架，无限库存，多轮播图), 叫花鸡(无分组，下架，有限库存，单轮播图)
		"""
		[{
			"name": "东坡肘子",
			"status": "待售",
			"categories": "分组1,分组2",
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
			"categories": "分组1",
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
	Then jobs能获取商品分组列表
		"""
		[{
			"name": "分组1",
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
			"name": "分组2",
			"products": [{
				"name": "东坡肘子",
				"display_price": 11.12,
				"status": "待售"
			}]
		}, {
			"name": "分组3",
			"products": []
		}]
		"""
