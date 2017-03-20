Feature: 删除会员等级


@gaia @member @member.grade
Scenario:删除会员等级
	更新会员等级后
	1. 会员等级列表中不再出现该会员等级
	2. TODO: 该等级的会员重新分配等级

	Given jobs登录系统
	When jobs创建会员等级
		"""
		[{
			"name": "铜牌会员"
		}, {
			"name": "银牌会员"
		}, {
			"name": "金牌会员"
		}]
		"""
	Then jobs能获得会员等级列表
		"""
		[{
			"name": "普通会员"
		}, {
			"name": "铜牌会员"
		}, {
			"name": "银牌会员"
		}, {
			"name": "金牌会员"
		}]
		"""
	When jobs删除会员等级'银牌会员'
	Then jobs能获得会员等级列表
		"""
		[{
			"name": "普通会员"
		}, {
			"name": "铜牌会员"
		}, {
			"name": "金牌会员"
		}]
		"""

@gaia @member @member.grade @todo
Scenario:删除会员等级，影响限时抢购促销
	删除会员等级后
	1. 设置了该等级的限时抢购活动自动结束
	2. 设置了其他等级的限时抢购活动不受影响

	Given jobs登录系统
	When jobs创建会员等级
		"""
		[{
			"name": "铜牌会员"
		}, {
			"name": "银牌会员"
		}, {
			"name": "金牌会员"
		}]
		"""

@gaia @member @member.grade @todo
Scenario:删除会员等级，影响积分应用促销
	删除会员等级后
	1. 设置了该等级的积分应用活动自动结束
	2. 设置了其他等级的积分应用活动不受影响

	Given jobs登录系统
	When jobs创建会员等级
		"""
		[{
			"name": "铜牌会员"
		}, {
			"name": "银牌会员"
		}, {
			"name": "金牌会员"
		}]
		"""