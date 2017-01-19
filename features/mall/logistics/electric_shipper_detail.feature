Feature:客户获得单个发货人详情
Background:
	Given jobs登录系统
	When jobs添加发货人
		"""
		[{
		"shipper":"aini",
		"province":"江苏省",
		"city":"南京市",
		"district":"栖霞区",
		"particular_address":"文昌东路437号",
		"post_code":"02134",
		"business_name":"爱伲咖啡",
		"mobile_num":"13813984402",
		"remark":"测试"
		},{
		"shipper":"tuxiaobao",
		"province":"江苏省",
		"city":"南京市",
		"district":"玄武区",
		"particular_address":"玄武路127号",
		"post_code":"02134",
		"business_name":"土小宝食品",
		"mobile_num":"13813984405",
		"remark":"测试1"
		}]
		"""
@gaia @features @mall @logic @electric_shipper @electric_shipper_detail @xzh 
Scenario:1 客户获取指定发货人详情
	Given jobs登录系统

	Then jobs能获得指定发货人'aini'的列表
		"""
		[{
		"shipper":"aini",
		"province":"江苏省",
		"city":"南京市",
		"district":"栖霞区",
		"particular_address":"文昌东路437号",
		"post_code":"02134",
		"business_name":"爱伲咖啡",
		"mobile_num":"13813984402",
		"remark":"测试"
		}]
		"""
