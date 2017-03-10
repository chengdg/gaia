Feature: 删除会员等级


@gaia @member @member.grade
Scenario:删除会员等级
	更新会员等级后
	1. 会员等级列表中不再出现该会员等级

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