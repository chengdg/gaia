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

 @gaia @set_onshelf_product_order
Scenario: 设置zhouxun的商品列表商品排列顺序

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
	Given zhouxun登录系统
	When zhouxun添加代销商品
		"""
		["东坡肘子-weizoom", "叫花鸡-weizoom", "水晶虾仁-weizoom"]
		"""

	When zhouxun将商品移动到'在售'货架
		"""
		["东坡肘子-weizoom", "叫花鸡-weizoom", "水晶虾仁-weizoom"]
		"""

	When zhouxun设置商品显示顺序
	"""
	[{

		"name": "东坡肘子-weizoom",
		"position": "2"

	}, {
		"name": "叫花鸡-weizoom",
		"position": "1"

	}, {
		"name": "水晶虾仁-weizoom",
		"position": "3"
	}]
	"""

	Then zhouxun能获得'在售'商品列表
		"""
		[{
			"name": "叫花鸡-weizoom"
		}, {
			"name": "东坡肘子-weizoom"
		}, {
			"name": "水晶虾仁-weizoom"
		}]
		"""
