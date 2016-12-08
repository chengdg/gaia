auther:徐梓豪 2016-08-31
Feature:运营人员新增标签
"""
1.运营人员新增标签
2.运营人员删除标签
"""

Background:
	Given manager登录管理系统
	When manager添加账号
	"""
	[{
	"account_type":"运营",
	"account_name":"运营部门",
	"login_account":"yunying",
	"password":123456,
	"ramarks":"运营部门"
	}]
	"""
	Given yunying登录系统
	When yunying添加分类
	"""
	{
	"head_classify":"无",
	"classify_name":"电子数码",
	"comments":"1"
	},{
	"head_classify":"无",
	"classify_name":"生活用品",
	"comments":"1"
	},{
	"head_classify":"电子数码",
	"classify_name":"手机",
	"comments":""
	},{
	"head_classify":"电子数码",
	"classify_name":"平板电脑",
	"comments":""
	},{
	"head_classify":"电子数码",
	"classify_name":"耳机",
	"comments":""
	},{
	"head_classify":"生活用品",
	"classify_name":"零食",
	"comments":""
	},{
	"head_classify":"生活用品",
	"classify_name":"肥皂",
	"comments":""
	},{
	"head_classify":"生活用品",
	"classify_name":"清洗用品,
	"comments":""
	}
	"""
	
@panda @tag
Scenario:1 运营人员新增标签
	Given yunying登录管理系统
	When yunying新增标签
	"""
	{
	"classify":"国家",
	"tag":{
			"美国"，"法国","中国","德国","意大利","澳大利亚"
	},{
	"classify":"省市",
	"tag":{
			"江苏"，"黑龙江","广东","浙江","北京","江西"
	},{
	"classify":"基本信息",
	"tag":{
			"男"，"女","新生儿","9-13岁","14-18岁","成年"
		}
	}
	"""
	Then yunying查看标签列表
	|classify|                tag                 |
	|  国家  |美国，法国,中国,德国,意大利,澳大利亚|
	|  省市  |  江苏，黑龙江,广东,浙江,北京,江西  |
	|基本信息| 男，女,新生儿,9-13岁,14-18岁,成年  | 

@panda @tag
Scenario:2 运营人员删除标签
	Given yunying登录管理系统
	When yunying新增标签分组
		"""
		[{
		"classify":"国家"
		},{
		"classify":"省市"
		},{
		"classify":"基本信息"
		}]
		"""
	When yunying新增标签
	"""
	{
	"classify":"国家",
	"tag":{
			"美国"，"法国","中国","德国","意大利","澳大利亚"
	},{
	"classify":"省市",
	"tag":{
			"江苏"，"黑龙江","广东","浙江","北京","江西"
	},{
	"classify":"基本信息",
	"tag":{
			"男"，"女","新生儿","9-13岁","14-18岁","成年"
		}
	}
	"""
	Then yunying查看标签列表
		|classify|                tag                 |
		|  国家  |美国，法国,中国,德国,意大利,澳大利亚|
		|  省市  |  江苏，黑龙江,广东,浙江,北京,江西  |
		|基本信息| 男，女,新生儿,9-13岁,14-18岁,成年  | 

	When yunying删除标签
		"""
		{
		"tag":"江苏"
		}
		"""
	Then yunying查看标签列表
		|classify|                tag                 |
		|  国家  |美国，法国,中国,德国,意大利,澳大利亚|
		|  省市  |     黑龙江,广东,浙江,北京,江西     |
		|基本信息| 男，女,新生儿,9-13岁,14-18岁,成年  | 
	When yunying删除标签
		"""
		{
		"tag":"澳大利亚"
		}
		"""
	Then yunying查看标签列表
		|classify|                tag                 |
		|  国家  |     美国，法国,中国,德国,意大利    |
		|  省市  |     黑龙江,广东,浙江,北京,江西     |
		|基本信息| 男，女,新生儿,9-13岁,14-18岁,成年  | 
	When yunying删除标签
		"""
		{
		"classify":"基本信息"
		}
		"""
	Then yunying查看标签列表
		|classify|                tag                 |
		|  国家  |     美国，法国,中国,德国,意大利    |
		|  省市  |     黑龙江,广东,浙江,北京,江西     |
