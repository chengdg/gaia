#_author_:张三香 2017.01.20

Feature:管理员给订单添加备注信息
	"""
		管理员【备注】订单(最多输入300字，超过300字时不允许输入):
			订单列表显示备注信息
			订单详情显示备注信息
	"""

Background:
	Given 重置'apiserver'的bdd环境
	Given jobs登录系统
	When jobs添加商品
		"""
		[{
			"name": "jobs商品1",
			"model": {
				"models": {
					"standard": {
						"price": 11.00,
						"stock_type": "有限",
						"stocks": 30
					}
				}
			}
		}]
		"""
	Given zhouxun登录系统
	When zhouxun添加支付方式
		"""
		[{
			"type":"微信支付",
			"is_active":"启用",
			"version":3,
			"weixin_appid":"app_id_1",
			"mch_id":"mch_id_1",
			"api_key":"api_key_1",
			"paysign_key":"paysign_key_1"
		}]
		"""
	When zhouxun添加商品
		"""
		[{
			"name":"无规格商品1",
			"swipe_images":
				[{
					"url": "/static/test_resource_img/hangzhou1.jpg"
				},{
					"url": "/static/test_resource_img/hangzhou2.jpg"
				}],
			"model":{
				"models":{
					"standard":{
						"price": 10.10,
						"purchase_price": 10.00,
						"stock_type": "无限"
						}
					}
				}
		}]
		"""
	When zhouxun添加代销商品
		"""
		["jobs商品1"]
		"""
	When zhouxun将商品移动到'在售'货架
		"""
		["无规格商品1", "jobs商品1"]
		"""

	Given bill关注zhouxun的公众号::apiserver
	When bill访问zhouxun的webapp::apiserver
	When bill购买zhouxun的商品::apiserver
		"""
		{
			"order_id":"001",
			"date":"2016-01-01",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type": "微信支付",
			"products":
				[{
					"name":"无规格商品1",
					"count":1
				}],
			"postage":0.00,
			"customer_message": "bill购买无规格商品1"
		}
		"""

@gaia @order
Scenario:1 给订单添加备注信息，备注信息少于300字
	Given zhouxun登录系统
	When zhouxun给订单添加备注信息
		"""
		{
			"bid":"001",
			"remark":"备注信息少于300字！！"
		}
		"""
	Then zhouxun获得订单列表
		"""
		[{
			"bid": "001",
			"remark":"备注信息少于300字！！"
		}]
		"""
	Then zhouxun获得订单'001'
		"""
		{
			"bid": "001",
			"remark":"备注信息少于300字！！"
		}
		"""

@gaia @order
Scenario:2 给订单添加备注信息，备注信息等于300字
	Given zhouxun登录系统
	When zhouxun给订单添加备注信息
		"""
		{
			"bid":"001",
			"remark":"ab备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦"
		}
		"""
	Then zhouxun获得订单列表
		"""
		[{
			"bid": "001",
			"remark":"ab备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦"
		}]
		"""
	Then zhouxun获得订单'001'
		"""
		{
			"bid": "001",
			"remark":"ab备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦订单备注啦"
		}
		"""

@gaia @order
Scenario:3 给多供货商的订单添加备注信息

	When bill访问zhouxun的webapp::apiserver
	When bill购买zhouxun的商品::apiserver
		"""
		{
			"order_id":"002",
			"date":"2016-01-01",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type": "微信支付",
			"products":
				[{
					"name":"无规格商品1",
					"count":1
				},{
					"name":"jobs商品1",
					"count":1
				}]
		}
		"""
	Given zhouxun登录系统
	When zhouxun给订单添加备注信息
		"""
		{
			"bid":"002",
			"remark":"备注信息少于300字！！"
		}
		"""
	Then zhouxun获得订单列表
		"""
		[{
			"bid": "002",
			"remark":"备注信息少于300字！！"
		},{
			"bid": "001",
			"remark":""
		}]
		"""
	Then zhouxun获得订单'002'
		"""
		{
			"bid": "002",
			"remark":"备注信息少于300字！！"
		}
		"""
