Feature:客户增加发货人
	
@gaia @add_electric_shipper @xzh
Scenario:1 客户增加发货人
	Given jobs登录系统
	When jobs新增发货人
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
	Then jobs 查看发货人列表
		|shipper|mobile_num |        area        |particular_address|post_code|
		|aini|13813984402|江苏省-南京市-栖霞区|   文昌东路437号  |  02134  |
		|tuxiaobao|13813984405|江苏省-南京市-玄武区|  玄武路127号   |  02134  |