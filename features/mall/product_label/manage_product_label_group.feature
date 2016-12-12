#auther:徐梓豪 2016-08-31
Feature:商品标签分组的新增、删除
	"""
	商品标签分组的新增、删除
	"""

Background:
	Given manager登录系统
	
@gaia @mall @product @product_label @label_group
Scenario:1 运营人员新增商品标签分组
	When manager新增商品标签分组
		"""
		[{
			"label_group_name": "国家"
		},
		{
			"label_group_name": "省市"
		},
		{
			"label_group_name": "基本信息"
		}]
		"""

	Then manager查看商品标签列表
		|label_group_name|labels|
		|  国家  |              |
		|  省市  |              |
		|基本信息|              |

@gaia @mall @product @product_label @label_group
Scenario:2 运营人员删除商品标签分组
	When manager新增商品标签分组
		"""
		[{
			"label_group_name": "国家"
		},
		{
			"label_group_name": "省市"
		},
		{
			"label_group_name": "基本信息"
		}]
		"""

	Then manager查看商品标签列表
		|label_group_name|labels|
		|  国家  |              |
		|  省市  |              |
		|基本信息|              |

	When manager删除商品标签分组
		"""
		[{
			"label_group_name": "国家"
		}]
		"""

	Then manager查看商品标签列表
		|label_group_name|labels|
		|  省市  |              |
		|基本信息|              |