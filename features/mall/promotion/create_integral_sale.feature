Feature: 添加积分应用促销活动

Background:
	Given jobs登录系统
	When jobs添加商品
		"""
		[{
			"name": "叫花鸡",
			"model": {
				"models": {
					"standard": {
						"price": 10
					}
				}
			}
		}, {
			"name": "水晶虾仁",
			"model": {
				"models": {
					"standard": {
						"price": 20
					}
				}
			}
		}, {
			"name": "松鼠桂鱼",
			"model": {
				"models": {
					"standard": {
						"price": 30
					}
				}
			}
		}]
		"""
	When jobs创建会员等级
		"""
		[{
			"name": "银牌会员"
		}, {
			"name": "金牌会员"
		}]
		"""

@gaia @promotion @promotion.integral_sale
Scenario:创建单商品的积分应用
	创建单商品的统一折扣的积分应用，查看详情

	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		{
			"name": "50%让利大折扣",
			"promotion_title": "中秋大促，仅此一天",
			"start_date": "2017-01-01 13:00",
			"end_date": "2017-03-01 13:00",
			"is_permanant_active": false,
			"rule_info": {
				"type": "fixed",
				"discount": 10.1,
				"discount_money": 5
			},
			"products": ["叫花鸡"]
		}
		"""
	Then jobs能获得积分应用活动'50%让利大折扣'的详情
		"""
		{
			"name": "50%让利大折扣",
			"promotion_title": "中秋大促，仅此一天",
			"start_date": "2017-01-01 13:00",
			"end_date": "2017-03-01 13:00",
			"is_permanant_active": false,
			"rule_info": {
				"type": "fixed",
				"discount": 10.1,
				"discount_money": 5
			},
			"products": ["叫花鸡"]
		}
		"""

@gaia @promotion @promotion.integral_sale
Scenario:创建多商品的积分应用
	创建多商品的分会员等级折扣的积分应用，查看详情

	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		{
			"name": "50%让利大折扣",
			"promotion_title": "中秋大促，仅此一天",
			"start_date": "2017-01-01 13:00",
			"end_date": "2017-03-01 13:00",
			"is_permanant_active": false,
			"rule_info": {
				"type": "individual",
				"rules": [{
					"member_grade": "普通会员",
					"discount": 10.1,
					"discount_money": 3.1
				}, {
					"member_grade": "银牌会员",
					"discount": 20.1,
					"discount_money": 5.1
				}, {
					"member_grade": "金牌会员",
					"discount": 25.3,
					"discount_money": 7.0
				}]
			},
			"products": ["水晶虾仁", "松鼠桂鱼"]
		}
		"""
	Then jobs能获得积分应用活动'50%让利大折扣'的详情
		"""
		{
			"name": "50%让利大折扣",
			"promotion_title": "中秋大促，仅此一天",
			"start_date": "2017-01-01 13:00",
			"end_date": "2017-03-01 13:00",
			"is_permanant_active": false,
			"rule_info": {
				"type": "individual",
				"rules": [{
					"member_grade": "普通会员",
					"discount": 10.1,
					"discount_money": 3.1
				}, {
					"member_grade": "银牌会员",
					"discount": 20.1,
					"discount_money": 5.1
				}, {
					"member_grade": "金牌会员",
					"discount": 25.3,
					"discount_money": 7.0
				}]
			},
			"products": ["水晶虾仁", "松鼠桂鱼"]
		}
		"""


@gaia @promotion @promotion.integral_sale
Scenario:创建多商品的积分应用
	创建多个积分应用后，查看积分应用列表

	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		{
			"name": "50%让利大折扣",
			"promotion_title": "中秋大促，仅此一天",
			"start_date": "2017-01-01 13:00",
			"end_date": "2017-03-01 13:00",
			"is_permanant_active": false,
			"rule_info": {
				"type": "fixed",
				"discount": 10.1,
				"discount_money": 5
			},
			"products": ["叫花鸡"]
		}
		"""
	When jobs创建积分应用活动
		"""
		{
			"name": "联合大让利",
			"promotion_title": "过年大促",
			"start_date": "2017-01-03 13:00",
			"end_date": "2017-03-03 13:00",
			"is_permanant_active": true,
			"rule_info": {
				"type": "individual",
				"rules": [{
					"member_grade": "普通会员",
					"discount": 10.1,
					"discount_money": 3.1
				}, {
					"member_grade": "银牌会员",
					"discount": 20.1,
					"discount_money": 5.1
				}, {
					"member_grade": "金牌会员",
					"discount": 25.3,
					"discount_money": 7.0
				}]
			},
			"products": ["水晶虾仁", "松鼠桂鱼"]
		}
		"""
	Then jobs能获得积分应用活动列表
		"""
		[{
			"name": "联合大让利",
			"promotion_title": "过年大促",
			"start_date": "2017-01-03 13:00",
			"end_date": "2017-03-03 13:00",
			"is_permanant_active": true,
			"rule_info": {
				"type": "individual",
				"rules": [{
					"member_grade": "普通会员",
					"discount": 10.1,
					"discount_money": 3.1
				}, {
					"member_grade": "银牌会员",
					"discount": 20.1,
					"discount_money": 5.1
				}, {
					"member_grade": "金牌会员",
					"discount": 25.3,
					"discount_money": 7.0
				}]
			},
			"products": ["水晶虾仁", "松鼠桂鱼"]
		}, {
			"name": "50%让利大折扣",
			"promotion_title": "中秋大促，仅此一天",
			"start_date": "2017-01-01 13:00",
			"end_date": "2017-03-01 13:00",
			"is_permanant_active": false,
			"rule_info": {
				"type": "fixed",
				"discount": 10.1,
				"discount_money": 5
			},
			"products": ["叫花鸡"]
		}]
		"""