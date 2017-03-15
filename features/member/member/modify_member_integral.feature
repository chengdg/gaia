Feature: 手动调整会员的积分

Background:
	Given jobs登录系统
	Given zhouxun成为'jobs'的会员
	Given yangmi成为'jobs'的会员
	Given yaochen成为'jobs'的会员


@gaia @member @member.group
Scenario: 调整会员的积分
	调整会员积分后
	1. 会员信息中携带修改后的积分
	2. 能获得会员积分的日志

	Given jobs登录系统
	Then jobs能获得会员'zhouxun'的信息
		"""
		{
			"name": "zhouxun",
			"integral": 0
		}
		"""
	When jobs为会员'zhouxun'增加积分'90'
	Then jobs能获得会员'zhouxun'的信息
		"""
		{
			"name": "zhouxun",
			"integral": 90
		}
		"""
	When jobs为会员'zhouxun'增加积分'-30'
		"""
		{
			"reason": "测试减"
		}
		"""
	Then jobs能获得会员'zhouxun'的信息
		"""
		{
			"name": "zhouxun",
			"integral": 60
		}
		"""
	Then jobs能获得会员'zhouxun'的积分日志
		"""
		[{
			"event": "manager_modify_decrease",
			"integral_increment": -30,
			"current_integral": 60,
			"actor": "jobs",
			"reason": "测试减"
		}, {
			"event": "manager_modify_increase",
			"integral_increment": 90,
			"current_integral": 90,
			"actor": "jobs",
			"reason": ""
		}]
		"""