#auther:徐梓豪 2016-12-09
Feature:运营人员配置分类的标签
	"""
		1.运营人员为分类配置标签
		2.运营人员删除一级分类的标签后查看二级分类的标签
	"""
Background:
	Given weizoom登录系统
	When weizoom添加商品分类
		"""
		[{
			"电子数码": [{
				"耳机": []
			},{
				"手机": []
			},{
				"平板电脑": []
			}]
		},{
			"生活用品": [{
				"零食": []
			},{
				"肥皂":[]
			},{
				"清洁用品": []
			}]
		}]
		"""
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
	When weizoom添加商品标签
		"""
		[{
			"label_group_name":"国家",
			"labels":["美国", "法国","中国","德国","意大利","澳大利亚"]
		},{
			"label_group_name":"省市",
			"labels":["江苏", "黑龙江","广东","浙江","北京","江西"]
		},{
			"label_group_name":"基本信息",
			"labels":["男", "女","新生儿","9-13岁","14-18岁","成年"]
		}]
		"""
@gaia @mall @mall.product @classfication_label @aix
Scenario:1 运营人员为分类配置标签
	When weizoom为商品分类'平板电脑'配置标签
		"""
		[{
			"label_group_name":"国家",
			"labels":["美国", "法国"]
		}]
		"""

	Then weizoom查看商品分类列表
		|classfication_name|      operation      |
		|   电子数码  |修改,删除,配置标签|
		|   生活用品  |修改,删除,配置标签|

	Then weizoom查看商品分类'电子数码'的二级分类
		|classfication_name|    operation          |
		|     耳机    |修改,删除,配置特殊资质,配置标签|
		|     手机    |修改,删除,配置特殊资质,配置标签|
		|  平板电脑    |修改,删除,配置特殊资质,已配置标签|

	Then weizoom查看商品分类'生活用品'的二级分类
		|classfication_name|             operation           |
		|     零食    |修改,删除,配置特殊资质,配置标签|
		|     肥皂    |修改,删除,配置特殊资质,配置标签|
		|   清洁用品  |修改,删除,配置特殊资质,配置标签|

	When weizoom为商品分类'生活用品'配置标签
	
		"""
		[{
			"label_group_name":"省市",
			"labels":["江苏","黑龙江"]
		},{
			"label_group_name":"基本信息",
			"labels":["男","女"]
		}]
		"""

	Then weizoom查看商品分类列表
		|classfication_name|      operation      |
		|   电子数码  |修改,删除,配置标签|
		|   生活用品  |修改,删除,已配置标签|

	Then weizoom查看商品分类'电子数码'的二级分类
		|classfication_name|           operation           |
		|     耳机    |修改,删除,配置特殊资质,配置标签|
		|     手机    |修改,删除,配置特殊资质,配置标签|
		|   平板电脑  |修改,删除,配置特殊资质,已配置标签|
#
	Then weizoom查看商品分类'生活用品'的二级分类
		|classfication_name|              operation            |
		|     零食    |修改,删除,配置特殊资质,已配置标签|
		|     肥皂    |修改,删除,配置特殊资质,已配置标签|
		|   清洁用品  |修改,删除,配置特殊资质,已配置标签|

	Then weizoom查看商品分类'肥皂'的标签
		"""
		[{
			"label_group_name":"省市",
			"labels":["江苏", "黑龙江"]
		},{
			"label_group_name":"基本信息",
			"labels":["男","女"]
		}]
		"""
	When weizoom为商品分类'零食'配置标签
		"""
		[{
			"label_group_name":"省市",
			"labels":["江苏","黑龙江"]
		},{
			"label_group_name":"基本信息",
			"labels":["男","女"]
		}]
		"""
	When weizoom为商品分类'肥皂'配置标签
		"""
		[{
			"label_group_name":"省市",
			"labels":["江苏"]
		},{
			"label_group_name":"基本信息",
			"labels":["男"]
		}]
		"""

	Then weizoom查看商品分类'肥皂'的标签
		"""
		[{
			"label_group_name": "省市",
			"labels": ["江苏","黑龙江"]
		},{
			"label_group_name": "基本信息",
			"labels": ["男","女"]
		}]
		"""
	When weizoom为商品分类'清洁用品'配置标签
		"""
		[]
		"""

	Then weizoom查看商品分类列表
		|classfication_name|      operation      |
		|   电子数码  |修改,删除,配置标签|
		|   生活用品  |修改,删除,已配置标签|

	Then weizoom查看商品分类'电子数码'的二级分类
		|classfication_name|           operation           |
		|     耳机    |修改,删除,配置特殊资质,配置标签|
		|     手机    |修改,删除,配置特殊资质,配置标签|
		|   平板电脑  |修改,删除,配置特殊资质,已配置标签|

	Then weizoom查看商品分类'生活用品'的二级分类
		|classfication_name|          operation            |
		|     零食    |修改,删除,配置特殊资质,已配置标签|
		|     肥皂    |修改,删除,配置特殊资质,已配置标签|
		|   清洁用品  |修改,删除,配置特殊资质,已配置标签|

@gaia @mall @mall.product @classfication_label @aix
Scenario:1 运营人员删除一级分类的标签后查看二级分类的标签
	Then weizoom查看商品分类列表
		|classfication_name|      operation      |
		|     电子数码     |修改,删除,配置标签|
		|     生活用品     |修改,删除,配置标签|
	When weizoom为商品分类'电子数码'配置标签
		"""
		[{
			"label_group_name":"省市",
			"labels":["江苏","黑龙江"]
		},{
			"label_group_name":"基本信息",
			"labels":["男","女"]
		}]
		"""
	Then weizoom查看商品分类'电子数码'的二级分类
		|classfication_name|            operation            |
		|       耳机       |修改,删除,配置特殊资质,已配置标签|
		|       手机       |修改,删除,配置特殊资质,已配置标签|
		|      平板电脑    |修改,删除,配置特殊资质,已配置标签|
	When weizoom为商品分类'耳机'配置标签
		"""
		[{
			"label_group_name":"省市",
			"labels":["江苏","黑龙江"]
		},{
			"label_group_name":"基本信息",
			"labels":["男","女","新生儿"]
		},{
			"label_group_name":"国家",
			"labels":["中国"]
		}]
		"""
	When weizoom为商品分类'电子数码'配置标签
		"""
		[]
		"""
	Then weizoom查看商品分类列表
		|classfication_name|      operation      |
		|     电子数码     |修改,删除,配置标签|
		|     生活用品     |修改,删除,配置标签|
 	Then weizoom查看商品分类'电子数码'的二级分类
		|classfication_name|            operation            |
		|       耳机       |修改,删除,配置特殊资质,已配置标签|
		|       手机       |修改,删除,配置特殊资质,配置标签|
		|      平板电脑    |修改,删除,配置特殊资质,配置标签|
#	Then weizoom查看商品分类'耳机'的标签
#		"""
#		[{
#			"label_group_name":"省市",
#			"labels":["江苏","黑龙江"]
#		},{
#			"label_group_name":"基本信息",
#			"labels":["男","女","新生儿"]
#		},{
#			"label_group_name":"国家",
#			"labels":["中国"]
#		}]
#		"""