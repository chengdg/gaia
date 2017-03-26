Feature: 添加会员收货地址

Background:
	Given jobs登录系统
	Given zhouxun成为'jobs'的会员
	Given yangmi成为'jobs'的会员


@gaia @member @wip
Scenario: 添加会员收货地址
	添加会员收货地址后
	1. 能获得收货地址列表

	Given jobs登录系统
	Then jobs能获得会员'zhouxun'的信息
		"""
		{
			"ship_infos": []
		}
		"""
	Then jobs能获得会员'yangmi'的信息
		"""
		{
			"ship_infos": []
		}
		"""
	When jobs为会员'zhouxun'添加收货地址
		"""
		[{
			"receiver_name": "周迅1",
			"phone": "13811223344",
			"area": "北京市 北京市 海淀区",
			"address": "长安大街",
			"is_selected": false
		}, {
			"receiver_name": "周迅2",
			"phone": "13811223355",
			"area": "江苏省 南京市 秦淮区",
			"address": "国创园",
			"is_selected": true
		}]
		"""
	Then jobs能获得会员'zhouxun'的信息
		"""
		{
			"ship_infos": [{
				"receiver_name": "周迅1",
				"phone": "13811223344",
				"area": "北京市 北京市 海淀区",
				"address": "长安大街",
				"is_selected": false
			}, {
				"receiver_name": "周迅2",
				"phone": "13811223355",
				"area": "江苏省 南京市 秦淮区",
				"address": "国创园",
				"is_selected": true
			}]
		}
		"""
	Then jobs能获得会员'zhouxun'的收货地址列表
		"""
		[{
			"receiver_name": "周迅1",
			"phone": "13811223344",
			"area": "北京市 北京市 海淀区",
			"address": "长安大街",
			"is_selected": false
		}, {
			"receiver_name": "周迅2",
			"phone": "13811223355",
			"area": "江苏省 南京市 秦淮区",
			"address": "国创园",
			"is_selected": true
		}]
		"""
	Then jobs能获得会员'yangmi'的信息
		"""
		{
			"ship_infos": []
		}
		"""
	