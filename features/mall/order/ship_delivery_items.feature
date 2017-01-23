Feature: 对出货单进行发货
	"""
		zhouxun能为用户出货单进行发货
		1 对出货单进行发货，使用物流（非其他）
		2 对出货单进行发货，使用其他物流
		3 对出货单进行发货，不使用物流
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

@order
Scenario: 1 对出货单进行发货，使用物流（非其他）
	Given zhouxun登录系统
	When zhouxun对出货单进行发货
		"""
		[{
			"delivery_item_bid":"001-zhouxun",
			"with_logistics":true,
			"with_logistics_trace":true,
			"express_company_name_text_value":"顺丰速运",
			"express_number":"147258369",
			"leader_name":"zhouxun|001",
			"time":"2016-10-05 10:11:00"
		},{
			"delivery_item_bid":"002-zhouxun",
			"with_logistics":true,
			"with_logistics_trace":true,
			"express_company_name_text_value":"申通快递",
			"express_number":"147258368",
			"leader_name":"zhouxun|002-1",
			"time":"2016-10-05 10:11:00"
		},{
			"delivery_item_bid":"002-yangmi",
			"with_logistics":true,
			"with_logistics_trace":true,
			"express_company_name_text_value":"申通快递",
			"express_number":"147258367",
			"leader_name":"yangmi",
			"time":"2016-10-05 10:11:00"
		},{
			"delivery_item_bid":"003-zhouxun",
			"with_logistics":true,
			"with_logistics_trace":true,
			"express_company_name_text_value":"圆通速递",
			"express_number":"147258366",
			"leader_name":"",
			"time":"2016-10-05 10:11:00"
		}]
		"""

	Then zhouxun获得订单列表
	"""
	[{
		"bid":"003",
		"status_code": "paid",
		"delivery_items": [{
			"supplier_info": {
				"supplier_type": "supplier",
				"name": "zhouxun"
			},
			"products": [{
				"count": 1,
				"name": "东坡肘子zhouxun"
			}],
			"status_code": "shipped",
			"with_logistics":true,
			"with_logistics_trace":true,
			"express_company_name_text": "圆通速递",
			"express_number": "147258366",
			"leader_name":""
		},{
			"supplier_info": {
				"supplier_type": "supplier",
				"name": "yangmi"
			},
			"products": [{
				"count": 1,
				"name": "土豆yangmi"
			}],
			"status_code": "paid",
			"with_logistics":false,
			"with_logistics_trace":false,
			"express_company_name_text": "",
			"express_number": "",
			"leader_name":""
		}]
	},{
		"bid":"002",
		"status_code": "shipped",
		"delivery_items": [{
			"supplier_info": {
				"supplier_type": "supplier",
				"name": "zhouxun"
			},
			"products": [{
				"count": 1,
				"name": "东坡肘子zhouxun"
			}],
			"status_code": "shipped",
			"with_logistics":true,
			"with_logistics_trace":true,
			"express_company_name_text": "申通快递",
			"express_number": "147258368",
			"leader_name":"zhouxun|002-1"
		},{
			"supplier_info": {
				"supplier_type": "supplier",
				"name": "yangmi"
			},
			"products": [{
				"count": 1,
				"name": "土豆yangmi"
			}],
			"status_code": "shipped",
			"with_logistics":true,
			"with_logistics_trace":true,
			"express_company_name_text": "申通快递",
			"express_number": "147258367",
			"leader_name":"yangmi"
		}]
	},{
		"bid":"001",
		"status_code": "shipped",
		"delivery_items": [{
			"supplier_info": {
				"supplier_type": "supplier",
				"name": "zhouxun"
			},
			"products": [{
				"count": 1,
				"name": "东坡肘子zhouxun"
			}],
			"status_code": "shipped",
			"with_logistics":true,
			"with_logistics_trace":true,
			"express_company_name_text": "顺丰速运",
			"express_number": "147258369",
			"leader_name":"zhouxun|001"
		}]
	}]
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
			"supplier_info": {
				"supplier_type": "supplier",
				"name": "zhouxun"
			},
			"products": [{
				"count": 1,
				"name": "东坡肘子zhouxun"
			}],
			"status_code": "shipped",
			"with_logistics":true,
			"with_logistics_trace":true,
			"express_company_name_text": "顺丰速运",
			"express_number": "147258369",
			"leader_name":"zhouxun|001"
		}]
	}
	"""
	Then zhouxun获得订单'002'
	"""
	{
		"bid":"002",
		"status_code": "shipped",
		"status_logs":[{
			"from_status_code":"",
			"to_status_code":"created",
			"time":"2016-10-02 10:00:00"
		},{
			"from_status_code":"created",
			"to_status_code":"paid",
			"time":"2016-10-02 10:01:00"
		},{
			"from_status_code":"paid",
			"to_status_code":"shipped",
			"time":"2016-10-05 10:11:00"
		}],
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
			"action_text":"订单发货",
			"operator":"zhouxun",
			"time":"2016-10-05 10:11:00"
		}],
		"delivery_items": [{
			"supplier_info": {
				"supplier_type": "supplier",
				"name": "zhouxun"
			},
			"products": [{
				"count": 1,
				"name": "东坡肘子zhouxun"
			}],
			"status_code": "shipped",
			"with_logistics":true,
			"with_logistics_trace":true,
			"express_company_name_text": "申通快递",
			"express_number": "147258368",
			"leader_name":"zhouxun|002-1"
		},{
			"supplier_info": {
				"supplier_type": "supplier",
				"name": "yangmi"
			},
			"products": [{
				"count": 1,
				"name": "土豆yangmi"
			}],
			"status_code": "shipped",
			"with_logistics":true,
			"with_logistics_trace":true,
			"express_company_name_text": "申通快递",
			"express_number": "147258367",
			"leader_name":"yangmi"
		}]
	}
	"""
	Then zhouxun获得订单'003'
	"""
	{
		"bid":"003",
		"status_code": "paid",
		"status_logs":[{
			"from_status_code":"",
			"to_status_code":"created",
			"time":"2016-10-03 10:00:00"
		},{
			"from_status_code":"created",
			"to_status_code":"paid",
			"time":"2016-10-03 10:01:00"
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
			"supplier_info": {
				"supplier_type": "supplier",
				"name": "zhouxun"
			},
			"products": [{
				"count": 1,
				"name": "东坡肘子zhouxun"
			}],
			"status_code": "shipped",
			"with_logistics":true,
			"with_logistics_trace":true,
			"express_company_name_text": "圆通速递",
			"express_number": "147258366",
			"leader_name":""
		},{
			"supplier_info": {
				"supplier_type": "supplier",
				"name": "yangmi"
			},
			"products": [{
				"count": 1,
				"name": "土豆yangmi"
			}],
			"status_code": "paid",
			"with_logistics":false,
			"with_logistics_trace":false,
			"express_company_name_text": "",
			"express_number": "",
			"leader_name":""
		}]
	}
	"""

@order
Scenario: 2 对出货单进行发货，使用其他物流
	Given zhouxun登录系统
	When zhouxun对出货单进行发货
		"""
		[{
			"delivery_item_bid":"001-zhouxun",
			"with_logistics":true,
			"with_logistics_trace":false,
			"express_company_name_text_value":"其他物流",
			"express_number":"138123456",
			"leader_name":"其他物流|001",
			"time":"2016-10-05 10:11:00"
		}]
		"""
	Then zhouxun获得订单列表
	"""
	[{
		"bid":"001",
		"status_code": "shipped",
		"delivery_items": [{
			"supplier_info": {
				"supplier_type": "supplier",
				"name": "zhouxun"
			},
			"products": [{
				"count": 1,
				"name": "东坡肘子zhouxun"
			}],
			"status_code": "shipped"
		}]
	}]
	"""
	Then zhouxun获得订单'001'
	"""
	{
		"bid":"001",
		"status_code": "shipped",
		"status_logs":[{
			"from_status_code":"",
			"to_status_code":"created",
			"time":"2016-10-01 10:00:00",
		},{
			"from_status_code":"created",
			"to_status_code":"paid",
			"time":"2016-10-01 10:01:00",
		},{
			"from_status_code":"paid",
			"to_status_code":"shipped",
			"time":"2016-10-05 10:11:00",
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
			"action_text":"订单发货-zhouxun",
			"operator":"zhouxun",
			"time":"2016-10-05 10:11:00"
		}],
		"delivery_items": [{
			"supplier_info": {
				"supplier_type": "supplier",
				"name": "zhouxun"
			},
			"products": [{
				"count": 1,
				"name": "东坡肘子zhouxun"
			}],
			"express_company_name_text_text":"其他物流",
			"express_number": "138123456",
			"leader_name":"其他物流|001"
		}]
	}
	"""

@order
Scenario: 3 对出货单进行发货，不使用物流
	Given zhouxun登录系统
	When zhouxun对出货单进行发货
		"""
		[{
			"delivery_item_bid":"002-zhouxun",
			"with_logistics":false,
			"with_logistics_trace":false,
			"express_company_name_text_value":"",
			"express_number":"",
			"leader_name":"zhouxun|002-1",
			"time":"2016-10-05 10:11:00"
		},{
			"delivery_item_bid":"002-yangmi",
			"with_logistics":false,
			"with_logistics_trace":false,
			"express_company_name_text_value":"",
			"express_number":"",
			"leader_name":"",
			"time":"2016-10-05 10:11:00"
		}]
		"""

	Then zhouxun获得订单列表
	"""
	[{
		"bid":"002",
		"status_code": "shipped",
		"delivery_items": [{
			"supplier_info": {
				"supplier_type": "supplier",
				"name": "zhouxun"
			},
			"products": [{
				"count": 1,
				"name": "东坡肘子zhouxun"
			}],
			"status_code": "shipped"
		},{
			"supplier_info": {
				"supplier_type": "supplier",
				"name": "yangmi"
			},
			"products": [{
				"count": 1,
				"name": "土豆yangmi"
			}],
			"status_code": "shipped"
		}]
	}]
	"""

	Then zhouxun获得订单'002'
	"""
	{
		"bid":"002",
		"status_code": "shipped",
		"status_logs":[{
			"from_status_code":"",
			"to_status_code":"created",
			"time":"2016-10-02 10:00:00",
		},{
			"from_status_code":"created",
			"to_status_code":"paid",
			"time":"2016-10-02 10:01:00",
		},{
			"from_status_code":"paid",
			"to_status_code":"shipped",
			"time":"2016-10-05 10:11:00",
		}],
		"operation_logs":[{
			"action_text":"下单",
			"operator":"客户",
			"time":"2016-10-02 10:00:00"
		},{
			"action_text":"支付",
			"operator":"客户",
			"time":"2016-10-02 10:01:00"
		},{
			"action_text":"订单发货-zhouxun",
			"operator":"zhouxun",
			"time":"2016-10-05 10:11:00"
		},{
			"action_text":"订单发货-yangmi",
			"operator":"zhouxun",
			"time":"2016-10-05 10:11:00"
		}],
		"delivery_items": [{
			"supplier_info": {
				"supplier_type": "supplier",
				"name": "zhouxun"
			},
			"products": [{
				"count": 1,
				"name": "东坡肘子zhouxun"
			}],
			"status_code": "shipped",
			"express_company_name_text_text":"",
			"express_number": "",
			"leader_name":"zhouxun|002-1"
		},{
			"supplier_info": {
				"supplier_type": "supplier",
				"name": "yangmi"
			},
			"products": [{
				"count": 1,
				"name": "土豆yangmi"
			}],
			"status_code": "shipped",
			"express_company_name_text_text":"",
			"express_number": "",
			"leader_name":""
		}]
	}
	"""
