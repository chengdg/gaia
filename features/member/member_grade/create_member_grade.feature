Feature: 创建会员等级

Background:
	Given jobs登录系统


@gaia @member @member.grade
Scenario:创建会员等级
	创建会员等级后
	1. 会员等级列表中显示会员等级，会员等级按顺序排列

	Given jobs登录系统
	When jobs创建会员等级
		"""
		{
			"name": "银牌会员",
			"is_auto_upgrade": false,
			"shop_discount": 3
		}
		"""
	When jobs创建会员等级
		"""
		{
			"name": "金牌会员",
			"is_auto_upgrade": true,
			"shop_discount": 1,
			"pay_money": 1.23,
			"pay_times": 5
		}
		"""
	Then jobs能获得会员等级列表
		"""
		[{
			"name": "普通会员",
			"is_auto_upgrade": true
		}, {
			"name": "银牌会员",
			"is_auto_upgrade": false,
			"shop_discount": 3	
		}, {
			"name": "金牌会员",
			"is_auto_upgrade": true,
			"shop_discount": 1,
			"pay_money": 1.23,
			"pay_times": 5
		}]
		"""