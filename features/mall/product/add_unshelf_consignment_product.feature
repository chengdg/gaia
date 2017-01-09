Feature: 添加代销商品
"""

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
		{
			"分类11": {
				"分类21": null,
				"分类22": null,
				"分类23": {
					"分类31": null
				}
			},
			"分类12": {
				"分类24": null
			},
			"分类13": null
		}
		"""
	When weizoom添加供应商
		"""
		[{
			"name": "苹果",
			"type": "固定低价"
		}, {
			"name": "微软",
			"type": "首月55分成",
			"divide_info": {
				"divide_money": 1.0,
				"basic_rebate": 20,
				"rebate": 30
			}
		}, {
			"name": "谷歌",
			"type": "零售返点",
			"retail_info": {
				"rebate": 50
			}
		}]
		"""

@gaia @unshelf_consignment
Scenario:1 weizoom已经有了商品

	Given weizoom登录系统
	When weizoom添加商品
		"""
		[{
			"name": "东坡肘子",
			"bar_code": "zhouzi_1",
			"min_limit": 10,
			"promotion_title": "促销的东坡肘子",
			"categories": ["分类1", "分类2", "分类3"],
			"detail": "东坡肘子的详情",
			"status": "待售",
			"is_member_product": true,
			"is_enable_bill": true,
			"postage_type": "统一运费",
			"unified_postage_money": 3.1,
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
						"purchase_price": 1.11,
						"weight": 5.0,
						"stock_type": "无限"
					}
				}
			},
			"properties": [{
				"name": "产地",
				"value": "南京"
			}, {
				"name": "品质",
				"value": "优"
			}]
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

	When zhouxun添加代销商品
		"""
		["东坡肘子", "叫花鸡"]
		"""


	Then zhouxun能获得'待销'商品列表
		"""
		[{
			"name": "叫花鸡",
			"create_type": "sync",
			"price": 12.00,
			"stocks": 3,
			"sales": 0,
			"image": "/static/test_resource_img/hangzhou2.jpg"
		}, {
			"name": "东坡肘子",
			"create_type": "sync",
			"bar_code": "zhouzi_1",
			"categories": "分类1,分类2,分类3",
			"price": 11.12,
			"stocks": "无限",
			"sales": 0,
			"image": "/static/test_resource_img/hangzhou1.jpg"
		}]
		"""