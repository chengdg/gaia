Feature: 更新会员升级策略


@gaia @member @member.grade
Scenario: 更新会员升级策略
	更新会员升级策略后
	1. 全局会员升级策略改变
	2. 会员等级中的会员升级策略改变

	Given jobs登录系统
	When jobs创建会员等级
		"""
		{
			"name": "金牌会员"
		}
		"""
	When jobs更新会员升级策略为'满足全部条件'
	Then jobs能获得会员升级策略为'满足全部条件'
	Then jobs能获得会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade_strategy": "match_all"
		}, {
			"name": "金牌会员",
			"upgrade_strategy": "match_all"
		}]
		"""
	When jobs更新会员升级策略为'满足任一条件'
	Then jobs能获得会员升级策略为'满足任一条件'
	Then jobs能获得会员等级列表
		"""
		[{
			"name": "普通会员",
			"upgrade_strategy": "match_any"
		}, {
			"name": "金牌会员",
			"upgrade_strategy": "match_any"
		}]
		"""