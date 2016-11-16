Feature: 添加邮费配置
	Jobs能通过管理系统为商城添加的"邮费配置"

@gaia @mall @mall.logistics
Scenario:1 添加邮费配置
	Jobs添加"邮费配置"
	1. jobs能获得邮费配置列表

	Given jobs登录系统
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
	Then jobs能获取邮费配置列表
		"""
		[{
			"name": "免运费",
			"postage_items":[{
				"to_the":"全国",
				"first_weight": 0.0,
				"first_weight_price": 0.00,
				"added_weight": 0.0,
				"added_weight_price": 0.00
			}]
		},{
			"name": "圆通",
			"is_enable_free_config": false,
			"is_enable_special_config": false,
			"postage_items":[{
				"to_the":"全国",
				"first_weight": 40.0,
				"first_weight_price": 4.00,
				"added_weight": 1.0,
				"added_weight_price": 6.00
			}]			
		},{
			"name": "顺丰",
			"postage_items":[{
				"to_the":"全国",
				"first_weight": 41.0,
				"first_weight_price": 5.00,
				"added_weight": 0.0,
				"added_weight_price": 0.00
			}]
		},{
			"name": "EMS",
			"is_enable_free_config": false,
			"is_enable_special_config": true,
			"postage_items": [{
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
			},{
				"to_the": "其他地区",
				"first_weight": 1.0,
				"first_weight_price": 15.00,
				"added_weight": 1.0,
				"added_weight_price": 5.00
			}]
		},{
			"name": "韵达",
			"is_enable_free_config": true,
			"is_enable_special_config": false,
			"postage_items":[{
				"to_the":"全国",
				"first_weight": 1.0,
				"first_weight_price": 12.00,
				"added_weight": 1.0,
				"added_weight_price": 2.00
			}]
		}]
		"""
