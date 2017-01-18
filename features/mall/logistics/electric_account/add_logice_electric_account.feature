Feature:jobs添加电子面单
	#不同物流公司对应的必填项也有不同

	 圆通：Customer_name，monthcode
	 中通：Customer_name，Custome_password
	 申通：Customer_name，Custome_password
	 韵达：Customer_name，Custome_password
	 百世：Customer_name，Custome_password
	 顺丰：
	 德邦：Customer_name
	 宅急送：Customer_name，Custome_password
	 优速：Customer_name，Custome_password
	 广东邮政：
	 EMS：
	 远成快运：
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
		""
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