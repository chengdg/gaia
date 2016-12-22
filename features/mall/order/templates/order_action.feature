Feature: 购买自营平台商品
"""
weizoom: 微众公司
zhouxun: 即自营平台
bill: 会员
"""

  Background:
	 Given weizoom登录系统
	 And weizoom已添加商品分组
	"""
	[{
		"name": "分类1"
	}, {
		"name": "分类2"
	}, {
		"name": "分类3"
	}]
	"""
	 And weizoom已添加商品规格
	"""
	[{
		"name": "颜色",
		"type": "图片",
		"values": [{
			"name": "黑色",
			"image": "/static/test_resource_img/icon_color/black.png"
		}, {
			"name": "白色",
			"image": "/static/test_resource_img/icon_color/white.png"
		}]
	}, {
		"name": "尺寸",
		"type": "文字",
		"values": [{
			"name": "M"
		}, {
			"name": "S"
		}]
	}]
	"""
	 When weizoom添加商品分类
	"""
	{
		"分类11": {
			"分类21": null,
			"分类22": null,
			"分类23": {
				"分类31": null
			}
		},
		"分类12": {
			"分类24": null
		},
		"分类13": null
	}
	"""
	 When weizoom添加供应商
	"""
	[{
		"name": "苹果",
		"type": "固定低价"
	}, {
		"name": "微软",
		"type": "首月55分成",
		"divide_info": {
			"divide_money": 1.0,
			"basic_rebate": 20,
		"rebate": 30
		}
	}, {
		"name": "谷歌",
		"type": "零售返点",
		"retail_info": {
			"rebate": 50
		}
	}]
	"""
	 Given weizoom登录系统
	 When weizoom添加商品
"""
[{
	"name": "东坡肘子",
	"supplier": "苹果",
	"classification": "分类31",
	"swipe_images": [{
		"url": "/static/test_resource_img/hangzhou1.jpg"
	}, {
		"url": "/static/test_resource_img/hangzhou2.jpg"
	}, {
		"url": "/static/test_resource_img/hangzhou3.jpg"
	}],
	"model": {
		"models": {
			"standard": {
				"price": 11.12,
				"purchase_price": 1.1,
				"stock_type": "无限"
			}
		}
	}
}, {
	"name": "叫花鸡",
	"supplier": "微软",
	"classification": "分类24",
	"swipe_images": [{
		"url": "/static/test_resource_img/hangzhou2.jpg"
	}],
	"model": {
		"models": {
			"黑色 M": {
				"price": 10.1,
				"purchase_price": 1.2,
				"stock_type": "有限",
				"stocks": 10
			},
			"白色 S": {
				"price": 20.2,
				"purchase_price": 1.2,
				"stock_type": "有限",
				"stocks": 20
			}
		}
	}
}, {
	"name": "黄桥烧饼",
	"swipe_images": [{
		"url": "/static/test_resource_img/hangzhou3.jpg"
	}],
	"model": {
		"models": {
			"standard": {
				"price": 30.1,
				"purchase_price": 1.0,
				"stock_type": "有限",
				"stocks": 30
			}
		}
	}
}]
"""
	 Given zhouxun登录系统
	 When zhouxun添加支付方式
	"""
	[{
		"type": "微信支付",
		"is_active": "启用",
		"version": 3,
		"weixin_appid": "app_id_1",
		"mch_id": "mch_id_1",
		"api_key": "api_key_1",
		"paysign_key": "paysign_key_1"
	}]
	"""
	 Then zhouxun能获得'待售'商品列表
"""
[]
"""
	 Given zhouxun成为自营平台
	 Then zhouxun能获得'weizoom商品池'商品列表
"""
[{
	"name": "黄桥烧饼",
	"supplier": "",
	"supplier_type": "",
	"classification": "",
	"price": 30.1,
	"stocks": 30,
	"gross_profit": 29.10,
	"image": "/static/test_resource_img/hangzhou3.jpg"
}, {
	"name": "叫花鸡",
	"supplier": "微软",
	"supplier_type": "首月55分成(20%)",
	"classification": "分类12-分类24",
	"price": "10.10~20.20",
	"stocks": "",
	"gross_profit": "8.90~19.00",
	"image": "/static/test_resource_img/hangzhou2.jpg"
}, {
	"name": "东坡肘子",
	"supplier": "苹果",
	"supplier_type": "固定低价",
	"classification": "分类11-分类23-分类31",
	"price": 11.12,
	"stocks": "无限",
	"gross_profit": 10.02,
	"image": "/static/test_resource_img/hangzhou1.jpg"
}]
"""
	 When zhouxun添加代销商品
"""
["东坡肘子", "叫花鸡"]
"""
	 Then zhouxun能获得'zhouxun商品池'商品列表
"""
[{
	"name": "叫花鸡"
}, {
	"name": "东坡肘子"
}]
"""
	 When zhouxun将商品移动到'在售'货架
"""
["东坡肘子", "叫花鸡"]
"""
	 Then zhouxun能获得'在售'商品列表
"""
[{
	"name": "叫花鸡"
}, {
	"name": "东坡肘子"
}]
"""
	 Given bill关注zhouxun的公众号::apiserver
	 When bill访问zhouxun的webapp::apiserver
	 When bill购买zhouxun的商品::apiserver
"""
{
	"order_id":"001",
	"date":"2016-01-01",
	"ship_name": "bill",
	"ship_tel": "13811223344",
	"ship_area": "北京市 北京市 海淀区",
	"ship_address": "泰兴大厦",
	"pay_type": "微信支付",
	"products":[{
		"name":"东坡肘子",
		"count":1
	}],
	"postage": 0.00,
	"customer_message": "bill购买无规格商品1"
}
"""
	 Given zhouxun登录系统
	 Then zhouxun获得订单列表
"""
		[
		{
		"bill": "",
		"status_code": "created"
		}
	]
"""

  @ztqb
  Scenario:1 支付订单
  weizoom添加商品后：
  1、zhouxun能获得weizoom商品池商品（创建时间倒序排列）

  zhouxun创建代销商品后:
  1、zhouxun在商品池商品列表能看到代销商品（创建时间倒序排列）


	 When jobs支付订单'001'

	 Then zhouxun获得订单列表
"""
[
  {
  "bid": "001",
  "status_code": "paid",
  "delivery_items": [
       {
          "status_code": "paid"

       }
    ]
  }
]
"""

  @ztqb
  Scenario:1 取消订单
  weizoom添加商品后：
  1、zhouxun能获得weizoom商品池商品（创建时间倒序排列）

  zhouxun创建代销商品后:
  1、zhouxun在商品池商品列表能看到代销商品（创建时间倒序排列）


	 When jobs取消订单'001'

	 Then zhouxun获得订单列表
"""
[
  {
  "bid": "001",
  "status_code": "cancelled",
  "delivery_items": [
       {
          "status_code": "cancelled"

       }
    ]
  }
]
"""
"""