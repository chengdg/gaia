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

@gaia @promotion @wip
Scenario:创建积分应用
	Given jobs登录系统
	When jobs创建积分应用活动
		"""
		{
			"name": "50%让利大折扣",
			"promotio_title": "中秋大促，仅此一天",
			"start_date": "2017-01-01 13:00",
			"end_date": "2017-03-01 13:00",
			"is_permanant_active": false,
			"rule_info": {
				"type": "fixed",
				"discount_money": "5"
			},
			"products": ["叫花鸡"]
		}
		"""