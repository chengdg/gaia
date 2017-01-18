Feature:jobs编辑电子面单
Background:
	Given jobs登录系统
	When jobs添加电子面单账号配置
		"""
		[{
		"name":"圆通快递",
		"Customer_name":"yt",
		"Custome_password":"",
		"monthcode":"3",
		"send_site":"",
		"remark":""
		},{
		"name":"申通快递",
		"Customer_name":"st",	
		"Custome_password":"1",
		"monthcode":"",
		"send_site":"",
		"remark":""
		},{
		"name":"顺丰快递",
		"Customer_name":"",
		"Custome_password":"",
		"monthcode":"",
		"send_site":"",
		"remark":""
		}]
		"""
@gaia @features @mall @logic @electric_account @edit_logic_electric_account
Scenario:1 jobs编辑电子面单
	Given jobs登录系统
	When jobs编辑物流公司为'申通快递'的账号配置
		"""
		[{
		"name":"申通快递",
		"Customer_name":"st123",
		"Custome_password":"1",
		"monthcode":"",
		"send_site":"",
		"remark":""
		}]
		"""
	Then jobs能获得电子面单账号列表
		"""
		[{
		"name":"圆通快递",
		"Customer_name":"yt",
		"Custome_password":"",
		"monthcode":"3",
		"send_site":"",
		"remark":""
		},{
		"name":"申通快递",
		"Customer_name":"st123",
		"Custome_password":"1",
		"monthcode":"",
		"send_site":"",
		"remark":""
		},{
		"name":"顺丰快递",
		"Customer_name":"",
		"Custome_password":"",
		"monthcode":"",
		"send_site":"",
		"remark":""
		}]
	When jobs编辑物流公司为'圆通快递'的账号配置
		"""
		[{
		"name":"EMS",
		"Customer_name":"",
		"Custome_password":"",
		"monthcode":"",
		"send_site":"",
		"remark":"EMS不需要账号和密码就能创建"
		}]
		"""
	Then jobs能获得电子面单账号列表
		"""
		[{
		"name":"EMS",
		"Customer_name":"",
		"Custome_password":"",
		"monthcode":"",
		"send_site":"",
		"remark":"EMS不需要账号和密码就能创建"
		},{
		"name":"申通快递",
		"Customer_name":"st123",
		"Custome_password":"1",
		"monthcode":"",
		"send_site":"",
		"remark":""
		},{
		"name":"顺丰快递",
		"Customer_name":"",
		"Custome_password":"",
		"monthcode":"",
		"send_site":"",
		"remark":""
		}]