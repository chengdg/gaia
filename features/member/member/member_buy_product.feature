Feature: 搜索会员
	zhouxun: 供货商+社群商城
	yangmi: 供货商
	leijun...: 微信用户

Background:
	Given yangmi登录系统
	When yangmi添加商品
		"""
		[{
			"name": "无规格商品1-yangmi",
			"model": {
				"models":{
					"standard":{
						"price": 10.00,
						"purchase_price": 9.00,
						"stock_type": "有限",
						"stocks": 100
					}
				}
			}
		}]
		"""

	Given zhouxun登录系统
	When zhouxun更新积分规则为
		"""
		{
			"integral_each_yuan": 20
		}
		"""
	Given zhouxun已添加商品规格
		"""
		[{
			"name": "颜色",
			"type": "图片",
			"values": [{
				"name": "黑色",
				"image": "/static/test_resource_img/icon_color/black.png"
			},{
				"name": "白色",
				"image": "/static/test_resource_img/icon_color/white.png"
			}]
		},{
			"name": "尺寸",
			"type": "文字",
			"values": [{
				"name": "M"
			},{
				"name": "S"
			}]
		}]
		"""
	When zhouxun添加支付方式
		"""
		[{
			"type": "支付宝",
			"is_active": "启用"
		}]
		"""

	When zhouxun添加商品
		"""
		[{
			"name": "无规格商品1-zhouxun",
			"model":{
				"models":{
					"standard":{
						"price": 10,
						"purchase_price": 9.00,
						"stock_type": "有限",
						"stocks": 100
					}
				}
			}
		},{
			"name": "多规格商品2-zhouxun",
			"model":{
				"models": {
					"黑色 M": {
						"price": 20,
						"purchase_price": 19.22,
						"stock_type": "有限",
						"stocks": 100
					},
					"白色 S": {
						"price": 21,
						"purchase_price": 20.22,
						"stock_type": "有限",
						"stocks": 100
					}
				}
			}
		}]
		"""
	When zhouxun添加代销商品
		"""
		["无规格商品1-yangmi"]
		"""
	When zhouxun将商品移动到'在售'货架
		"""
		["无规格商品1-zhouxun", "多规格商品2-zhouxun","无规格商品1-yangmi"]
		"""
	Given mayun成为'zhouxun'的会员
	Given liyanhong成为'zhouxun'的会员
	Given leijun成为'zhouxun'的会员
		"""
		{
			"source": "会员分享"
		}
		"""
	Given dinglei成为'zhouxun'的会员
		"""
		{
			"source": "会员分享"
		}
		"""
	Given mahuateng成为'zhouxun'的会员
		"""
		{
			"source": "推广扫码"
		}
		"""


@gaia @member @cross_service
Scenario: 购买商品影响会员信息
	会员购买商品后：

	When 微信用户批量消费zhouxun的商品
	| order_id | date      | consumer | product             | payment     |  action      |
	|   0001   | 2天前      |   mayun  | 无规格商品1-zhouxun,1 | 支付宝,1天前  |  mayun,完成   |
	|   0002   | 3天前      |   leijun | 无规格商品1-zhouxun,2 |             |              |