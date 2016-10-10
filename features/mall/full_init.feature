Feature: 安装完整测试所需的各种数据

@full_init
Scenario: 安装完整测试数据
	Given jobs登录系统
	#商品
	And jobs已添加商品规格
		"""
		[{
			"name": "颜色",
			"type": "图片",
			"values": [{
				"name": "红色",
				"image": "/static/test_resource_img/icon_color/icon_1.png"
			}, {
				"name": "黄色",
				"image": "/static/test_resource_img/icon_color/icon_5.png"
			}, {
				"name": "蓝色",
				"image": "/static/test_resource_img/icon_color/icon_9.png"
			}]
		}, {
			"name": "尺寸",
			"type": "文字",
			"values": [{
				"name": "M"
			}, {
				"name": "S"
			}, {
				"name": "L"
			}]
		}]
		"""
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
	And jobs已添加商品
		"""
		[{
			"name": "东坡肘子",
			"categories": ["分类1", "分类2", "分类3"],
			"detail": "东坡肘子的详情",
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
			"categories": ["分类1"],
			"detail": "叫花鸡的详情",
			"swipe_images": [{
				"url": "/static/test_resource_img/hangzhou2.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 12.0,
						"weight": 5.5,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		}, {
			"name": "水晶虾仁",
			"categories": ["分类2", "分类3"],
			"detail": "水晶虾仁的详情",
			"swipe_images": [{
				"url": "/static/test_resource_img/hangzhou3.jpg"
			}],
			"model": {
				"models": {
					"红色 S": {
						"price": 10.0,
						"weight": 3.1,
						"stock_type": "有限",
						"stocks": 3
					},
					"黄色 M": {
						"price": 9.1,
						"weight": 1.0,
						"stock_type": "无限"
					},
					"蓝色 M": {
						"price": 11.1,
						"weight": 1.0,
						"stock_type": "有限",
						"stocks": 0
					}
				}
			}
		}, {
			"name": "莲藕排骨汤",
			"categories": ["分类3"],
			"detail": "莲藕排骨汤的详情",
			"swipe_images": [{
				"url": "/static/test_resource_img/tang1.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 5.0
					}
				}
			}
		}, {
			"name": "冬荫功汤",
			"categories": ["分类3"],
			"detail": "冬荫功汤的详情",
			"swipe_images": [{
				"url": "/static/test_resource_img/tang2.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 6.0
					}
				}
			}
		}, {
			"name": "松鼠桂鱼",
			"categories": ["分类3"],
			"detail": "松鼠桂鱼的详情",
			"swipe_images": [{
				"url": "/static/test_resource_img/yu3.jpg"
			}],
			"model": {
				"models": {
					"S": {
						"price": 6.0
					}, 
					"L": {
						"price": 8.0
					}, 
					"M": {
						"price": 7.0
					}
				}
			}
		}, {
			"name": "武昌鱼",
			"detail": "武昌鱼的详情",
			"swipe_images": [{
				"url": "/static/test_resource_img/yu1.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 11.0,
						"weight": 20,
						"stock_type": "有限",
						"stocks": 3
					}
				}
			}
		}, {
			"name": "黄桥烧饼",
			"detail": "黄桥烧饼的详情",
			"swipe_images": [{
				"url": "/static/test_resource_img/mian1.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 2.0
					}
				}
			}
		}, {
			"name": "热干面",
			"detail": "热干面的详情",
			"swipe_images": [{
				"url": "/static/test_resource_img/mian2.jpg"
			}],
			"model": {
				"models": {
					"standard": {
						"price": 1.5
					}
				}
			}
		}]	
		"""
