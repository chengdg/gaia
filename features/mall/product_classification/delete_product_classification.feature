Feature: 删除商品分类
"""
	weizoom能删除"商品分类"
"""

Background:
	Given weizoom登录系统
	When weizoom已添加商品分类
		"""
		[{
			"分类11": [{
                "分类21": []
            },{
                "分类22": []
            },{
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

@gaia @mall @mall.product @mall.product_classification @aix
Scenario:1 Jobs删除已存在的商品分类
	Given weizoom登录系统
	When weizoom删除商品分类'分类12'
	Then weizoom查看商品分类列表
		|classfication_name|      operation      |
		|   分类11  |修改,删除,配置标签|
		|   分类13  |修改,删除,配置标签|

	When weizoom删除商品分类'分类21'
	Then weizoom能获得'分类11'的子分类集合
		"""
		["分类22", "分类23"]
		"""

@gaia @mall @mall.product @mall.product_classification @aix
Scenario:2 运营端删除正在使用商品分类

	Given jobs登录系统
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
			"name":"顺丰",
			"first_weight":1,
			"first_weight_price":15.00,
			"added_weight":1,
			"added_weight_price":5.00
		}, {
			"name" : "圆通",
			"first_weight":1,
			"first_weight_price":10.00,
			"special_area": [{
				"to_the":"北京市",
				"first_weight_price":20.00,
				"added_weight_price":10.00
			}]
		}]
		"""
	When jobs选择'顺丰'运费配置
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
			"limit_zone_name":"仅售地区1",
			"postage_type": "使用默认运费模板:顺丰",
			"images":["wuhan.jpg"],
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
			"limit_zone_name":"禁售地区",
			"postage_type": "使用默认运费模板:顺丰",
			"images":["ipad1.jpg"],
			"remark":"苹果平板，大屏看电视"
		}]
		"""
	Then jobs查看待审核商品列表
		|name|classification|price|stock|created_time|status|operation|
		|   ipad     |分类11--分类21|3000.00|200| 创建时间 |   待审核   |编辑|
		|  武汉鸭脖  |分类12--分类24|10.00|200|  创建时间 |   待审核   |编辑|

	Given weizoom登录系统

	Then weizoom查看商品分类列表
		|classfication_name|product_count|
		|      分类11      |     1      |
		|      分类12      |     1     |
		|      分类13      |     0      |

	When weizoom删除商品分类'分类11'

	Then weizoom查看商品分类列表
		|classfication_name|product_count|
		|      分类11      |     1      |
		|      分类12      |     1     |
		|      分类13      |     0      |

	Then weizoom能获得'分类11'的子分类集合
		|classfication_name|product_count|
		|      分类21      |     1      |
		|      分类22      |     0     |
		|      分类23      |     0      |

	When weizoom删除商品分类'分类21'

	Then weizoom能获得'分类11'的子分类集合
		|classfication_name|product_count|
		|      分类21      |     1      |
		|      分类22      |     0     |
		|      分类23      |     0      |