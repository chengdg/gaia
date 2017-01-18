Feature:jobs添加电子面单

Background:
	Given jobs登录系统
@gaia @features @mall @logic @electric_account @add_logic_electric_account
Scenario:1 jobs添加电子面单
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