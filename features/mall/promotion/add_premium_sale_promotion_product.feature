Feature: 添加新买赠促销活动
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
			"name": "红星",
			"type": "固定低价"
		}]
		"""

@add_premium_sale_promotion
Scenario:1 weizoom添加有未参加促销的商品
		2.zhouxun将商品加入买赠促销

	Given weizoom登录系统
	When weizoom添加商品
		"""
		[{

			"name": "红星二锅头-weizoom",
			"supplier": "红星",
			"classification": "分类31"

		}, {
			"name": "红星葡萄酒-weizoom",
			"supplier": "红星",
			"classification": "分类24"

		}]

		"""

	When zhouxun创建一个买赠活动
		"""
		{
			"product": "红星二锅头-weizoom",
			"premium_product": "红星葡萄酒-weizoom",
			"name": "zhouxun买一赠一",
			"promotion_title": "买一瓶二锅头送一瓶葡萄酒",
			"start_date": "2016-12-03 00:00:00",
			"end_date": "2018-12-03 00:00:00",
			"count": "1",
			"is_enable_cycle": "true",
			"premium_count": "1",
			"unit": "瓶"
		}
		"""


	Then zhouxun根据商品名搜索到新创建的买赠活动
		"""
		{
			"product": "红星二锅头-weizoom"
		}
		"""

	When zhouxun结束买赠活动
		"""
		{
			"name": "zhouxun买一赠一"
		}
		"""
	Then zhouxun查看买赠活动'zhouxun买一赠一'状态是'已结束'