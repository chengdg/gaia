#auther:徐梓豪 2016-12-09
Feature:运营人员配置分类的标签和资质
	"""
		1.运营人员为分类配置特殊资质
	"""


Background:
	Given weizoom登录系统
	When weizoom添加商品分类
		"""
		[{
			"电子数码": [{
				"耳机": [],
				"手机": [],
				"平板电脑": [{
					"分类31": []
				}]
			}]
		},{
			"生活用品": [{
				"零食": null,
				"肥皂":null,
				"清洁用品": null
			}]
		}]
		"""

	
@gaia @mall @mall.product @mall.product_classification @product_classification_qualification
Scenario:1  运营人员为分配配置特殊资质
	When weizoom为商品分类'平板电脑'配置特殊资质
		"""
		[{
			"qualification_name":"平板电脑销售许可证"
		}]
		"""

	Then weizoom查看商品分类'平板电脑'的特殊资质
		| qualification_name |
		| 平板电脑销售许可证 |