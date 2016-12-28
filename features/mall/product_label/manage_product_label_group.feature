#auther:徐梓豪 2016-08-31
Feature:商品标签分组的新增、删除
	"""
	商品标签分组的新增、删除
	"""

Background:
	Given weizoom登录系统
	
@gaia @mall @product @product_label @label_group @aix
Scenario:1 运营人员新增商品标签分组
	When weizoom新增商品标签分组
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

	Then weizoom查看商品标签列表
		|label_group_name|labels|
		|  国家  |              |
		|  省市  |              |
		|基本信息|              |

@gaia @mall @product @product_label @label_group @aix
Scenario:2 运营人员删除商品标签分组
	When weizoom新增商品标签分组
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

	Then weizoom查看商品标签列表
		|label_group_name|labels|
		|  国家  |              |
		|  省市  |              |
		|基本信息|              |

	When weizoom删除商品标签分组
		"""
		[{
			"label_group_name": "国家"
		}]
		"""

	Then weizoom查看商品标签列表
		|label_group_name|labels|
		|  省市  |              |
		|基本信息|              |