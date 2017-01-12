Feature:客户删除发货人
	"""
	1.jobs删除发货人
	"""
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
		"district":"栖霞区",
		"particular_address":"玄武区",
		"post_code":"02134",
		"business_name":"土小宝食品",
		"mobile_num":"13813984405",
		"remark":"测试1"
		}]
		"""
	Then jobs获得发货人列表
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
		"remark":"测试",
		"operate":['设为默认','编辑','删除']
		},{
		"shipper":"tuxiaobao",
		"province":"江苏省",
		"city":"南京市",
		"district":"玄武区",
		"particular_address":"玄武路127号",
		"post_code":"02134",
		"business_name":"土小宝食品",
		"mobile_num":"13813984405",
		"remark":"测试1",
		"operate":['设为默认','编辑','删除']
		}]
		"""
@gaia @delete_electric_shipper @xzh
Scenario:1 jobs删除默认的发货人
	Given jobs登录系统
	When jobs删除发货人
		"""
		['aini']
		"""
	Then jobs获得发货人列表
		"""
		[{
		"shipper":"tuxiaobao",
		"province":"江苏省",
		"city":"南京市",
		"district":"玄武区",
		"particular_address":"玄武路127号",
		"post_code":"02134",
		"business_name":"土小宝食品",
		"mobile_num":"13813984405",
		"remark":"测试1",
		"operate":['设为默认','编辑','删除']
		}]
		"""
