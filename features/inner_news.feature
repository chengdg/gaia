#author:徐梓豪 2016-12-06
feature:运营人员管理站内消息
	"""
	1.运营新增站内消息
		#所有客户都能收到站内消息
	2.运营编辑站内消息
		#编辑后客户收到的站内消息也会变化
	3.运营删除站内消息
		#客户端也将该站内消息删除，不管已读未读

	"""
Background:
	Given manager登录系统
	When manager创建账号
		"""
		{
			"login_account":"yunying",
			"password":"1",
			"real_name":"运营",
			"email":"yunying@163.com",
			"department":"CorpStaff",
			"right":"运营管理"
		}
		"""
	When yunying新增站内消息
		"""
		[{
		"title":"每日新闻",
		"content":"今日华为获取世界范围5g标准的短码控制信道",
		"accessory":''
		},{
		"title":"新增功能介绍",
		"content":"系统目前新增新功能站内消息，系统更新功能后会在这及时更新并附上操作视频",
		"accessory":''
		}]
		"""
	Then yunying查看站内消息列表
		|    title   |creat_time|operation|
		|  每日新闻  | 创建时间 |编辑/删除|
		|新增功能介绍| 创建时间 |编辑/删除|

@mantis @news	
Scenario:1 运营编辑站内消息
	When yunying编辑站内消息
		"""
		[{
		"title":"每日之声",
		"content":"今日推荐：土小宝",
		"accessory":''
		},{
		"title":"新增功能介绍",
		"content":"系统目前新增新功能站内消息，系统更新功能后会在这及时更新并附上操作视频",
		"accessory":''
		}]
		"""
	Then yunying查看站内消息列表
	Then yunying查看站内消息列表
		|    title   |creat_time|operation|
		|  每日之声  | 创建时间 |编辑/删除|
		|新增功能介绍| 创建时间 |编辑/删除|

@mantis @news	
Scenario:2 运营删除站内消息
	When yunying编辑站内消息
		"""
		{
		"title":"新增功能介绍"
		}
		"""
	Then yunying查看消息列表
		|    title   |creat_time|operation|
		|  每日之声  | 创建时间 |编辑/删除|
