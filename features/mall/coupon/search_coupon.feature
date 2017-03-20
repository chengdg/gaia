Feature: 搜索优惠券
	Jobs能通过管理系统搜索"优惠券"

Background:
	Given jobs登录系统
	And jobs已添加商品
		"""
		[{
			"name": "商品1",
			"price": 200.00
		},{
			"name": "商品2",
			"price": 200.00
		},{
			"name": "商品3",
			"price": 200.00
		}]
		"""
	Given zhouxun成为'jobs'的会员
	Given yangmi成为'jobs'的会员
	Given yaochen成为'jobs'的会员
	Given bigs成为'jobs'的会员

@gaia @promotion @coupon
Scenario:1 按优惠券的bid搜索
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "通用券1",
			"coupon_id_prefix": "coupon1_id_"
		}, {
			"name": "通用券2",
			"coupon_id_prefix": "coupon2_id_"
		}]
		"""
	#有搜索结果
	When jobs搜索优惠券规则'通用券1'中的优惠券
		"""
		{
			"bid": "coupon1_id_3"
		}
		"""
	Then jobs能获得优惠券搜索结果
		"""
		[{
			"bid": "coupon1_id_3"
		}]
		"""
	#搜索结果为空
	When jobs搜索优惠券规则'通用券1'中的优惠券
		"""
		{
			"bid": "coupon1_id_333"
		}
		"""
	Then jobs能获得优惠券搜索结果
		"""
		[]
		"""

@gaia @promotion @coupon
Scenario:1 按优惠券的状态搜索
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "通用券1",
			"coupon_id_prefix": "coupon1_id_",
			"count": 3
		}, {
			"name": "通用券2",
			"coupon_id_prefix": "coupon2_id_",
			"count": 2
		}]
		"""
	#搜索未领取优惠券
	When jobs搜索优惠券规则'通用券1'中的优惠券
		"""
		{
			"status": "ungot"
		}
		"""
	Then jobs能获得优惠券搜索结果
		"""
		[{
			"bid": "coupon1_id_1"
		}, {
			"bid": "coupon1_id_2"
		}, {
			"bid": "coupon1_id_3"
		}]
		"""
	#搜索未使用优惠券
	When jobs为会员每人发放'1'张优惠券'通用券1'
		"""
		["zhouxun", "yangmi"]
		"""
	When jobs搜索优惠券规则'通用券1'中的优惠券
		"""
		{
			"status": "unused"
		}
		"""
	Then jobs能获得优惠券搜索结果
		"""
		[{
			"bid": "coupon1_id_1",
			"receiver": "zhouxun"
		}, {
			"bid": "coupon1_id_2",
			"receiver": "yangmi"
		}]
		"""
	#搜索已使用优惠券
	When jobs使用优惠券'通用券1'
		"""
		["coupon1_id_2", "coupon1_id_3"]
		"""
	When jobs搜索优惠券规则'通用券1'中的优惠券
		"""
		{
			"status": "used"
		}
		"""
	Then jobs能获得优惠券搜索结果
		"""
		[{
			"bid": "coupon1_id_2"
		}, {
			"bid": "coupon1_id_3"
		}]
		"""

@gaia @promotion @coupon
Scenario:1 按优惠券的领取人搜索
	Given jobs登录系统
	When jobs添加优惠券规则
		"""
		[{
			"name": "通用券1",
			"coupon_id_prefix": "coupon1_id_",
			"count": 3
		}, {
			"name": "通用券2",
			"coupon_id_prefix": "coupon2_id_",
			"count": 2
		}]
		"""
	#搜索未使用优惠券
	When jobs为会员每人发放'1'张优惠券'通用券1'
		"""
		["zhouxun", "yangmi"]
		"""
	#有搜索结果
	When jobs搜索优惠券规则'通用券1'中的优惠券
		"""
		{
			"receiver": "zhouxun"
		}
		"""
	Then jobs能获得优惠券搜索结果
		"""
		[{
			"bid": "coupon1_id_1"
		}]
		"""
	#搜索结果为空
	When jobs搜索优惠券规则'通用券1'中的优惠券
		"""
		{
			"receiver": "yaochen"
		}
		"""
	Then jobs能获得优惠券搜索结果
		"""
		[]
		"""