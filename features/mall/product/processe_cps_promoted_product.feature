Feature: 添加新的推广商品
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

@process_cps_promoted_products
Scenario:1 weizoom已经有了推广商品
		2.zhouxun已经有了代售商品

	Given weizoom登录系统
	When weizoom添加商品
		"""
		[{

			"name": "东坡肘子-weizoom",
			"supplier": "苹果",
			"classification": "分类31"

		}, {
			"name": "叫花鸡-weizoom",
			"supplier": "微软",
			"classification": "分类24"

		}, {
			"name": "水晶虾仁-weizoom",
			"supplier": "谷歌",
			"classification": "分类13"
		}]

		"""
	When weizoom将商品加入CPS推广
		"""
		[{
			"product_name": "东坡肘子-weizoom",
			"promote_money": "10.0",
			"promote_stock": "50",
			"promote_time_from": "2016-01-01",
			"promote_time_to": "2019-01-01"

		}, {
			"product_name": "叫花鸡-weizoom",
			"promote_money": 10.0,
			"promote_stock": "50",
			"promote_time_from": "2016-01-01",
			"promote_time_to": "2019-02-01"
		}, {
			"product_name": "水晶虾仁-weizoom",
			"promote_money": 10.0,
			"promote_stock": 50,
			"promote_time_from": "2016-01-01",
			"promote_time_to": "2019-03-01"
		}]
		"""
	When zhouxun创建代售商品
		"""
		["东坡肘子-weizoom", "叫花鸡-weizoom", "水晶虾仁-weizoom"]
		"""


	Then zhouxun可以查询到至少3个新增推广商品

	Then zhouxun处理推广商品
		"""
		["东坡肘子-weizoom"]
		"""

