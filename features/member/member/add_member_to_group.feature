Feature: 将会员加入会员分组

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
	Given zhouxun成为'jobs'的会员


@gaia @member @member.group @wip
Scenario: 将会员加入会员分组
	将会员加入分组后
	1. 会员信息中携带分组信息
	2. 分组中的会员数量发生更新

	Given jobs登录系统
	Then jobs能获得会员'zhouxun'的信息
		"""
		{
			"name": "zhouxun"
		}
		"""
	
	