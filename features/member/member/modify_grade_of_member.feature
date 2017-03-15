Feature: 手动修改会员的等级

Background:
	Given jobs登录系统
	When jobs创建会员等级
		"""
		[{
			"name": "银牌会员",
			"shop_discount": 90
		}, {
			"name": "金牌会员",
			"pay_times": 70
		}]
		"""
	Given zhouxun成为'jobs'的会员
	Given yangmi成为'jobs'的会员
	Given yaochen成为'jobs'的会员


@gaia @member @member.group
Scenario: 修改会员的等级
	将会员的等级信息手工修改后
	1. 会员信息中携带修改后的等级信息

	Given jobs登录系统
	Then jobs能获得会员'zhouxun'的信息
		"""
		{
			"name": "zhouxun",
			"grade": {
				"name": "普通会员"
			}
		}
		"""
	Then jobs能获得会员'yangmi'的信息
		"""
		{
			"name": "yangmi",
			"grade": {
				"name": "普通会员"
			}
		}
		"""
	Then jobs能获得会员'yaochen'的信息
		"""
		{
			"name": "yaochen",
			"grade": {
				"name": "普通会员"
			}
		}
		"""
	When jobs批量调整会员的等级为'银牌会员'
		"""
		["zhouxun", "yangmi"]
		"""
	Then jobs能获得会员'zhouxun'的信息
		"""
		{
			"name": "zhouxun",
			"grade": {
				"name": "银牌会员"
			}
		}
		"""
	Then jobs能获得会员'yangmi'的信息
		"""
		{
			"name": "yangmi",
			"grade": {
				"name": "银牌会员"
			}
		}
		"""
	Then jobs能获得会员'yaochen'的信息
		"""
		{
			"name": "yaochen",
			"grade": {
				"name": "普通会员"
			}
		}
		"""