#auther:徐梓豪 2016-12-09
Feature:运营人员删除已经配置给分类的特殊资质
	"""
		1.运营人员删除特殊资质
	"""
Background:
	Given manager登录系统
	When manager添加商品分类
		"""
		{
			"电子数码": {
				"耳机": null,
				"手机": null,
				"平板电脑": {
					"分类31": null
				}
			},
			"生活用品": {
				"零食": null,
				"肥皂":null,
				"清洁用品": null
			}
		}
		"""

	When manager为商品分类'平板电脑'配置特殊资质
		"""
		[{
			"qualification_name":"平板电脑销售许可证"
		}]
		"""
	Then manager查看商品分类'平板电脑'的特殊资质
		|   qualification_name   |
		| 平板电脑销售许可证|

	When manager为商品分类'零食'配置特殊资质
		"""
		[{
			"qualification_name":"食品安全资格"
		},{
			"qualification_name":"食品销售资格"
		},{
			"qualification_name":"安全食品许可证"
		}]
		"""
	Then manager查看商品分类'零食'的特殊资质
		|   qualification_name   |
		|    食品安全资格   |
		|    食品销售资格   |
		|   安全食品许可证  |

@gaia @mall @mall.product @mall.product_classification @product_classification_qualification @aix
Scenario:1 运营人员删除资质
	When manager删除商品分类'零食'中已经分配的资质
		"""
		[{
			"qualification_name":"食品安全资格"
		}]
		"""
	Then manager查看商品分类'零食'的特殊资质
		|   qualification_name   |
		|    食品销售资格   |
		|   安全食品许可证  |
