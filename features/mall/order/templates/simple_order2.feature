#author:徐梓豪  2016-12-15
Feature:客户创建待审核商品
"""
	客户添加无规格商品
	"""

  Background:
    Given weizoom登录系统
    When weizoom添加商品分类
		"""
		[{
			"分类11": [{
				"分类21": [],
				"分类22": []
			}]
		}]
		"""

  @ztqb
  Scenario:1 客户添加无规格商品
    Given jobs登录系统
    When jobs创建待审核商品
		"""
		[{
			"classification_name": "分类11",
			"product_name": "武汉鸭脖",
			"promotion_title":"武汉鸭脖",
			"has_product_model": false,
			"price":10.00,
			"weight":0.23,
			"stock":200,
			"limit_zone_type":"无限制",
			"postage_type": "统一运费",
			"postage_money":2.00,
			"images": [],
			"remark":"周黑鸭 鲜卤鸭脖 230g/袋 办公室休闲零食 肉干小食"
		}]
		"""
    Given weizoom登录系统
    When weizoom审核通过待审核商品
		"""
		["武汉鸭脖"]
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
    When zhouxun添加代销商品
    """
    ["武汉鸭脖"]
    """
    When zhouxun将商品移动到'在售'货架
    """
    ["武汉鸭脖"]
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
          "name":"武汉鸭脖",
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
            "status_code": "created",
            "bid":"001"

          }
        ]
    """