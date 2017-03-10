Feature: 更新会员等级


@gaia @member @member.grade
Scenario:更新会员等级
	更新会员等级后
	1. 会员等级列表中显示会员等级

	Given jobs登录系统
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
			"name": "金牌会员",
			"is_auto_upgrade": true,
			"shop_discount": 1,
			"pay_money": 1.23,
			"pay_times": 5
		}]
		"""
	When jobs更新会员等级'金牌会员'为
		"""
		{
			"name": "金牌会员*",
			"is_auto_upgrade": false,
			"shop_discount": 20,
			"pay_money": 3.21,
			"pay_times": 10
		}
		"""
	#更新后，内容发生变化
	Then jobs能获得会员等级列表
		"""
		[{
			"name": "普通会员",
			"is_auto_upgrade": true
		}, {
			"name": "金牌会员*",
			"is_auto_upgrade": false,
			"shop_discount": 20,
			"pay_money": 3.21,
			"pay_times": 10
		}]
		"""