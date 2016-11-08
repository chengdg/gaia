Feature:选择运费配置

Background:
	Given jobs登录系统 
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

@gaia @mall @mall.logistics
Scenario:1 选择邮费配置
	Jobs选择"邮费配置"
	1. jobs能获得更新后的邮费配置

	Given jobs登录系统
	Then jobs能获取邮费配置列表
		"""
		[{
			"name": "免运费",
			"is_used": true
		},{
			"name": "顺丰",
			"is_used": false
		},{
			"name": "圆通",
			"is_used": false
		}]
		"""
	When jobs选择'顺丰'运费配置
	Then jobs能获取邮费配置列表
		"""
		[{
			"name": "免运费",
			"is_used": false
		},{
			"name": "顺丰",
			"is_used": true
		},{
			"name": "圆通",
			"is_used": false
		}]
		"""

