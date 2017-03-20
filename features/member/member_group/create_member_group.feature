Feature: 创建会员分组

Background:
	Given jobs登录系统


@gaia @member @member.group
Scenario:创建会员分组
	创建会员分组
	1. 会员分组列表中显示会员分组，会员分组按顺序排列

	Given jobs登录系统
	When jobs创建会员分组
		"""
		{
			"name": "分组1"
		}
		"""
	When jobs创建会员分组
		"""
		{
			"name": "分组2"
		}
		"""
	Then jobs能获得会员分组列表
		"""
		[{
			"name": "未分组",
			"member_count": 0
		}, {
			"name": "分组1",
			"member_count": 0
		}, {
			"name": "分组2",
			"member_count": 0
		}]
		"""
	