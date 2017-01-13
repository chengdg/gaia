#author:徐梓豪  2016-12-15
Feature:运营审核客户创建的商品
	"""
	1.运营审核通过客户创建的商品
	2.运营审核驳回客户创建的商品
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
			}],
			"分类13": []
		}]
		"""
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
	When jobs添加限定区域配置
		"""
		{
			"name": "禁售地区",
			"limit_area": [{
				"area": "其它",
				"province": ["香港特别行政区"]
			}]
		}
		"""
	When jobs添加限定区域配置
		"""
		{
			"name": "仅售地区",
			"limit_area": [{
				"area": "直辖市",
				"province": ["北京市","天津市","上海市","重庆市"]
			}]
		}
		"""
	When jobs添加限定区域配置
		"""
		{
			"name": "仅售地区1",
			"limit_area": [{
				"area": "直辖市",
				"province": ["北京市","天津市"]
			},{
				"area": "华北-东北",
				"province": "河北省",
				"city": ["石家庄市","唐山市","沧州市"]
			},{
				"area": "华北-东北",
				"province": "山西省",
				"city": ["太原市","大同市","阳泉市","长治市","晋城市","朔州市","晋中市","运城市","忻州市","临汾市","吕梁市"]
			},{
				"area": "华东地区",
				"province": "江苏省",
				"city": ["苏州市"]
			},{
				"area": "西北-西南",
				"province": "陕西省",
				"city": ["西安市"]
			},{
				"area": "其它",
				"province": ["香港特别行政区","澳门特别行政区","台湾省"]
			}]
		}
		"""
	When jobs添加邮费配置
		"""
		[{
			"name": "圆通",
			"first_weight": 40,
			"first_weight_price": 4.00,
			"added_weight": 1,
			"added_weight_price": 6.00
		},{
			"name": "顺丰",
			"first_weight": 41,
			"first_weight_price": 5.00
		},{
			"name": "EMS",
			"first_weight": 1,
			"first_weight_price": 15.00,
			"added_weight": 1,
			"added_weight_price": 5.00,
			"special_area": [{
				"to_the": "北京市",
				"first_weight": 1.0,
				"first_weight_price": 20.00,
				"added_weight": 1.0,
				"added_weight_price": 10.00
			},{
				"to_the": "上海市,重庆市,江苏省",
				"first_weight": 1.0,
				"first_weight_price": 30.00,
				"added_weight": 1.0,
				"added_weight_price": 20.00
			}]
		},{
			"name": "韵达",
			"first_weight": 1,
			"first_weight_price": 12.00,
			"added_weight": 1,
			"added_weight_price": 2.00,
			"free_postages": [{
				"to_the": "上海市",
				"condition": "count",
				"value": 1
			},{
				"to_the": "北京市,重庆市,江苏省",
				"condition": "money",
				"value": 2.0
			}]
		}]
		"""
	When jobs选择'EMS'运费配置
	When jobs创建商品分类为'分类24'的待审核商品
		"""
		[{
			"name": "武汉鸭脖",
			"promotion_title":"武汉鸭脖",
			"has_product_model":false,
			"price":10.00,
			"weight":0.23,
			"stock":200,
			"limit_zone_type":"仅发货地区",
			"limit_zone_model_name":"仅售地区1",
			"postage_type": "使用默认运费模板:EMS",
			"images":['一张图片'],
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
			"limit_zone_type":"不发货地区",
			"limit_zone_model_name":"禁售地区",
			"postage_type": "使用默认运费模板:EMS",
			"images":['2张图片'],
			"remark":"苹果平板，大屏看电视"
		}]
		"""
	When jobs创建分类为'分类23'的待审核商品
		"""
		[{
			"name":"多规格商品1",
			"promotion_title":"多规格商品1",
			"has_product_model":true,
			"model":[{
				"黑色 S":{
					"price":3.00,
					"weight":5.00,
					"stocks":200
				}
			},{
				"白色 M":{
					"price":5.50,
					"weight":7.00,
					"stocks":300
				}
			}],
			"limit_zone_type":"仅发货地区",
			"limit_zone_model_name":"仅售地区",
			"postage_type": "使用默认运费模板:EMS",
			"images":['多规格图片'],
			"remark":"多规格商品1"
		}]
		"""
	Then jobs查看待审核商品列表
		|name|classfication|price|stock|created_time|status|operation|
		|  武汉鸭脖  |分类12--分类24|10.00|200|  创建时间 |   待审核   |编辑|
		|   ipad     |分类11--分类21|3000.00|200| 创建时间 |   待审核   |编辑|
		|多规格商品1|分类11--分类23|3.00-5.00|200.00-300.00|  创建时间 |   待审核   |编辑|

	When jobs提交商品审核
		"""
		["武汉鸭脖", "ipad"]
		"""

	Then jobs查看待审核商品列表
		|name|classfication|price|stock|created_time|status|operation|
		|  武汉鸭脖  |分类12--分类24|10.00|200|  创建时间 |   审核中  |编辑|
		|   ipad     |分类11--分类21|3000.00|200| 创建时间 |   审核中   |编辑|
		|多规格商品1|分类11--分类23|3.00-5.00|200.00-300.00|  创建时间 |   待审核   |编辑|


@gaia @mall @product @pre_product @pending_pre_product @aix
Scenario:1 运营审核通过客户创建的商品
	Given weizoom登录系统
	Then weizoom查看待审核商品列表
		|name|owner_name|classfication|status|    operation   |
		|  武汉鸭脖  |     jobs    |分类12--分类24| 审核中   |通过 驳回 删除|
		|   ipad     |     jobs    |分类11--分类21| 审核中   |通过 驳回 删除|

	When weizoom审核通过待审核商品
		"""
		["ipad"]
		"""

	Then weizoom查看待审核商品列表
		|name|owner_name|classfication|status|    operation   |
		|  武汉鸭脖  |     jobs    |分类12--分类24|  审核中   |通过 驳回 删除|
		|   ipad     |     jobs    |分类11--分类21|  已审核   |删除|

	Given jobs登录系统
	Then jobs查看待审核商品列表
		|name|classfication|price|stock|created_time|status|operation|
		|  武汉鸭脖  |分类12--分类24|10.00|200|  创建时间 |   审核中   |编辑|
		|   ipad     |分类11--分类21|3000.00|200| 创建时间 |   已审核   |编辑|
		|多规格商品1|分类11--分类23|3.00-5.00|200.00-300.00|  创建时间 |   待审核   |编辑|
@gaia @mall @product @pre_product @review_pre_product @aix1
Scenario:2 运营审核驳回客户创建的商品
	Given weizoom登录系统
	When weizoom驳回待审核商品
		"""
		[{
		"name":"武汉鸭脖",
		"reason":"商品名称不规范，标准格式：品牌名+商品名+包装规格"	
		}]
		"""
		
	Then weizoom查看待审核商品列表
		|name|owner_name|classfication|status|    operation   |
		|  武汉鸭脖  |     jobs    |分类12--分类24| 已驳回   |删除|
		|   ipad     |     jobs    |分类11--分类21| 审核中   |通过 驳回 删除|
	Given jobs登录系统
	Then jobs查看商品列表
		|name|classfication|price|stock|created_time|status|operation|
		|  武汉鸭脖  |分类12--分类24|10.00|200|  创建时间 |   审核驳回   |编辑 重新提交审核|
		|   ipad     |分类11--分类21|3000.00|200| 创建时间 |   待审核   |编辑|
		|多规格商品1|分类11--分类23|3.00-5.00|200.00-300.00|  创建时间 |   待审核   |编辑|