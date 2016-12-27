#author:徐梓豪  2016-12-15
Feature:gaia-客户新增待入库商品
	"""
	客户添加无规格商品
	"""
Background:
	Given manager登录系统
	When manager添加商品分类
		"""
		[{
			"分类11": [{
				"分类21": [],
				"分类22": []
			}]
		}]
		"""

@gaia @mall @product @pending_product_tmp @aix
Scenario:1 客户添加无规格商品
	When manager创建待入库商品
		"""
		[{
			"classification_name": "分类11",
			"product_name": "武汉鸭脖",
			"promotion_title":"武汉鸭脖",
			"has_product_model": false,
			"price":10.00,
			"weight":0.23,
			"store":200,
			"limit_zone_type":"无限制",
			"postage_type": "统一运费",
			"postage_money":2.00,
			"images": [],
			"remark":"周黑鸭 鲜卤鸭脖 230g/袋 办公室休闲零食 肉干小食"
		}]
		"""
	When manager审核通过待入库商品
		"""
		["武汉鸭脖"]
		"""