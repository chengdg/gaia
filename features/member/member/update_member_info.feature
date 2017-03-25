Feature: 编辑用户详情信息

Background:
	Given jobs登录系统
	When jobs创建会员分组
		"""
		[{
			"name": "分组1"
		}, {
			"name": "分组2"
		}, {
			"name": "分组3"
		}, {
			"name": "分组4"
		}]
		"""
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


@gaia @member
Scenario: 编辑会员信息
	编辑会员信息后
	1. 能获得更新后的会员信息

	Given jobs登录系统
	Then jobs能获得会员'zhouxun'的信息
		"""
		{
			"sex": "unknown",
			"phone_number": "",
			"remark_name": "zhouxun",
			"remark": "",
			"name": "zhouxun",
			"groups": ["未分组"],
			"grade": {
				"name": "普通会员"
			},
			"integral": 0
		}
		"""
	Then jobs能获得会员'yangmi'的信息
		"""
		{
			"sex": "unknown",
			"phone_number": "",
			"remark_name": "yangmi",
			"remark": "",
			"name": "yangmi",
			"groups": ["未分组"],
			"grade": {
				"name": "普通会员"
			},
			"integral": 0
		}
		"""
	When jobs更新会员'zhouxun'的信息
		"""
		{
			"sex": "male",
			"remark_name": "周迅",
			"remark": "周迅的备注信息",
			"integral_increment": {
				"integral_increment": 90,
				"reason": "测试加"
			},
			"grade": "金牌会员",
			"groups": ["分组2", "分组4"],
			"phone_number": "13811223344"
		}
		"""
	Then jobs能获得会员'zhouxun'的信息
		"""
		{
			"sex": "male",
			"phone_number": "13811223344",
			"remark_name": "周迅",
			"remark": "周迅的备注信息",
			"name": "zhouxun",
			"groups": ["分组2", "分组4"],
			"grade": {
				"name": "金牌会员"
			},
			"integral": 90
		}
		"""
	Then jobs能获得会员'yangmi'的信息
		"""
		{
			"sex": "unknown",
			"phone_number": "",
			"remark_name": "yangmi",
			"remark": "",
			"name": "yangmi",
			"groups": ["未分组"],
			"grade": {
				"name": "普通会员"
			},
			"integral": 0
		}
		"""
	Then jobs能获得会员'zhouxun'的积分日志
		"""
		[{
			"event": "manager_modify_increase",
			"integral_increment": 90,
			"current_integral": 90,
			"actor": "jobs",
			"reason": "测试加"
		}]
		"""
	