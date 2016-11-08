Feature: 更新wbapp配置

Background:
	Given jobs登录系统

@gaia @mall @mall.config
Scenario:1 更新webapp配置
	When jobs更新Webapp配置为
		"""
		{
			"show_product_sales": true,
			"show_product_sort": true,
			"show_product_search": true,
			"show_shopping_cart": true,
			"is_enable_bill": true,
			"max_product_count": 99,
			"order_expired_day": 100
		}
		"""
	Then jobs能获得Webapp配置
		"""
		{
			"show_product_sales": true,
			"show_product_sort": true,
			"show_product_search": true,
			"show_shopping_cart": true,
			"is_enable_bill": true,
			"max_product_count": 99,
			"order_expired_day": 100
		}
		"""
	When jobs更新Webapp配置为
		"""
		{
			"show_product_sales": false,
			"show_product_sort": false,
			"show_product_search": false,
			"show_shopping_cart": false,
			"is_enable_bill": false
		}
		"""
	Then jobs能获得Webapp配置
		"""
		{
			"show_product_sales": false,
			"show_product_sort": false,
			"show_product_search": false,
			"show_shopping_cart": false,
			"is_enable_bill": false
		}
		"""