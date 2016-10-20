Feature: 添加供应商

@mall @mall.product @mall.supplier @hermes
Scenario:1 添加供应商
	Jobs添加一组"供应商"后，能获得供应商列表

	Given jobs登录系统
	When jobs添加供应商
		"""
		[{
			"name": "苹果公司",
			"responsible_person": "乔布斯",
			"supplier_tel": "13811111111",
			"supplier_address": "苹果公司的地址"
		}, {
			"name": "微软",
			"type": "首月55分成",
			"responsible_person": "盖茨",
			"supplier_tel": "13822222222",
			"supplier_address": "微软的地址",
			"divide_info": {
				"divide_money": 1.0,
				"basic_rebate": 20,
				"rebate": 30
			}
		}, {
			"name": "谷歌",
			"type": "零售返点",
			"responsible_person": "谷歌老板",
			"supplier_tel": "13833333333",
			"supplier_address": "谷歌的地址",
			"retail_info": {
				"rebate": 50
			}
		}, {
			"name": "amazon",
			"type": "固定低价"
		}]
		"""
	Then jobs能获取供应商列表
		"""
		[{
			"name": "苹果公司",
			"responsible_person": "乔布斯",
			"supplier_tel": "13811111111",
			"supplier_address": "苹果公司的地址"
		}, {
			"name": "微软",
			"type": "首月55分成",
			"responsible_person": "盖茨",
			"supplier_tel": "13822222222",
			"supplier_address": "微软的地址",
			"divide_info": {
				"divide_money": 1.0,
				"basic_rebate": 20,
				"rebate": 30
			}
		}, {
			"name": "谷歌",
			"type": "零售返点",
			"responsible_person": "谷歌老板",
			"supplier_tel": "13833333333",
			"supplier_address": "谷歌的地址",
			"retail_info": {
				"rebate": 50
			}
		}, {
			"name": "amazon",
			"type": "固定低价"
		}]
		"""
	Given bill登录系统
	Then bill能获取供应商列表
		"""
		[]
		"""
