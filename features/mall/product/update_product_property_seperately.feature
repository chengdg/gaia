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
Scenario:1 单独修改商品价格

	Given jobs登录系统
	#修改标准规格的价格
	Then jobs能获取商品'东坡肘子'
		"""
		{
			"name": "东坡肘子",
			"model": {
				"models": {
					"standard": {
						"price": 11.12
					}
				}
			}
		}
		"""
	When jobs修改商品'东坡肘子'的价格为
		"""
		{
			"standard": 3.14
		}
		"""
	Then jobs能获取商品'东坡肘子'
		"""
		{
			"name": "东坡肘子",
			"model": {
				"models": {
					"standard": {
						"price": 3.14
					}
				}
			}
		}
		"""
	#修改定制规格的价格
	Then jobs能获取商品'莲藕排骨汤'
		"""
		{
			"name": "莲藕排骨汤",
			"model": {
				"models": {
					"黑色 M": {
						"price": 1.1
					},
					"黑色 S": {
						"price": 2.2
					}
				}
			}
		}
		"""
	When jobs修改商品'莲藕排骨汤'的价格为
		"""
		{
			"黑色 M": 3.14,
			"黑色 S": 3.15
		}
		"""
	Then jobs能获取商品'莲藕排骨汤'
		"""
		{
			"name": "莲藕排骨汤",
			"model": {
				"models": {
					"黑色 M": {
						"price": 3.14
					},
					"黑色 S": {
						"price": 3.15
					}
				}
			}
		}
		"""


@mall @mall.product @mall.product_management @hermes
Scenario:2 单独修改商品库存

	Given jobs登录系统
	#将标准规格由无限库存修改为有限库存
	Then jobs能获取商品'东坡肘子'
		"""
		{
			"model": {
				"models": {
					"standard": {
						"stock_type": "无限"
					}
				}
			}
		}
		"""
	When jobs修改商品'东坡肘子'的库存为
		"""
		{
			"standard": {
				"stock_type": "有限",
				"stocks": 99
			}		
		}
		"""
	Then jobs能获取商品'东坡肘子'
		"""
		{
			"model": {
				"models": {
					"standard": {
						"stock_type": "有限",
						"stocks": 99
					}
				}
			}
		}
		"""
	#将标准规格由有限库存修改为无限库存
	Then jobs能获取商品'叫花鸡'
		"""
		{
			"model": {
				"models": {
					"standard": {
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		}
		"""	
	When jobs修改商品'叫花鸡'的库存为
		"""
		{
			"standard": {
				"stock_type": "无限"
			}
		}
		"""
	Then jobs能获取商品'叫花鸡'
		"""
		{
			"model": {
				"models": {
					"standard": {
						"stock_type": "无限"
					}
				}
			}
		}
		"""
	#修改定制规格
	Then jobs能获取商品'莲藕排骨汤'
		"""
		{
			"model": {
				"models": {
					"黑色 M": {
						"stock_type": "无限"
					},
					"黑色 S": {
						"stock_type": "有限",
						"stocks": 99
					}
				}
			}
		}
		"""
	When jobs修改商品'莲藕排骨汤'的库存为
		"""
		{
			"黑色 M": {
				"stock_type": "有限",
				"stocks": 199
			},
			"黑色 S": {
				"stock_type": "无限"
			}
		}
		"""
	Then jobs能获取商品'莲藕排骨汤'
		"""
		{
			"model": {
				"models": {
					"黑色 M": {
						"stock_type": "有限",
						"stocks": 199
					},
					"黑色 S": {
						"stock_type": "无限"
					}
				}
			}
		}
		"""
	
@mall @mall.product @mall.product_management @hermes
Scenario:2 单独修改商品的排序

	Given jobs登录系统
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "东坡肘子",
			"display_index": 9999999
		}, {
			"name": "叫花鸡",
			"display_index": 9999999
		}, {
			"name": "莲藕排骨汤",
			"display_index": 9999999
		}]
		"""
	When jobs修改商品'叫花鸡'的显示排序为'2'
	Then jobs能获得'待售'商品列表
		"""
		[{
			"name": "叫花鸡",
			"display_index": 2
		}, {
			"name": "东坡肘子",
			"display_index": 9999999
		}, {
			"name": "莲藕排骨汤",
			"display_index": 9999999
		}]
		"""
