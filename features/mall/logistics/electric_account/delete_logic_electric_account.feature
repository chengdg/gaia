Feature:jobs删除电子面单
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
@gaia @features @mall @logic @electric_account @delete_logic_electric_account
Scenario:1 jobs删除电子面单
	Given jobs登录系统
	When jobs删除物流公司为'申通快递'的账号配置
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
		"name":"顺丰快递",
		"Customer_name":"",
		"Custome_password":"",
		"monthcode":"",
		"send_site":"",
		"remark":""
		}]
		"""