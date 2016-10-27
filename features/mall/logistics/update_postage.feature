#author: 冯雪静
#editor: 张三香 2015.10.16

Feature:更新运费配置
	Jobs能通过管理系统为管理商城更新已添加的"邮费配置"

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

@gaia @mall @mall.logistics @hermes
Scenario:1 更新邮费配置
	Jobs更新"邮费配置"
	修改策略为：
		顺丰：修改name，修改default_config，添加special_config
		圆通：删除special config，增加free config
	1. jobs能获得更新后的邮费配置

	Given jobs登录系统
	Then jobs能获取'顺丰'运费配置
		"""
		{
			"name" : "顺丰",
			"is_enable_special_config": false,
			"is_enable_free_config": false
		}	
		"""
	Then jobs能获取'圆通'运费配置
		"""
		{
			"name" : "圆通",
			"is_enable_special_config": true,
			"is_enable_free_config": false
		}	
		"""
	When jobs修改'顺丰'运费配置
		"""
		{
			"name" : "顺丰1",
			"first_weight":2,
			"first_weight_price":25.00,
			"added_weight":3,
			"added_weight_price":35.00,
			"special_area": [{
				"to_the":"北京市",
				"first_weight_price":20.00,
				"added_weight_price":10.00
			},{
				"to_the":"上海市,重庆市,江苏省",
				"first_weight_price":30.00,
				"added_weight_price":20.00
			}]
		}
		"""
	When jobs修改'圆通'运费配置
		"""
		{
			"name" : "圆通",
			"first_weight":1,
			"first_weight_price":10.00,
			"free_postages": [{
				"to_the": "上海市",
				"condition": "count",
				"value": 1
			},{
				"to_the": "北京市,重庆市,江苏省",
				"condition": "money",
				"value": 2.0
			}]
		}
		"""
	Then jobs能获取'顺丰1'运费配置
		"""
		{
			"name" : "顺丰1",
			"first_weight":2,
			"first_weight_price":25.00,
			"added_weight":3,
			"added_weight_price":35.00,
			"special_area": [{
				"to_the":"北京市",
				"first_weight_price":20.00,
				"added_weight_price":10.00
			},{
				"to_the":"上海市,重庆市,江苏省",
				"first_weight_price":30.00,
				"added_weight_price":20.00
			}],
			"is_enable_special_config": true,
			"is_enable_free_config": false
		}	
		"""
	And jobs能获取'圆通'运费配置
		"""
		{
			"name" : "圆通",
			"first_weight":1,
			"first_weight_price":10.00,
			"free_postages": [{
				"to_the": "上海市",
				"condition": "count",
				"value": 1
			},{
				"to_the": "北京市,重庆市,江苏省",
				"condition": "money",
				"value": 2.0
			}],
			"is_enable_special_config": false,
			"is_enable_free_config": true
		}	
		"""

