Feature: 修改物流信息
	"""
		zhouxun能为用户出货单进行发货后，对物流信息进行修改
		1 对出货单进行发货，使用物流（非其他），修改物流信息
			1.1 普通物流修改为其他
			1.2 普通物流修改为普通物流
		2 对出货单进行发货，使用其他物流，修改物流信息
			2.1 其他物流修改为普通物流
			2.2 其他物流修改其他物流
	"""

Background:
	Given yangmi登录系统
	When yangmi添加商品
		"""
		[{
			"name": "土豆yangmi",
			"model": {
				"models": {
					"standard": {
						"price": 20.00,
						"stock_type": "无限"
					}
				}
			}
		}]
		"""

	Given zhouxun登录系统
	When zhouxun添加商品
		"""
		[{
			"name": "东坡肘子zhouxun",
			"model": {
				"models": {
					"standard": {
						"price": 10.00,
						"stock_type": "无限"
					}
				}
			}
		}, {
			"name": "黄桥烧饼zhouxun",
			"model": {
				"models": {
					"standard": {
						"price": 30.00,
						"stock_type": "无限"
					}
				}
			}
		}]
		"""

	When zhouxun添加支付方式
		"""
		[{
			"type": "微信支付",
			"is_active": "启用",
			"version": 3,
			"weixin_appid": "app_id_1",
			"mch_id": "mch_id_1",
			"api_key": "api_key_1",
			"paysign_key": "paysign_key_1"
		}]
		"""
	When zhouxun添加代销商品
		"""
			["土豆yangmi"]
		"""

	When zhouxun将商品移动到'在售'货架
		"""
			["东坡肘子zhouxun","土豆yangmi"]
		"""
	Given bill关注zhouxun的公众号::apiserver
	When bill访问zhouxun的webapp::apiserver

	When bill购买zhouxun的商品::apiserver
		"""
		{
			"order_id":"001",
			"date":"2016-10-01 10:00:00",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type": "微信支付",
			"products":[{
				"name":"东坡肘子zhouxun",
				"count":1
			}]
		}
		"""		
	When bill使用支付方式'微信支付'进行支付订单'001'于2016-10-01 10:01:00::apiserver

	When bill购买zhouxun的商品::apiserver
		"""
		{
			"order_id":"002",
			"date":"2016-10-02 10:00:00",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type": "微信支付",
			"products":[{
				"name":"东坡肘子zhouxun",
				"count":1
			},{
				"name":"土豆yangmi",
				"count":1
			}]
		}
		"""		
	When bill使用支付方式'微信支付'进行支付订单'002'于2016-10-02 10:01:00::apiserver

	When bill购买zhouxun的商品::apiserver
		"""
		{
			"order_id":"003",
			"date":"2016-10-03 10:00:00",
			"ship_name": "bill",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type": "微信支付",
			"products":[{
				"name":"东坡肘子zhouxun",
				"count":1
			},{
				"name":"土豆yangmi",
				"count":1
			}]
		}
		"""		
	When bill使用支付方式'微信支付'进行支付订单'003'于2016-10-03 10:01:00::apiserver

	Given zhouxun登录系统
	When zhouxun对出货单进行发货
		"""
		[{
			"delivery_item_bid":"001-zhouxun",
			"with_logistics":true,
			"with_logistics_trace":true,
			"express_company_name_value":"顺丰速运",
			"express_number":"147258369",
			"leader_name":"zhouxun|001",
			"time":"2016-10-05 10:11:00"
		},{
			"delivery_item_bid":"002-yangmi",
			"with_logistics":true,
			"with_logistics_trace":true,
			"express_company_name_value":"申通快递",
			"express_number":"147258367",
			"leader_name":"yangmi|002",
			"time":"2016-10-05 10:11:00"
		},{
			"delivery_item_bid":"003-zhouxun",
			"with_logistics":true,
			"with_logistics_trace":false,
			"express_company_name_value":"其他物流",
			"express_number":"147258366",
			"leader_name":"其他物流|003",
			"time":"2016-10-05 10:11:00"
		},{
			"delivery_item_bid":"003-yangmi",
			"with_logistics":true,
			"with_logistics_trace":false,
			"express_company_name_value":"其他物流",
			"express_number":"147258366",
			"leader_name":"其他物流|003",
			"time":"2016-10-05 10:11:00"
		}]
		"""

@order @ztqb
Scenario: 1 修改出货单物流信息
	Given zhouxun登录系统
	#修改普通物流公司信息为另一个普通物流公司信息
	When zhouxun修改出货单'001-zhouxun'物流信息
		"""
		{
			"with_logistics":true,
			"with_logistics_trace":true,
			"express_company_name_value":"申通快递",
			"express_number":"987654321",
			"leader_name":"zhouxun|001修改发货信息",
			"time":"2016-10-06 10:11:00"
		}
		"""
	Then zhouxun获得订单'001'
		"""
		{
			"bid":"001",
			"status_code": "shipped",
			"status_logs":[{
				"from_status_code":"",
				"to_status_code":"created",
				"time":"2016-10-01 10:00:00"
			},{
				"from_status_code":"created",
				"to_status_code":"paid",
				"time":"2016-10-01 10:01:00"
			},{
				"from_status_code":"paid",
				"to_status_code":"shipped",
				"time":"2016-10-05 10:11:00"
			}],
			"operation_logs":[{
				"action_text":"下单",
				"operator":"客户",
				"time":"2016-10-01 10:00:00"
			},{
				"action_text":"支付",
				"operator":"客户",
				"time":"2016-10-01 10:01:00"
			},{
				"action_text":"订单发货",
				"operator":"zhouxun",
				"time":"2016-10-05 10:11:00"
			}],
			"delivery_items": [{
				"bid": "001-zhouxun",
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "zhouxun"
				},
				"operation_logs":[{
					"action_text":"下单",
					"operator":"客户",
					"time":"2016-10-01 10:00:00"
				},{
					"action_text":"支付",
					"operator":"客户",
					"time":"2016-10-01 10:01:00"
				},{
					"action_text":"订单发货",
					"operator":"zhouxun",
					"time":"2016-10-05 10:11:00"
				},{
					"action_text":"修改发货信息",
					"operator":"zhouxun",
					"time":"2016-10-06 10:11:00"
				}],
				"products": [{
					"count": 1,
					"name": "东坡肘子zhouxun"
				}],
				"status_code": "shipped",
				"with_logistics":true,
				"with_logistics_trace":true,
				"express_company_name_text":"申通快递",
				"express_number": "987654321",
				"leader_name":"zhouxun|001修改发货信息"
			}]
		}
		"""
	#修改普通物流公司信息为其他物流公司信息
	When zhouxun修改出货单'002-yangmi'物流信息
		"""
		{
			"delivery_item_bid":"002-yangmi",
			"with_logistics":true,
			"with_logistics_trace":false,
			"express_company_name_value":"其他物流",
			"express_number":"123456789",
			"leader_name":"yangmi|002修改发货信息",
			"time":"2016-10-06 10:12:00"
		}
		"""
	Then zhouxun获得订单'002'
		"""
		{
			"bid":"002",
			"status_code": "paid",
			"status_logs":[{
				"from_status_code":"",
				"to_status_code":"created",
				"time":"2016-10-02 10:00:00"
			},{
				"from_status_code":"created",
				"to_status_code":"paid",
				"time":"2016-10-02 10:01:00"
			}],
			"operation_logs":[{
				"action_text":"下单",
				"operator":"客户",
				"time":"2016-10-02 10:00:00"
			},{
				"action_text":"支付",
				"operator":"客户",
				"time":"2016-10-02 10:01:00"
			}],
			"delivery_items": [{
				"bid": "002-zhouxun",
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "zhouxun"
				},
				"operation_logs":[{
					"action_text":"下单",
					"operator":"客户",
					"time":"2016-10-02 10:00:00"
				},{
					"action_text":"支付",
					"operator":"客户",
					"time":"2016-10-02 10:01:00"
				}],
				"products": [{
					"count": 1,
					"name": "东坡肘子zhouxun"
				}],
				"status_code": "paid",
				"with_logistics":false,
				"with_logistics_trace":true,
				"express_company_name_text":"",
				"express_number": "",
				"leader_name":""
			},{
				"bid": "001-yangmi",
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "yangmi"
				},
				"operation_logs":[{
					"action_text":"下单",
					"operator":"客户",
					"time":"2016-10-02 10:00:00"
				},{
					"action_text":"支付",
					"operator":"客户",
					"time":"2016-10-02 10:01:00"
				},{
					"action_text":"订单发货",
					"operator":"zhouxun",
					"time":"2016-10-05 10:11:00"
				},{
					"action_text":"修改发货信息",
					"operator":"zhouxun",
					"time":"2016-10-06 10:12:00"
				}],
				"products": [{
					"count": 1,
					"name": "土豆yangmi"
				}],
				"status_code": "shipped",
				"with_logistics":true,
				"with_logistics_trace":false,
				"express_company_name_text":"其他物流",
				"express_number": "123456789",
				"leader_name":"yangmi|002修改发货信息"
			}]
		}
		"""
	#修改其他物流公司信息为另一个其他物流公司信息
	When zhouxun修改出货单'003-zhouxun'物流信息
		"""
		{
			"delivery_item_bid":"003-zhouxun",
			"with_logistics":true,
			"with_logistics_trace":false,
			"express_company_name_value":"其他物流1",
			"express_number":"123456788",
			"leader_name":"其他物流|003修改发货信息",
			"time":"2016-10-06 10:13:00"
		}
		"""
	#修改其他物流公司信息为普通物流公司信息
	When zhouxun修改出货单'003-yangmi'物流信息
		"""
		{
			"delivery_item_bid":"003-yangmi",
			"with_logistics":true,
			"with_logistics_trace":true,
			"express_company_name_value":"顺丰速运",
			"express_number":"987654322",
			"leader_name":"其他物流|003修改发货信息",
			"time":"2016-10-06 10:14:00"
		}
		"""


	Then zhouxun获得订单'003'
		"""
		{
			"bid":"003",
			"status_code": "shipped",
			"status_logs":[{
				"from_status_code":"",
				"to_status_code":"created",
				"time":"2016-10-03 10:00:00"
			},{
				"from_status_code":"created",
				"to_status_code":"paid",
				"time":"2016-10-03 10:01:00"
			},{
				"from_status_code":"paid",
				"to_status_code":"shipped",
				"time":"2016-10-05 10:11:00"
			}],
			"operation_logs":[{
				"action_text":"下单",
				"operator":"客户",
				"time":"2016-10-03 10:00:00"
			},{
				"action_text":"支付",
				"operator":"客户",
				"time":"2016-10-03 10:01:00"
			},{
				"action_text":"订单发货",
				"operator":"zhouxun",
				"time":"2016-10-05 10:11:00"
			}],
			"delivery_items": [{
				"bid": "001-zhouxun",
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "zhouxun"
				},
				"operation_logs":[{
					"action_text":"下单",
					"operator":"客户",
					"time":"2016-10-03 10:00:00"
				},{
					"action_text":"支付",
					"operator":"客户",
					"time":"2016-10-03 10:01:00"
				},{
					"action_text":"订单发货",
					"operator":"zhouxun",
					"time":"2016-10-05 10:11:00"
				},{
					"action_text":"修改发货信息",
					"operator":"zhouxun",
					"time":"2016-10-06 10:13:00"
				}],
				"products": [{
					"count": 1,
					"name": "东坡肘子zhouxun"
				}],
				"status_code": "shipped",
				"with_logistics":true,
				"with_logistics_trace":false,
				"express_company_name_text":"其他物流1",
				"express_number": "123456788",
				"leader_name":"其他物流|003修改发货信息"
			},{
				"bid": "001-yangmi",
				"supplier_info": {
					"supplier_type": "supplier",
					"name": "yangmi"
				},
				"operation_logs":[{
					"action_text":"下单",
					"operator":"客户",
					"time":"2016-10-03 10:00:00"
				},{
					"action_text":"支付",
					"operator":"客户",
					"time":"2016-10-03 10:01:00"
				},{
					"action_text":"订单发货",
					"operator":"zhouxun",
					"time":"2016-10-05 10:11:00"
				},{
					"action_text":"修改发货信息",
					"operator":"zhouxun",
					"time":"2016-10-06 10:14:00"
				}],
				"products": [{
					"count": 1,
					"name": "土豆yangmi"
				}],
				"status_code": "shipped",
				"with_logistics":true,
				"with_logistics_trace":true,
				"express_company_name_text":"顺丰速运",
				"express_number": "987654322",
				"leader_name":"其他物流|003修改发货信息"
			}]
		}
		"""
