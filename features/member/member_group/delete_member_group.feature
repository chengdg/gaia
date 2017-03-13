Feature: 删除会员分组

@gaia @member @member.group
Scenario:删除会员分组影响会员分组列表
	删除会员分组后
	1. 会员分组列表中该会员分组消失

	Given jobs登录系统
	When jobs创建会员分组
		"""
		[{
			"name": "分组1"
		}, {
			"name": "分组2"
		}]
		"""
	When jobs删除会员分组'分组2'
	Then jobs能获得会员分组列表
		"""
		[{
			"name": "未分组",
			"member_count": 0
		}, {
			"name": "分组1",
			"member_count": 0
		}]
		"""

@gaia @member @member.group @wip
Scenario:删除会员分组影响已分组的会员
	删除会员分组后
	1. 如果会员的部分分组被删除，会员分组信息正常改变
	2. 如果会员的全部分组被删除，会员回到“未分组”分组

	Given jobs登录系统
	Given zhouxun成为'jobs'的会员
	When jobs创建会员分组
		"""
		[{
			"name": "分组1"
		}, {
			"name": "分组2"
		}]
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
		}]
		"""
	When jobs改变会员'zhouxun'的分组为
		"""
		["分组1", "分组2"]
		"""
	Then jobs能获得会员'zhouxun'的信息
		"""
		{
			"name": "zhouxun",
			"groups": ["分组1", "分组2"]
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
			"member_count": 1
		}]
		"""
	#删除会员的部分分组
	When jobs删除会员分组'分组2'
	Then jobs能获得会员'zhouxun'的信息
		"""
		{
			"name": "zhouxun",
			"groups": ["分组1"]
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
		}]
		"""
	#删除会员的全部分组
	When jobs删除会员分组'分组1'
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
		}]
		"""