#author:徐梓豪  2016-12-15
Feature:运营驳回客户创建的商品
	"""
	1.运营驳回客户创建的商品
		#驳回后的商品状态为'入库驳回',鼠标放在入库驳回上时，要出现悬浮窗，显示驳回原因
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
@mantis @reject_product
	Scenario:1 运营驳回商品入库请求
	When manager驳回商品'ipad'
	Then aini查看商品列表
		|product_name|classfication|price|sales|stocks|create_time|stock_status|sale_status|operate|
		|  武汉鸭脖  |分类12-分类24|10.00|0.00 |200.00|  创建时间 |   待入库   |  未上架   |编辑|
		|   ipad     |分类11-分类21|3000.00|0.00|200.00| 创建时间 |   待入库   | 入库驳回  |编辑|
		|  耐克男鞋  |分类12-分类24|500.00-700.00|0.00 |100.00-222.00|  创建时间 |   待入库   |  未上架   |编辑|