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


@gaia @member @member.group
Scenario: 将会员加入会员分组
	将会员加入分组后
	1. 会员信息中携带分组信息
	2. 分组中的会员数量发生更新

	Given jobs登录系统
	Then jobs能获得会员'zhouxun'的信息
		"""
		{
			"name": "zhouxun",
			"groups": ["未分组"]
		}
		"""
	Then jobs能获得会员分组列表
		"""
		[{
			"name": "未分组",
			"member_count": 1
		}, {
			"name": "分组1",
			"member_count": 0
		}, {
			"name": "分组2",
			"member_count": 0
		}, {
			"name": "分组3",
			"member_count": 0
		}, {
			"name": "分组4",
			"member_count": 0
		}]
		"""
	When jobs改变会员'zhouxun'的分组为
		"""
		["分组1", "分组3"]
		"""
	Then jobs能获得会员'zhouxun'的信息
		"""
		{
			"name": "zhouxun",
			"groups": ["分组1", "分组3"]
		}
		"""
	Then jobs能获得会员分组列表
		"""
		[{
			"name": "未分组",
			"member_count": 0
		}, {
			"name": "分组1",
			"member_count": 1
		}, {
			"name": "分组2",
			"member_count": 0
		}, {
			"name": "分组3",
			"member_count": 1
		}, {
			"name": "分组4",
			"member_count": 0
		}]
		"""
	#验证：删除所有分组后，回到'未分组'分组
	When jobs改变会员'zhouxun'的分组为
		"""
		[]
		"""
	When jobs改变会员'zhouxun'的分组为
		"""
		["未分组"]
		"""
	Then jobs能获得会员分组列表
		"""
		[{
			"name": "未分组",
			"member_count": 1
		}, {
			"name": "分组1",
			"member_count": 0
		}, {
			"name": "分组2",
			"member_count": 0
		}, {
			"name": "分组3",
			"member_count": 0
		}, {
			"name": "分组4",
			"member_count": 0
		}]
		"""
	