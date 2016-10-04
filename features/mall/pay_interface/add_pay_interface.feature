Feature:添加支付方式
	Jobs能通过管理系统添加"支付方式"

@mall @mall.pay_interface @hermes
Scenario:1 添加支付方式:微信支付 v3
	
	Given jobs登录系统
	When jobs添加支付方式
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
	Then jobs能获得支付方式
		"""
		{
			"type": "微信支付",
			"is_active": "启用",
			"weixin_appid": "app_id_1",
			"mch_id": "mch_id_1",
			"api_key": "api_key_1",
			"paysign_key": "paysign_key_1"
		}
		"""
	Given bill登录系统
	Then bill能获得支付方式
		"""
		{
			"type": "微信支付",
			"is_active": "停用"
		}
		"""

@mall @mall.pay_interface @hermes @wip
Scenario:2 添加支付方式:支付宝支付
	
	Given jobs登录系统
	When jobs添加支付方式
		"""
		[{
			"type": "支付宝",
			"is_active": "启用",
			"partner": "11",
			"key": "21",
			"ali_public_key": "31",
			"private_key": "41",
			"seller_email": "a@a.com"
		}]
		"""
	Then jobs能获得支付方式
		"""
		{
			"type": "支付宝",
			"is_active": "启用",
			"partner": "11",
			"key": "21",
			"ali_public_key": "31",
			"private_key": "41",
			"seller_email": "a@a.com"
		}
		"""
	Given bill登录系统
	Then bill能获得支付方式
		"""
		{
			"type": "支付宝",
			"is_active": "停用"
		}
		"""

@mall @mall.pay_interface @hermes
Scenario:3 添加支付方式:货到付款

	Given jobs登录系统
	When jobs添加支付方式
		"""
		[{
			"type": "货到付款",
			"is_active": "启用"
		}]
		"""
	Then jobs能获得支付方式
		"""
		{
			"type": "货到付款",
			"is_active": "启用"
		}
		"""
	Given bill登录系统
	Then bill能获得支付方式
		"""
		{
			"type": "货到付款",
			"is_active": "停用"
		}
		"""

@mall @mall.pay_interface @hermes
Scenario:4 获得多个支付方式，改变支付接口启用状态

	Given jobs登录系统
	Then jobs能获得支付方式列表
		"""
		[{
			"type": "微信支付"
		}, {
			"type": "货到付款"
		},{
			"type": "支付宝"
		}]
		"""
	Given bill登录系统
	Then bill能获得支付方式列表
		"""
		[{
			"type": "微信支付",
			"is_active": "停用"
		}, {
			"type": "货到付款",
			"is_active": "停用"
		},{
			"type": "支付宝",
			"is_active": "停用"
		}]
		"""
	Given jobs登录系统
	When jobs'启用'支付方式'微信支付'
	Then jobs能获得支付方式列表
		"""
		[{
			"type": "微信支付",
			"is_active": "启用"
		}, {
			"type": "货到付款",
			"is_active": "停用"
		},{
			"type": "支付宝",
			"is_active": "停用"
		}]
		"""
	When jobs'停用'支付方式'微信支付'
	Then jobs能获得支付方式列表
		"""
		[{
			"type": "微信支付",
			"is_active": "停用"
		}, {
			"type": "货到付款",
			"is_active": "停用"
		},{
			"type": "支付宝",
			"is_active": "停用"
		}]
		"""

