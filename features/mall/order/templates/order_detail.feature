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

@ztqb
Scenario:1 创建代销的商品
weizoom添加商品后：
1、zhouxun能获得weizoom商品池商品（创建时间倒序排列）

zhouxun创建代销商品后:
1、zhouxun在商品池商品列表能看到代销商品（创建时间倒序排列）

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
Then zhouxun获得'001'订单详情
"""
      {
        "bill": "",
        "status_code": "created",
        "coupon_money": 0,
        "integral": 0,
        "ship_area": "1_1_8",
        "pay_money": 11.12,
        "origin_weizoom_card_money": 0,
        "ship_name": "bill",
        "product_price": 11.12,
        "final_price": 11.12,
        "is_first_order": false,
        "bid": "001",
        "ship_area_text": "北京市 北京市 海淀区",
        "extra_coupon_info": {
          "bid": "",
          "type": ""
        },
        "weizoom_card_money": 0,
        "ship_address": "泰兴大厦",
        "save_money": 0,
        "member_info": {
          "is_subscribed": true,
          "name": "bill"
        },
        "bill_type": 0,
        "is_weizoom_order": true,
        "remark": "",
        "origin_final_price": 11.12,
        "refunding_info": {
          "weizoom_card_money": 0,
          "coupon_money": 0,
          "integral": 0,
          "cash": 0,
          "integral_money": 0,
          "total": 0
        },
        "integral_money": 0,
        "ship_tel": "13811223344",
        "is_group_buy": false,
        "coupon_id": 0,
        "customer_message": "",
        "postage": 0,
        "delivery_time": "",
        "payment_time": "",
        "promotion_saved_money": 0,
        "bid_with_edit_money": "001",
        "delivery_items": [
          {
            "status_code": "created",

            "express_company_name_value": "",
            "express_details": [],
            "area": "1_1_8",
            "ship_name": "bill",
            "leader_name": "",
            "with_logistics_trace": true,
            "payment_time": "2000-01-01 00:00:00",
            "express_company_name_text": "",
            "refunding_info": {
              "weizoom_card_money": 0,
              "coupon_money": 0,
              "integral": 0,
              "cash": 0,
              "finished": false,
              "integral_money": 0,
              "total_can_refund": 11.12,
              "total": 0
            },

            "customer_message": "bill购买无规格商品1",
            "postage": 0,
            "supplier_info": {
              "supplier_type": "supplier",
              "name": "苹果"
            },
            "with_logistics": false,
            "products": [
              {
                "count": 1,
                "is_deleted": false,
                "show_sale_price": 11.12,
                "weight": 2,
                "product_model_name_texts": [],
                "total_origin_price": 11.12,
                "promotion_info": {
                  "type": "",
                  "promotion_saved_money": 0,
                  "grade_discount_money": 0,
                  "integral_count": 0,
                  "integral_money": 0
                },
                "thumbnails_url": "/static/test_resource_img/hangzhou1.jpg",
                "sale_price": 11.12,
                "origin_price": 11.12,
                "name": "东坡肘子"
              }
            ],
            "express_number": ""
          }
        ],
        "pay_interface_type_code": "weixin_pay",
        "edit_money": 0
      }

"""

