#author:徐梓豪  2016-12-15
Feature:客户创建待审核商品
	"""
	1.客户添加无规格商品
	"""
Background:
	Given weizoom登录系统
	When weizoom添加商品分类
		"""
		[{
			"分类11": [{
				"分类21": [],
				"分类22": [],
				"分类23": [{
					"分类31": []
				}]
			}]
		},{
			"分类12": [{
				"分类24": []
			}]
		},{
			"分类13": []
		}]
		"""

@gaia @mall @product @pre_product @add_pre_product @aix
Scenario:1 客户添加无规格商品
	Given jobs登录系统
	When jobs创建商品分类为'分类24'的待审核商品
		"""
		[{
			"name": "武汉鸭脖",
			"promotion_title":"武汉鸭脖",
			"has_product_model":false,
			"price":10.00,
			"weight":0.23,
			"stock":200,
			"limit_zone_type":"无限制",
			"postage_type": "统一运费",
			"postage_money":2.00,
			"images":[],
			"remark":"周黑鸭 鲜卤鸭脖 230g/袋 办公室休闲零食 肉干小食"
		}]
		"""
	When jobs创建商品分类为'分类21'的待审核商品
		"""
		[{
			"name": "ipad",
			"promotion_title":"苹果平板",
			"has_product_model":false,
			"price":3000.00,
			"weight":2.00,
			"stock":200,
			"limit_zone_type":"无限制",
			"postage_type": "统一运费",
			"postage_money":2.00,
			"images":[],
			"remark":"苹果平板，大屏看电视"
		}]
		"""
	Then jobs查看待审核商品列表
		|name|classfication|price|stock|created_time|status|operation|
		|  武汉鸭脖  |分类12--分类24|10.00|200|  创建时间 |   待入库   |编辑|
		|   ipad     |分类11--分类21|3000.00|200| 创建时间 |   待入库   |编辑|

	Given weizoom登录系统

	Then weizoom查看商品分类列表
		|classfication_name|product_count|
		|      分类11      |     1      |
		|      分类12      |     1     |
		|      分类13      |     0      |

	Then weizoom查看商品分类'分类12'的二级分类
	    |classfication_name|product_count|
		|      分类24      |     1      |