Feature: 创建商品规格
	Jobs通过管理系统在商城中新增供商品使用的"商品规格"


@gaia @mall.product_model_property_value
Scenario:1 添加商品规格信息
	Given jobs登录系统
	When jobs添加商品规格
		"""
		[{
			"name": "颜色",
			"type": "图片",
			"values": [{
				"name": "黑色",
				"image": "/static/test_resource_img/hangzhou1.jpg"
			}, {
				"name": "白色",
				"image": "/static/test_resource_img/hangzhou2.jpg"
			}]
		}]
		"""

	Then jobs修改商品规格属性'黑色'的值
		"""
		{
			"name": "黑色的神秘",
			"pic_url": "/static/test_resource_img/black.jpg"
		}
		"""

	Then jobs能获取商品规格列表
		"""
		[{
			"name": "颜色",
			"type": "图片",
			"values": [{
				"name": "黑色的神秘",
				"image": "/static/test_resource_img/black.jpg"
			}, {
				"name": "白色",
				"image": "/static/test_resource_img/hangzhou2.jpg"
			}]
		}]
		"""
