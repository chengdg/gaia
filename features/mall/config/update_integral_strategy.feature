Feature: 更新积分规则

Background:
	Given jobs登录系统

@gaia @mall @mall.config
Scenario:1 更新积分规则
	When jobs更新积分规则为
		"""
		{
			"integral_each_yuan": 1,
			"be_member_increase_count": 2,
			"buy_award_count_for_buyer": 4,
			"order_money_percentage_for_each_buy": 3.14,
			"buy_via_offline_increase_count_for_author": 6,
			"buy_via_offline_increase_count_percentage_for_author": 4.14,
			"use_ceiling": 20,
			"review_increase": 7
		}
		"""
	Then jobs能获得积分规则
		"""
		{
			"integral_each_yuan": 1,
			"be_member_increase_count": 2,
			"buy_award_count_for_buyer": 4,
			"order_money_percentage_for_each_buy": 3.14,
			"buy_via_offline_increase_count_for_author": 6,
			"buy_via_offline_increase_count_percentage_for_author": 4.14,
			"use_ceiling": 20,
			"review_increase": 7
		}
		"""