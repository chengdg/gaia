#author:徐梓豪 2016-01-22
Feature:weizoom编辑账号信息
Background:
	Given weizoom登录系统
	When weizoom添加商品分类
		"""
		[{
			"分类11": [{
                "分类21": []
            },{
                "分类22": []
            },{
                "分类23": [{
                    "分类31": []
                }]
            }]
		},{
			"分类12": [{
				"分类24": []
			}]
		},{
			"分类13": []
		}]
		"""
@gaia1 @account @edit_account
Scenario:1 weizoom修改账号信息
	When weizoom配置'jobs'的账号信息
		"""
		{
			"account_type":"合作客户",
			"company_name":"爱昵咖啡有限责任公司",
			"name":"爱昵咖啡",
			"purchase_type":"零售价返点",
			"points":"5.00",
			"clear_period":"15天",
			"classfications":["分类22"],
			"contact":"aini",
			"contact_phone":"13813985506",
			"note":"爱昵咖啡客户体验账号",
			"service_tel":13813984402,
			"service_qq_first":445068326,
			"service_qq_second":245079415
		}
		"""
	When weizoom配置'zhangxue'的账号信息
		"""
		{
			"account_type":"合作客户",
			"company_name":"土小宝有限责任公司",
			"name":"土小宝",
			"purchase_type":"固定底价",
			"clear_period":"自然月",
			"classfications":["分类23"],
			"contact":"aini",
			"contact_phone":"13813985506",
			"note":"土小宝客户体验账号",
			"service_tel":13813984402,
			"service_qq_first":445068326,
			"service_qq_second":245079415
		}
		"""
	Then weizoom能获取账号列表
		|shop_name|company_name|customer_from|username|created_at|classfications|purchase_type|max_product_count|operation|
		|爱昵咖啡|爱昵咖啡有限责任公司|   --   |    jobs    |创建时间|分类22|零售价返点|200|编辑|
		|土小宝  |土小宝有限责任公司  | --     |   zhangxue |创建时间|分类23|固定底价|100|编辑|