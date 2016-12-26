#author:徐梓豪  2016-12-19
Feature:mantis-客户编辑商品
	"""
	1.客户编辑已经创建的商品信息
	"""
Background:
	Given manager登录系统
	When manager创建账号
		"""
		{
			"login_account":"aini",
			"password":"1",
			"real_name":"爱伲咖啡",
			"email":"aini@163.com",
			"department":"CorpStaff",
			"right":"商户操作"
		}
		"""
	When manager添加商品分类
		"""
		[{
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
		}]
		"""
	Given aini登录系统
	When aini新增规格名和显示样式
		"""
		[{
			"specification_name":"规格11",
			"type":"文本"
		},{
			"specification_name":"规格12",
			"type":"文本"
		},{
			"specification_name":"规格13",
			"type":"文本"
		}
		}]
		"""
	When aini设置规格值
		"""
		[{
			"specification_name":"规格11",
			"type":"文本",
			"specification_values":["规格1","规格2","规格3"]
		},{
			"specification_name":"规格11",
			"type":"文本",
			"specification_values":["规格21","规格22","规格23"]
		},{
			"specification_name":"规格11",
			"type":"文本",
			"specification_values":["规格31","规格32","规格33"]
		}]
		"""
	When aini点击添加商品
	When aini选择商品分类
		"""
		[{
			"分类12": {
				"分类24": null
			}
		}]
		"""
	When aini添加商品
		"""
		[{
			"product_name": "武汉鸭脖",
			"title":"武汉鸭脖",
			"is_enable_specification":"否",
			"price":10.00,
			"weight":0.23,
			"stocks":200.00,
			"area_setting":"无限制",
			"freight":2.00,
			"picture":"",
			"description":"周黑鸭 鲜卤鸭脖 230g/袋 办公室休闲零食 肉干小食"
		}]
		"""
	When aini点击添加商品
	When aini选择商品分类
		"""
			[{
				"分类11": {
					"分类21": null
				}
			}]
		"""
	When aini添加商品	
		"""
		[{
			"shop_name": "ipad",
			"title":"苹果平板",
			"is_enable_specification":"否",
			"price":3000.00,
			"weight":2.00,
			"stocks":200.00,
			"area_setting":"无限制",
			"freight":5.00,
			"picture":"",
			"description":"苹果平板，大屏看电视"
		}]
		"""
	When aini点击添加商品
	When aini选择商品分类
		"""
		[{
			"分类12": {
				"分类24": null
			}
		}]
		"""
	When aini添加商品
		"""
		[{
			"product_name": "耐克男鞋",
			"title":"耐克男鞋，耐穿耐磨",
			"is_enable_specification":"是",
			"specification":{
						"颜色":["黑色","红色"],
						"尺码":["X","XL"]
			},
			"specification_price":{
						"黑色 X":{
							"price":500.00,
							"weight":0.50,
							"stocks":200.00
						},
						"黑色 XL":{
							"price":500.00,
							"weight":0.50,
							"stocks":100.00
						},
						"红色 X":{
							"price":700.00,
							"weight":0.60,
							"stocks":222.00
						},
						"红色 XL":{
							"price":730.00,
							"weight":0.60,
							"stocks":180.00
							}
			},			
			"area_setting":"无限制",
			"area_limit":"不发货模板",
			"freight":0.00,
			"picture":"",
			"description":"耐克男鞋，耐穿耐磨"
		}]
		"""
	Then aini查看商品列表
		|product_name|classfication|price|sales|stocks|create_time|stock_status|sale_status|operate|
		|  武汉鸭脖  |分类12-分类24|10.00|0.00 |200.00|  创建时间 |   待入库   |  未上架   |编辑|
		|   ipad     |分类11-分类21|3000.00|0.00|200.00| 创建时间 |   待入库   |  未上架   |编辑|
		|  耐克男鞋  |分类12-分类24|500.00-700.00|0.00 |100.00-222.00|  创建时间 |   待入库   |  未上架   |编辑|
@mantis @product
Scenario:1 客户编辑已经创建的商品信息
	When aini编辑商品'ipad'的信息
		"""
		[{
			"shop_name": "ipad",
			"title":"苹果平板",
			"is_enable_specification":"否",
			"price":2000.00,
			"weight":2.00,
			"stocks":200.00,
			"area_setting":"无限制",
			"freight":5.00,
			"picture":"",
			"description":"苹果平板，大屏看电视"
		}]
		"""
	Then aini查看商品列表
		|product_name|classfication|price|sales|stocks|create_time|stock_status|sale_status|operate|
		|  武汉鸭脖  |分类12-分类24|10.00|0.00 |200.00|  创建时间 |   待入库   |  未上架   |编辑|
		|   ipad     |分类11-分类21|2000.00|0.00|200.00| 创建时间 |   待入库   |  未上架   |编辑|
		|  耐克男鞋  |分类12-分类24|500.00-700.00|0.00 |100.00-222.00|  创建时间 |   待入库   |  未上架   |编辑|
	When aini编辑商品'耐克男鞋'的信息
		"""
		[{
			"product_name": "耐克男鞋",
			"title":"耐克男鞋，耐穿耐磨",
			"is_enable_specification":"否",
			"price":200.00,
			"weight":0.50,
			"stocks":200.00,
			"area_setting":"无限制",
			"area_limit":"不发货模板",
			"freight":0.00,
			"picture":"",
			"description":"耐克男鞋，耐穿耐磨"
		}]
		"""
	Then aini查看商品列表
		|product_name|classfication|price|sales|stocks|create_time|stock_status|sale_status|operate|
		|  武汉鸭脖  |分类12-分类24|10.00|0.00 |200.00|  创建时间 |   待入库   |  未上架   |编辑|
		|   ipad     |分类11-分类21|2000.00|0.00|200.00| 创建时间 |   待入库   |  未上架   |编辑|
		|  耐克男鞋  |分类12-分类24|200.00|0.00 |200.00|  创建时间 |   待入库   |  未上架   |编辑|
	Then manager查看分类列表
		|classfication_name|business_number|
		|      分类11      |     1.00      |
		|      分类12      |     2.00      |
		|      分类13      |     0.00      |
	Then manager查看分类'12'的下级分类
	    |classfication_name|business_number|
		|      分类24      |     2.00      |
	When aini修改商品'武汉鸭脖'的分类
		"""
		[{
			"分类11": {
				"分类22": null
			}
		}]
		"""
	Then aini查看商品列表
		|product_name|classfication|price|sales|stocks|create_time|stock_status|sale_status|operate|
		|  武汉鸭脖  |分类11-分类22|10.00|0.00 |200.00|  创建时间 |   待入库   |  未上架   |编辑|
		|   ipad     |分类11-分类21|2000.00|0.00|200.00| 创建时间 |   待入库   |  未上架   |编辑|
		|  耐克男鞋  |分类12-分类24|200.00|0.00 |200.00|  创建时间 |   待入库   |  未上架   |编辑|
	Then manager查看分类列表
		|classfication_name|business_number|
		|      分类11      |     2.00      |
		|      分类12      |     1.00      |
		|      分类13      |     0.00      |
	Then manager查看'分类12'的下级分类
	    |classfication_name|business_number|
		|      分类24      |     1.00      |
	Then manager查看'分类11'的下级分类
		|classfication_name|business_number|
		|      分类21      |     1.00      |
		|      分类22      |     1.00      |
		|      分类23      |     0.00      |
