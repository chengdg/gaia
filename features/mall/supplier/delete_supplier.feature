Feature: 删除供应商
"""
	Jobs能通过管理系统为商城删除的"供应商"
"""

Background:
	Given jobs登录系统
	When jobs添加供应商
		"""
		[{
			"name": "苹果"
		}, {
			"name": "微软"
		}, {
			"name": "谷歌"
		}]
		"""
	Given bill登录系统
	When bill添加供应商
		"""
		[{
			"name": "苹果"
		}, {
			"name": "微软"
		}, {
			"name": "谷歌"
		}]
		"""


@mall @mall.product @mall.product_category @hermes
Scenario:1 Jobs删除已存在的供应商
	Given jobs登录系统
	When jobs删除供应商'微软'
	Then jobs能获取供应商列表
		"""
		[{
			"name": "苹果"
		}, {
			"name": "谷歌"
		}]
		"""
	Given bill登录系统
	Then bill能获取供应商列表
		"""
		[{
			"name": "苹果"
		}, {
			"name": "微软"
		}, {
			"name": "谷歌"
		}]
		"""
