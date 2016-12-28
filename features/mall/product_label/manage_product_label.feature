#auther:徐梓豪 2016-08-31
Feature:商品标签的新增、删除
	"""
	商品商品标签的新增、删除
	"""

Background:
	Given weizoom登录系统
	
	When weizoom新增商品标签分组
		"""
		[{
			"label_group_name": "国家"
		},{
			"label_group_name": "省市"
		},{
			"label_group_name": "基本信息"
		}]
		"""

@gaia @mall @product @product_label @label @aix
Scenario:1 运营人员新增商品标签
	When weizoom添加商品标签
		"""
		[{
			"label_group_name": "国家",
			"labels": ["美国","法国","中国","德国","意大利","澳大利亚"]
		},
		{
			"label_group_name": "省市",
			"labels": ["江苏","黑龙江","广东","浙江","北京","江西"]
		},
		{
			"label_group_name": "基本信息",
			"labels": ["男","女","新生儿","9-13岁","14-18岁","成年"]
		}]
		"""
	
	Then weizoom查看商品标签列表
		|label_group_name|        labels          |
		|  国家  |美国,法国,中国,德国,意大利,澳大利亚|
		|  省市  |  江苏,黑龙江,广东,浙江,北京,江西  |
		|基本信息| 男,女,新生儿,9-13岁,14-18岁,成年  | 

@gaia @mall @product @product_label @label @aix
Scenario:2 运营人员删除商品标签
	Given weizoom登录系统
	
	When weizoom添加商品标签
		"""
		[{
			"label_group_name": "国家",
			"labels": ["美国","法国","中国","德国","意大利","澳大利亚"]
		},
		{
			"label_group_name": "省市",
			"labels": ["江苏","黑龙江","广东","浙江","北京","江西"]
		},
		{
			"label_group_name": "基本信息",
			"labels": ["男","女","新生儿","9-13岁","14-18岁","成年"]
		}]
		"""

	When weizoom删除商品标签
		"""
		[{
			"label_name":"江苏"
		},
		{
			"label_name":"澳大利亚"
		}]
		"""
	Then weizoom查看商品标签列表
		|label_group_name|      labels        |
		|  国家  |美国,法国,中国,德国,意大利    |
		|  省市  |     黑龙江,广东,浙江,北京,江西     |
		|基本信息| 男,女,新生儿,9-13岁,14-18岁,成年  | 
	When weizoom删除商品标签分组
		"""
		[{
			"label_group_name":"基本信息"
		}]
		"""
	Then weizoom查看商品标签列表
		|label_group_name|        labels           |
		|  国家  |     美国,法国,中国,德国,意大利    |
		|  省市  |     黑龙江,广东,浙江,北京,江西     |
