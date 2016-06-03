#coding: utf8
import copy
from datetime import datetime
import json

from eaglet.core.db import models
from db.account.models import User, UserProfile
from eaglet.core import watchdog
import settings

DEFAULT_DATETIME = datetime.strptime('2000-01-01', '%Y-%m-%d')


#########################################################################
# 商城相关Model
#########################################################################

MALL_CONFIG_PRODUCT_COUNT_NO_LIMIT = 999999999
MALL_CONFIG_PRODUCT_NORMAL = 7
class MallConfig(models.Model):
    """
    商城配置
    """
    owner = models.ForeignKey(User, related_name='mall_config')
    max_product_count = models.IntegerField(default=MALL_CONFIG_PRODUCT_NORMAL)  # 最大商品数量
    is_enable_bill = models.BooleanField(default=False)  # 是否启用发票功能
    show_product_sales = models.BooleanField(default=False) # 通用设置，商品销量
    show_product_sort = models.BooleanField(default=False) # 通用设置，商品排序
    show_product_search = models.BooleanField(default=False) # 通用设置， 商品搜索框
    show_shopping_cart =models.BooleanField(default=False) # 通用设置， 购物车
    created_at = models.DateTimeField(auto_now_add=True)  # 添加时间
    # new add at 13  by bert
    order_expired_day = models.IntegerField(default=0)  # 未付款订单过期时间(单位是小时)

    class Meta(object):
        db_table = 'mall_config'

#########################################################################
# 订单完成分享挣积分信息配置相关Model
#########################################################################
class MallShareOrderPageConfig(models.Model):
    """
    订单完成分享挣积分信息配置
    """
    owner = models.ForeignKey(User)
    is_share_page = models.BooleanField(default=False) # 是否提示分享挣积分
    background_image = models.CharField(max_length=1024, default='')
    share_image = models.CharField(max_length=1024, default='')
    share_describe = models.TextField(default='')
    material_id = models.IntegerField(default=0) #图文素材id
    news_id = models.IntegerField(default=0) #图文id
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        db_table = 'mall_share_order_page_config'
        verbose_name = '订单完成分享挣积分信息配置'
        verbose_name_plural = '订单完成分享挣积分信息配置'


#########################################################################
# 地域相关Model
#########################################################################
class City(models.Model):
    name = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    province_id = models.IntegerField(db_index=True)

    class Meta(object):
        db_table = 'city'
        verbose_name = '城市列表'
        verbose_name_plural = '城市列表'

class Province(models.Model):
    name = models.CharField(max_length=50)

    class Meta(object):
        db_table = 'province'
        verbose_name = '省份列表'
        verbose_name_plural = '省份列表'


class District(models.Model):
    name = models.CharField(max_length=50)
    city_id = models.IntegerField(db_index=True)

    class Meta(object):
        db_table = 'district'
        verbose_name = '区县列表'
        verbose_name_plural = '区县列表'



#########################################################################
# 运费相关Model
#########################################################################
class PostageConfig(models.Model):
    """
    运费配置
    """
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=256)  # 名称
    first_weight = models.FloatField(default=0.0)  # 首重
    first_weight_price = models.FloatField(default=0.0)  # 首重价格
    is_enable_added_weight = models.BooleanField(default=True)  # 是否启用续重机制
    added_weight = models.CharField(max_length=256, default='0')  # 续重
    added_weight_price = models.CharField(max_length=256, default='0')  # 续重价格
    display_index = models.IntegerField(default=1)  # 显示的排序
    is_used = models.BooleanField(default=True)  # 是否启用
    is_system_level_config = models.BooleanField(default=False)  # 是否是系统创建的不可修改的配置
    created_at = models.DateTimeField(auto_now_add=True)  # 添加时间
    update_time = models.DateTimeField(auto_now=True)  # 更新时间
    is_enable_special_config = models.BooleanField(default=True)  # 是否启用续重机制
    is_enable_free_config = models.BooleanField(default=True)  # 是否启用包邮机制
    is_deleted = models.BooleanField(default=False) #是否删除

    class Meta(object):
        db_table = 'mall_postage_config'

    def get_special_configs(self):
        return SpecialPostageConfig.select().dj_where(postage_config=self)

    def get_free_configs(self):
        return FreePostageConfig.select().dj_where(postage_config=self)


class SpecialPostageConfig(models.Model):
    """
    特殊地区运费配置
    """
    owner = models.ForeignKey(User)
    postage_config = models.ForeignKey(PostageConfig)
    first_weight_price = models.FloatField(default=0.0)  # 首重价格
    added_weight_price = models.CharField(max_length=256)  # 续重价格
    created_at = models.DateTimeField(auto_now_add=True)  # 添加时间
    # v2
    destination = models.CharField(max_length=512)  # 目的省份的id集合
    first_weight = models.FloatField(default=0.0)  # 首重
    added_weight = models.FloatField(default=0.0)  # 续重

    class Meta(object):
        db_table = 'mall_postage_config_special'


class FreePostageConfig(models.Model):
    """
    特殊地区包邮配置
    """
    owner = models.ForeignKey(User)
    postage_config = models.ForeignKey(PostageConfig)
    destination = models.CharField(max_length=512)  # 目的省份的id集合
    condition = models.CharField(max_length=25, default='count')  # 免邮条件类型, 共有'count', 'money'两种
    condition_value = models.CharField(max_length=25)  # 免邮条件值
    created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

    class Meta(object):
        db_table = 'mall_free_postage_config'

#########################################################################
# 商品相关Model
#########################################################################
class ProductCategory(models.Model):
    """
    商品分类
    """
    owner = models.ForeignKey(User, related_name='owned_product_categories')
    name = models.CharField(max_length=256)  # 分类名称
    pic_url = models.CharField(max_length=1024, default='')  # 分类图片
    product_count = models.IntegerField(default=0)  # 包含商品数量
    display_index = models.IntegerField(default=1)  # 显示的排序
    created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

    class Meta(object):
        db_table = 'mall_product_category'



PRODUCT_STOCK_TYPE_LIMIT = 1
PRODUCT_STOCK_TYPE_UNLIMIT = 0
PRODUCT_SHELVE_TYPE_ON = 1
PRODUCT_SHELVE_TYPE_OFF = 0
PRODUCT_SHELVE_TYPE_RECYCLED = 2
PRODUCT_DEFAULT_TYPE = 'object'
PRODUCT_DELIVERY_PLAN_TYPE = 'delivery'
PRODUCT_TEST_TYPE = 'test'
PRODUCT_INTEGRAL_TYPE = 'integral'
POSTAGE_TYPE_UNIFIED = 'unified_postage_type'
POSTAGE_TYPE_CUSTOM = 'custom_postage_type'

PRODUCT_TYPE2TEXT = {
    PRODUCT_DEFAULT_TYPE: u'普通商品',
    PRODUCT_DELIVERY_PLAN_TYPE: u'套餐商品',
    PRODUCT_INTEGRAL_TYPE: u'积分商品'
}
MAX_INDEX = 2**16 - 1

class Product(models.Model):
    """
    商品

    表名：mall_product
    """
    owner = models.ForeignKey(User, related_name='user-product')
    name = models.CharField(max_length=256)  # 商品名称
    physical_unit = models.CharField(default='', max_length=256)  # 计量单位
    price = models.FloatField(default=0.0)  # 商品价格
    introduction = models.CharField(max_length=256)  # 商品简介
    weight = models.FloatField(default=0.0)  # 重量
    thumbnails_url = models.CharField(max_length=1024)  # 商品缩略图
    pic_url = models.CharField(max_length=1024)  # 商品图
    detail = models.TextField(default='')  # 商品详情
    remark = models.TextField(default='')  # 备注
    display_index = models.IntegerField(default=0)  # 显示的排序
    created_at = models.DateTimeField(auto_now_add=True)  # 添加时间
    shelve_type = models.IntegerField(default=PRODUCT_SHELVE_TYPE_OFF)  # 0:下架（待售） 1:上架（在售） 2:回收站
    shelve_start_time = models.CharField(max_length=50, null=True)  # 定时上架:上架时间
    shelve_end_time = models.CharField(max_length=50, null=True)  # 定时上架:下架时间
    stock_type = models.IntegerField(
        default=PRODUCT_STOCK_TYPE_UNLIMIT)  # 0:无限 1:有限
    stocks = models.IntegerField(default=-1)  # 起购数量
    is_deleted = models.BooleanField(default=False)  # 是否删除
    is_support_make_thanks_card = models.BooleanField(
        default=False)  # 是否支持制作感恩贺卡
    type = models.CharField(max_length=50,default=PRODUCT_DEFAULT_TYPE)  # 产品的类型
    update_time = models.DateTimeField(auto_now=True)  # 商品信息更新时间 2014-11-11
    postage_id = models.IntegerField(default=-1)  # 运费id ，-1为使用统一运费
    is_use_online_pay_interface = models.BooleanField(default=True)  # 在线支付方式
    is_use_cod_pay_interface = models.BooleanField(default=False)  # 货到付款支付方式
    promotion_title = models.CharField(max_length=256, default='')  # 促销标题
    user_code = models.CharField(max_length=256, default='')  # 编码
    bar_code = models.CharField(max_length=256, default='')  # 条码
    unified_postage_money = models.FloatField(default=0.0)  # 统一运费金额
    postage_type = models.CharField(max_length=125, default=POSTAGE_TYPE_UNIFIED)  # 运费类型
    weshop_sync = models.IntegerField(default=0)  # 0不同步 1普通同步 2加价同步
    weshop_status = models.IntegerField(default=0)  # 0待售 1上架 2回收站
    is_member_product = models.BooleanField(default=False)  # 是否参加会员折扣
    supplier = models.IntegerField(default=0) # 供货商
    supplier_user_id = models.IntegerField(default=0) # 供货商(非8千)
    purchase_price = models.FloatField(default=0.0) # 进货价格
    is_enable_bill = models.BooleanField(default=False)  # 商品是否开具发票
    is_delivery = models.BooleanField(default=False) # 是否勾选配送时间
    buy_in_supplier = models.BooleanField(default=False) # 记录下单位置是商城还是供货商，0是商城1是供货商

    class Meta(object):
        db_table = 'mall_product'


class CategoryHasProduct(models.Model):
    """
    <category, product>关系
    """
    product = models.ForeignKey(Product)
    category = models.ForeignKey(ProductCategory)
    display_index = models.IntegerField(default=0, null=True)  # 分组商品排序
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        db_table = 'mall_category_has_product'


class ProductSwipeImage(models.Model):
    """
    商品轮播图
    """
    product = models.ForeignKey(Product)
    url = models.CharField(max_length=256, default='')
    link_url = models.CharField(max_length=256, default='')
    created_at = models.DateTimeField(auto_now_add=True)  # 添加时间
    # v2
    width = models.IntegerField()  # 图片宽度
    height = models.IntegerField()  # 图片高度

    class Meta(object):
        db_table = 'mall_product_swipe_image'


class ProductSales(models.Model):
    """
    商品销量
    """
    product = models.ForeignKey(Product)
    sales = models.IntegerField(default=0) #销量

    class Meta(object):
        db_table = 'mall_product_sales'


class MemberProductWishlist(models.Model):
    owner = models.ForeignKey(User)
    member_id = models.IntegerField(default=0) #会员ID
    product_id = models.IntegerField(default=0) #商品ID
    is_collect = models.BooleanField(default=False) #商品是否被收藏
    add_time = models.DateTimeField(auto_now_add=True) #商品收藏的时间
    delete_time = models.DateTimeField(default=DEFAULT_DATETIME) #商品取消收藏的时间
    created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

    class Meta(object):
        db_table = 'mall_member_product_wishlist'


PAY_INTERFACE_ALIPAY = 0
PAY_INTERFACE_TENPAY = 1
PAY_INTERFACE_WEIXIN_PAY = 2
PAY_INTERFACE_COD = 9
PAY_INTERFACE_PREFERENCE = 10
PAY_INTERFACE_WEIZOOM_COIN = 3

PAYTYPE2LOGO = {
    PAY_INTERFACE_ALIPAY: '/standard_static/img/mockapi/alipay.png',
    PAY_INTERFACE_TENPAY: '/standard_static/img/mockapi/tenpay.png',
    PAY_INTERFACE_WEIXIN_PAY: '/standard_static/img/mockapi/weixin_pay.png',
    PAY_INTERFACE_COD: '/standard_static/img/mockapi/cod.png',
    PAY_INTERFACE_WEIZOOM_COIN: '/standard_static/img/mockapi/wzcoin.png',
}
PAYTYPE2NAME = {
    -1: u'',
    PAY_INTERFACE_PREFERENCE: u'优惠抵扣',
    PAY_INTERFACE_ALIPAY: u'支付宝',
    PAY_INTERFACE_TENPAY: u'财付通',
    PAY_INTERFACE_WEIXIN_PAY: u'微信支付',
    PAY_INTERFACE_COD: u'货到付款',
    PAY_INTERFACE_WEIZOOM_COIN: u"微众卡支付"
}
PAYNAME2TYPE = {
    u'优惠抵扣':PAY_INTERFACE_PREFERENCE,
    u'支付宝': PAY_INTERFACE_ALIPAY,
    u'财付通': PAY_INTERFACE_TENPAY,
    u'微信支付': PAY_INTERFACE_WEIXIN_PAY,
    u'货到付款': PAY_INTERFACE_COD,
    u"微众卡支付": PAY_INTERFACE_WEIZOOM_COIN
}

VALID_PAY_INTERFACES = [
    PAY_INTERFACE_WEIXIN_PAY,
    PAY_INTERFACE_COD,
    PAY_INTERFACE_WEIZOOM_COIN,
    PAY_INTERFACE_ALIPAY]
ONLINE_PAY_INTERFACE = [
    PAY_INTERFACE_WEIXIN_PAY,
    PAY_INTERFACE_ALIPAY,
    PAY_INTERFACE_WEIZOOM_COIN,
    PAY_INTERFACE_TENPAY]

class PayInterface(models.Model):
    """
    支付方式
    """
    owner = models.ForeignKey(User)
    type = models.IntegerField()  # 支付接口类型
    description = models.CharField(max_length=50)  # 描述
    is_active = models.BooleanField(default=True)  # 是否启用
    related_config_id = models.IntegerField(default=0)  # 各种支付方式关联配置信息的id
    created_at = models.DateTimeField(auto_now_add=True)  # 创建日期

    class Meta(object):
        db_table = 'mall_pay_interface'

    def pay(self, order, webapp_owner_id):
        if PAY_INTERFACE_ALIPAY == self.type:
            return '/webapp/alipay/?woid={}&order_id={}&related_config_id={}'.format(webapp_owner_id, order.order_id, self.related_config_id)
        elif PAY_INTERFACE_TENPAY == self.type:
            from account.models import UserProfile
            user_profile = UserProfile.objects.get(user_id=webapp_owner_id)
            call_back_url = "http://{}/tenpay/mall/pay_result/get/{}/{}/".format(
                user_profile.host,
                webapp_owner_id,
                self.related_config_id)
            notify_url = "http://{}/tenpay/mall/pay_notify_result/get/{}/{}/".format(
                user_profile.host,
                webapp_owner_id,
                self.related_config_id)
            pay_submit = TenpaySubmit(
                self.related_config_id,
                order,
                call_back_url,
                notify_url)
            tenpay_url = pay_submit.submit()

            return tenpay_url
        elif PAY_INTERFACE_COD == self.type:
            return './?woid={}&module=mall&model=pay_result&action=get&pay_interface_type={}&order_id={}'.format(
                webapp_owner_id,
                PAY_INTERFACE_COD,
                order.order_id)
        elif PAY_INTERFACE_WEIXIN_PAY == self.type:
            return '/webapp/wxpay/?woid={}&order_id={}&pay_id={}&showwxpaytitle=1'.format(
                webapp_owner_id,
                order.order_id,
                self.id)
        else:
            return ''

    def parse_pay_result(self, request):
        error_msg = ''
        if PAY_INTERFACE_ALIPAY == self.type:
            order_id = request.GET.get('out_trade_no', None)
            trade_status = request.GET.get('result', '')
            is_trade_success = ('success' == trade_status.lower())
        elif PAY_INTERFACE_TENPAY == self.type:
            trade_status = int(request.GET.get('trade_status', -1))
            is_trade_success = (0 == trade_status)
            error_msg = request.GET.get('pay_info', '')
            order_id = request.GET.get('out_trade_no', None)
        elif PAY_INTERFACE_COD == self.type:
            is_trade_success = True
            order_id = request.GET.get('order_id')
        elif PAY_INTERFACE_WEIXIN_PAY == self.type:
            is_trade_success = True
            order_id = request.GET.get('order_id')
        else:
            pass

        #兼容改价
        try:
            order_id = order_id.split('-')[0]
        except:
            pass

        return {
            'is_success': is_trade_success,
            'order_id': order_id,
            'error_msg': error_msg
        }

    def parse_notify_result(self, request):
        error_msg = ''
        if PAY_INTERFACE_ALIPAY == self.type:
            config = UserAlipayOrderConfig.objects.get(
                id=self.related_config_id)
            notify = AlipayNotify(request, config)
        elif PAY_INTERFACE_TENPAY == self.type:
            notify = TenpayNotify(request)
        elif PAY_INTERFACE_WEIXIN_PAY == self.type:
            notify = WxpayNotify(request)
        else:
            notify = None

        if notify:
            order_id = notify.get_payed_order_id()
            is_trade_success = notify.is_pay_succeed()
            error_msg = notify.get_pay_info()
            reply_response = notify.get_reply_response()
            order_payment_info = notify.get_order_payment_info()
        else:
            order_id = ''
            is_trade_success = False
            error_msg = ''
            reply_response = ''
            order_payment_info = None

        #兼容改价
        try:
            order_id = order_id.split('-')[0]
        except:
            pass

        return {
            'order_id': order_id,
            'is_success': is_trade_success,
            'error_msg': error_msg,
            'reply_response': reply_response,
            'order_payment_info': order_payment_info
        }

    def get_str_name(self):
        return PAYTYPE2NAME[self.type]


V2 = 0
V3 = 1
class UserWeixinPayOrderConfig(models.Model):
    owner = models.ForeignKey(User)
    app_id = models.CharField(max_length=32, verbose_name='微信公众号app_id')
    app_secret = models.CharField(max_length=64)
    partner_id = models.CharField(max_length=32, verbose_name='合作商户id')
    partner_key = models.CharField(max_length=32, verbose_name='合作商初始密钥')
    paysign_key = models.CharField(max_length=128, verbose_name='支付专用签名串')
    pay_version  = models.IntegerField(default=V2)

    class Meta(object):
        db_table = 'account_weixin_pay_order_config'





#===============================================================================
# UserAlipayOrderConfig : 支付宝支付配置信息
#===============================================================================
class UserAlipayOrderConfig(models.Model):
    owner = models.ForeignKey(User)
    partner = models.CharField(max_length=32, verbose_name='合作身份者ID，以2088开头由16位纯数字组成的字符串')
    key = models.CharField(max_length=32, verbose_name='交易安全检验码，由数字和字母组成的32位字符串')
    private_key = models.CharField(max_length=1024, blank=True, null=True, verbose_name='商户的私钥')
    ali_public_key = models.CharField(max_length=1024, blank=True, null=True, verbose_name='支付宝的公钥')
    input_charset = models.CharField(max_length=8, default='utf-8', verbose_name='字符编码格式 目前支持utf-8')
    sign_type = models.CharField(max_length=8, default='MD5', verbose_name='签名方式')
    seller_email = models.CharField(max_length=64, blank=True)
    pay_version = models.CharField(max_length=64)

    class Meta(object):
        db_table = 'account_alipay_order_config'



#########################################################################
# 商品规格相关Model
#########################################################################
PRODUCT_MODEL_PROPERTY_TYPE_TEXT = 0
PRODUCT_MODEL_PROPERTY_TYPE_IMAGE = 1
class ProductModelProperty(models.Model):
    """
    商品规格属性
    """
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=256)  # 商品规格属性名
    type = models.IntegerField(default=PRODUCT_MODEL_PROPERTY_TYPE_TEXT)  # 属性类型
    is_deleted = models.BooleanField(default=False)  # 是否删除
    created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

    class Meta(object):
        db_table = 'mall_product_model_property'

    @property
    def values(self):
        return list(
            ProductModelPropertyValue.objects.filter(
                property=self,
                is_deleted=False))

    @property
    def is_image_property(self):
        return self.type == PRODUCT_MODEL_PROPERTY_TYPE_IMAGE


class ProductModelPropertyValue(models.Model):
    """
    商品规格属性值
    """
    property = models.ForeignKey(ProductModelProperty, related_name='model_property_values')
    name = models.CharField(max_length=256)  # 商品名称
    pic_url = models.CharField(max_length=1024)  # 商品图
    is_deleted = models.BooleanField(default=False)  # 是否已删除
    created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

    class Meta(object):
        db_table = 'mall_product_model_property_value'


class ProductModel(models.Model):
    """
    商品规格
    """
    owner = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    name = models.CharField(max_length=255)  # 商品规格名
    is_standard = models.BooleanField(default=True)  # 是否是标准规格
    price = models.FloatField(default=0.0)  # 商品价格
    market_price = models.FloatField(default=0.0)  # 商品市场价格
    weight = models.FloatField(default=0.0)  # 重量
    stock_type = models.IntegerField(default=PRODUCT_STOCK_TYPE_UNLIMIT)  # 0:无限 1:有限
    stocks = models.IntegerField(default=0)  # 有限：数量
    is_deleted = models.BooleanField(default=False)  # 是否已删除
    created_at = models.DateTimeField(auto_now_add=True)  # 添加时间
    # v2
    user_code = models.CharField(max_length=256, default='')  # 编码

    class Meta(object):
        db_table = 'mall_product_model'

    def __getitem__(self, name):
        return getattr(self, name, None)


class ProductModelHasPropertyValue(models.Model):
    """
    <商品规格，商品规格属性值>关系
    """
    model = models.ForeignKey(ProductModel)
    property_id = models.IntegerField(default=0)
    property_value_id = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

    class Meta(object):
        db_table = 'mall_product_model_has_property'


class ProductProperty(models.Model):
    """
    商品属性
    """
    owner = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    name = models.CharField(max_length=256)  # 商品属性名
    value = models.CharField(max_length=256)  # 商品属性值
    created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

    class Meta(object):
        db_table = 'mall_product_property'
        verbose_name = '商品属性'
        verbose_name_plural = '商品属性'


class ProductPropertyTemplate(models.Model):
    """
    商品属性模板
    """
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=256)  # 商品属性名
    created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

    class Meta(object):
        db_table = 'mall_product_property_template'


class TemplateProperty(models.Model):
    """
    模板中的属性
    """
    owner = models.ForeignKey(User)
    template = models.ForeignKey(ProductPropertyTemplate)
    name = models.CharField(max_length=256)  # 商品属性名
    value = models.CharField(max_length=256)  # 商品属性值
    created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

    class Meta(object):
        db_table = 'mall_product_template_property'




#########################################################################
# 订单相关Model
#########################################################################
ORDER_STATUS_NOT = 0  # 待支付：已下单，未付款
ORDER_STATUS_CANCEL = 1  # 已取消：取消订单(回退销量)
ORDER_STATUS_PAYED_SUCCESSED = 2  # 已支付：已下单，已付款，已不存此状态
ORDER_STATUS_PAYED_NOT_SHIP = 3  # 待发货：已付款，未发货
ORDER_STATUS_PAYED_SHIPED = 4  # 已发货：已付款，已发货
ORDER_STATUS_SUCCESSED = 5  # 已完成：自下单10日后自动置为已完成状态
ORDER_STATUS_REFUNDING = 6  # 退款中
ORDER_STATUS_REFUNDED = 7  # 退款完成(回退销量)
ORDER_STATUS_GROUP_REFUNDING = 8 #团购退款（没有退款完成按钮）
ORDER_STATUS_GROUP_REFUNDED = 9 #团购退款完成

ORDER_BILL_TYPE_NONE = 0  # 无发票
ORDER_BILL_TYPE_PERSONAL = 1  # 个人发票
ORDER_BILL_TYPE_COMPANY = 2  # 公司发票
STATUS2TEXT = {
    ORDER_STATUS_NOT: u'待支付',
    ORDER_STATUS_CANCEL: u'已取消',
    ORDER_STATUS_PAYED_SUCCESSED: u'已支付',
    ORDER_STATUS_PAYED_NOT_SHIP: u'待发货',
    ORDER_STATUS_PAYED_SHIPED: u'已发货',
    ORDER_STATUS_SUCCESSED: u'已完成',
    ORDER_STATUS_REFUNDING: u'退款中',
    ORDER_STATUS_REFUNDED: u'退款成功',
    ORDER_STATUS_GROUP_REFUNDING: u'退款中',
    ORDER_STATUS_GROUP_REFUNDED: u'退款成功',
}

AUDIT_STATUS2TEXT = {
    ORDER_STATUS_REFUNDING: u'退款中',
    ORDER_STATUS_REFUNDED: u'退款成功',
    ORDER_STATUS_GROUP_REFUNDING: u'团购退款',
}

REFUND_STATUS2TEXT = {
    ORDER_STATUS_REFUNDING: u'退款中',
    ORDER_STATUS_REFUNDED: u'退款成功',
}

ORDERSTATUS2TEXT = STATUS2TEXT

ORDERSTATUS2MOBILETEXT = copy.copy(ORDERSTATUS2TEXT)
ORDERSTATUS2MOBILETEXT[ORDER_STATUS_PAYED_SHIPED] = u'待收货'

PAYMENT_INFO = u'下单'

THANKS_CARD_ORDER = 'thanks_card'  # 感恩贺卡类型的订单

ORDER_TYPE2TEXT = {
    PRODUCT_DEFAULT_TYPE: u'普通订单',
    PRODUCT_DELIVERY_PLAN_TYPE: u'套餐订单',
    PRODUCT_TEST_TYPE: u'测试订单',
    THANKS_CARD_ORDER: u'贺卡订单',
    PRODUCT_INTEGRAL_TYPE: u'积分商品'
}

ORDER_SOURCE_OWN = 0
ORDER_SOURCE_WEISHOP = 1
ORDER_SOURCE2TEXT = {
    ORDER_SOURCE_OWN: u'本店',
    ORDER_SOURCE_WEISHOP: u'商城',
}

QUALIFIED_ORDER_STATUS = [ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED]

ACTION2TARGET_STATUS = {
    'pay': ORDER_STATUS_PAYED_NOT_SHIP,
    'cancel': ORDER_STATUS_CANCEL,
    'finish': ORDER_STATUS_SUCCESSED,
    'buy': ORDER_STATUS_NOT
}

ACTION2MSG = {
    'pay': '支付',
    'cancel': '取消订单',
    'finish': '完成',
    'buy': '下单'
}

ORIGIN_ORDER = -1
NO_SUBORDER = 0

class Order(models.Model):
    """
    订单

    表名: mall_order
    """
    order_id = models.CharField(max_length=100)  # 订单号
    webapp_user_id = models.IntegerField()  # WebApp用户的id
    webapp_id = models.CharField(max_length=20, verbose_name='店铺ID')  # webapp,订单成交的店铺id
    webapp_source_id = models.IntegerField(default=0, verbose_name='商品来源店铺ID')  # 订单内商品实际来源店铺的id，已废弃
    buyer_name = models.CharField(max_length=100)  # 购买人姓名
    buyer_tel = models.CharField(max_length=100, default='')  # 购买人电话,已废弃
    ship_name = models.CharField(max_length=100)  # 收货人姓名
    ship_tel = models.CharField(max_length=100)  # 收货人电话
    ship_address = models.CharField(max_length=200)  # 收货人地址
    area = models.CharField(max_length=100)
    status = models.IntegerField(default=ORDER_STATUS_NOT)  # 订单状态
    order_source = models.IntegerField(default=ORDER_SOURCE_OWN)  # 订单来源 0本店 1商城 已废弃，新订单使用默认值兼容老数据
    bill_type = models.IntegerField(default=ORDER_BILL_TYPE_NONE)  # 发票类型 2016-01-20重新启用by Eugene
    bill = models.CharField(max_length=100, default='')  # 发票信息 2016-01-20重新启用by Eugene
    remark = models.TextField(default='')  # 备注
    supplier_remark = models.TextField(default='')  # 供应商备注
    product_price = models.FloatField(default=0.0)  # 商品金额（应用促销后的商品总价）
    coupon_id = models.IntegerField(default=0)  # 优惠券id，用于支持返还优惠券
    coupon_money = models.FloatField(default=0.0)  # 优惠券金额
    postage = models.FloatField(default=0.0)  # 运费
    integral = models.IntegerField(default=0)  # 积分
    integral_money = models.FloatField(default=0.0)  # 积分对应金额
    member_grade = models.CharField(max_length=50, default='')  # 会员等级
    member_grade_discount = models.IntegerField(default=100)  # 折扣
    member_grade_discounted_money = models.FloatField(default=0.0)  # 折扣金额，已废弃
    # 实付金额: final_price = (product_price + postage) - (coupon_money + integral_money + weizoom_card_money)
    final_price = models.FloatField(default=0.0)
    pay_interface_type = models.IntegerField(default=-1)  # 支付方式
    express_company_name = models.CharField(max_length=50, default='')  # 物流公司名称
    express_number = models.CharField(max_length=100, default='')  # 快递单号
    leader_name = models.CharField(max_length=256, default='')  # 订单负责人
    customer_message = models.CharField(max_length=1024)  # 商家留言
    payment_time = models.DateTimeField(default=DEFAULT_DATETIME)  # 订单支付时间
    created_at = models.DateTimeField(auto_now_add=True)  # 添加时间
    type = models.CharField(max_length=50, default=PRODUCT_DEFAULT_TYPE)  # 产品的类型，已废弃
    integral_each_yuan = models.IntegerField(verbose_name='一元是多少积分', default=-1)
    reason = models.CharField(max_length=256, default='')  # 取消订单原因
    update_at = models.DateTimeField(auto_now=True)  # 订单信息更新时间 2014-11-11
    weizoom_card_money = models.FloatField(default=0.0)  # 微众卡抵扣金额
    promotion_saved_money = models.FloatField(default=0.0)  # 促销优惠金额（只在含限时抢购商品时产生）
    edit_money = models.FloatField(default=0.0)  # 商家修改差价：final_price（计算公式得） - final_price（商家修改成的）= edit_money
    origin_order_id = models.IntegerField(default=0) # 原始(母)订单id，用于微众精选拆单
    # origin_order_id=-1表示有子订单，>0表示有父母订单，=0为默认数据
    supplier = models.IntegerField(default=0) # 订单供货商，用于微众精选拆单
    is_100 = models.BooleanField(default=True) # 是否是快递100能够查询的快递
    delivery_time = models.CharField(max_length=50, default='')  # 配送时间字符串
    is_first_order = models.BooleanField(default=False) # 是否是用户的首单
    supplier_user_id = models.IntegerField(default=0) # 订单供货商user的id，用于系列拆单
    total_purchase_price = models.FloatField(default=0)  # 总订单采购价格

    class Meta(object):
        db_table = 'mall_order'
        verbose_name = '订单'
        verbose_name_plural = '订单'

    @property
    def has_sub_order(self):
        """
        判断该订单是否有子订单
        """
        return self.origin_order_id == -1 and self.status > 0 #未支付的订单按未拆单显示

    @property
    def is_sub_order(self):
        return self.origin_order_id > 0

    @staticmethod
    def get_sub_order_ids(origin_order_id):
        orders = Order.objects.filter(origin_order_id=origin_order_id)
        sub_order_ids = [order.order_id for order in orders]
        return sub_order_ids


    @staticmethod
    def by_webapp_user_id(webapp_user_id, order_id=None):
        if order_id:
            return Order.objects.filter(Q(webapp_user_id__in=webapp_user_id) | Q(id__in=order_id)).filter(origin_order_id__lte=0)
        if isinstance(webapp_user_id, int) or isinstance(webapp_user_id, long):
            return Order.objects.filter(webapp_user_id=webapp_user_id, origin_order_id__lte=0)
        else:
            return Order.objects.filter(webapp_user_id__in=webapp_user_id, origin_order_id__lte=0)

    @staticmethod
    def by_webapp_id(webapp_id):
        # print webapp_id.isdight()
        if str(webapp_id) == '3394':
            return Order.objects.filter(webapp_id=webapp_id)
        if isinstance(webapp_id, list):
            return Order.objects.filter(webapp_source_id__in=webapp_id, origin_order_id__lte=0)
        else:
            return Order.objects.filter(webapp_source_id=webapp_id, origin_order_id__lte=0)

    ##########################################################################
    # get_coupon: 获取定单使用的优惠券信息
    ##########################################################################
    def get_coupon(self):
        if self.coupon_id == 0:
            return None
        else:
            from mall.promotion import models as coupon_model
            coupon = coupon_model.Coupon.objects.filter(id=self.coupon_id)
            if len(coupon) == 1:
                return coupon[0]
            return None


    @staticmethod
    def fill_payment_time(orders):
        order_ids = [order.order_id for order in orders]
        order2paylog = dict(
            [
                (pay_log.order_id, pay_log)
                for pay_log in OrderOperationLog.objects.filter(
                    order_id__in=order_ids, action='支付')])
        for order in orders:
            if order.order_id in order2paylog:
                order.payment_time = order2paylog[order.order_id].created_at
            else:
                order.payment_time = ''

    ##########################################################################
    # get_orders_by_coupon_ids: 通过优惠券id获取订单列表
    ##########################################################################
    @staticmethod
    def get_orders_by_coupon_ids(coupon_ids):
        if len(coupon_ids) == 0:
            return None
        else:
            return list(Order.objects.filter(coupon_id__in=coupon_ids))

    @property
    def get_pay_interface_name(self):
        return PAYTYPE2NAME.get(self.pay_interface_type, u'')

    @property
    def get_str_area(self):
        from util import regional_util
        if self.area:
            return regional_util.get_str_value_by_string_ids(self.area)
        else:
            return ''

    # 订单金额
    def get_total_price(self):
        return self.member_grade_discounted_money + self.postage

    # 支付金额
    # 1、如果是本店的订单，就显示 支付金额
    # 2、如果是商城下的单，显示  订单金额
    def get_final_price(self, webapp_id):
        if self.webapp_id == webapp_id:
            return self.final_price
        else:
            return self.get_total_price()

    # 订单使用积分
    # 1、如果是本店的订单，返回使用积分
    # 2、如果是商城下的单，返回空
    def get_use_integral(self, webapp_id):
        if self.webapp_id == webapp_id:
            return self.integral
        else:
            return ''

    def get_products(self):
        return OrderHasProduct.objects.filter(order=self)

    @staticmethod
    def get_order_has_price_number(order):
        numbers = OrderHasProduct.objects.filter(
            order=order).aggregate(
            Sum("total_price"))
        number = 0
        if numbers["total_price__sum"] is not None:
            number = numbers["total_price__sum"]

        return number

    @staticmethod
    def get_order_has_product(order):
        relations = list(OrderHasProduct.objects.filter(order=order))
        product_ids = [r.product_id for r in relations]
        return Product.objects.filter(id__in=product_ids)

    @staticmethod
    def get_order_has_product_number(order):
        numbers = OrderHasProduct.objects.filter(
            order=order).aggregate(
            Sum("number"))
        number = 0
        if numbers["number__sum"] is not None:
            number = numbers["number__sum"]
        return number

    def get_status_text(self):
        return STATUS2TEXT[self.status]

    # add by bert at member_4.0
    @staticmethod
    def get_orders_final_price_sum(webapp_user_ids):
        numbers = Order.by_webapp_user_id(webapp_user_ids).filter(
            status__gte=ORDER_STATUS_PAYED_SUCCESSED).aggregate(
            Sum("final_price"))
        number = 0
        if numbers["final_price__sum"] is not None:
            number = numbers["final_price__sum"]
        return number

    @staticmethod
    def get_pay_numbers(webapp_user_ids):
        return Order.objects.filter(
            webapp_user_id__in=webapp_user_ids,
            status__gte=ORDER_STATUS_PAYED_SUCCESSED, origin_order_id__lte=0).count()

    @staticmethod
    def get_webapp_user_ids_pay_times_greater_than(webapp_id, pay_times):
        list_info = Order.by_webapp_user_id(webapp_id).filter(
            status__gte=ORDER_STATUS_PAYED_SUCCESSED).values('webapp_user_id').annotate(
            dcount=Count('webapp_user_id'))
        webapp_user_ids = []
        if list_info:
            for vlaue in list_info:
                if vlaue['dcount'] >= int(pay_times):
                    webapp_user_ids.append(vlaue['webapp_user_id'])
        return webapp_user_ids

    @staticmethod
    def get_webapp_user_ids_pay_days_in(webapp_id, days):
        date_day = datetime.today()-timedelta(days=int(days))
        return [
            order.webapp_user_id for order in Order.objects.filter(
                webapp_id=webapp_id,
                status__gte=ORDER_STATUS_PAYED_SUCCESSED,
                payment_time__gte=date_day, origin_order_id__lte=0)]

    @property
    def get_express_details(self):
        if hasattr(self, '_express_details'):
            return self._express_details

        self._express_details = express_util.get_express_details_by_order(self)
        return self._express_details

    @property
    def get_express_detail_last(self):
        if len(self.get_express_details) > 0:
            return self.get_express_details[-1]

        return None

    @staticmethod
    def get_orders_from_webapp_user_ids(webapp_user_ids):
        return Order.objects.filter(webapp_user_id__in=webapp_user_ids)

    def __str__(self):
        r = {}
        for k in self._data.keys():
            try:
                 r[k] = str(getattr(self, k))
            except:
                 r[k] = json.dumps(getattr(self, k))
        return str(r)


# added by chuter
########################################################################
# OrderPaymentInfo: 订单支付信息
########################################################################
class OrderPaymentInfo(models.Model):
    order = models.ForeignKey(Order)
    transaction_id = models.CharField(max_length=32)  # 交易号
    appid = models.CharField(max_length=64)  # 公众平台账户的AppId
    openid = models.CharField(max_length=100)  # 购买用户的OpenId
    out_trade_no = models.CharField(max_length=100)  # 该平台中订单号

    class Meta(object):
        db_table = 'mall_order_payment_info'
        verbose_name = '订单支付信息'
        verbose_name_plural = '订单支付信息'


class OrderHasProduct(models.Model):
    """
    <order, product>关联
    """
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product, related_name='product')
    product_name = models.CharField(max_length=256)  # 商品名
    product_model_name = models.CharField(max_length=256, default='')  # 商品规格名
    price = models.FloatField()  # 商品单价
    total_price = models.FloatField()  # 订单价格
    is_shiped = models.IntegerField(default=0)  # 是否出货
    number = models.IntegerField(default=1)  # 商品数量
    created_at = models.DateTimeField(auto_now_add=True)  # 添加时间
    promotion_id = models.IntegerField(default=0)  # 促销信息id
    promotion_money = models.FloatField(default=0.0)  # 促销抵扣金额
    grade_discounted_money = models.FloatField(default=0.0)  # 折扣金额
    integral_sale_id = models.IntegerField(default=0) #使用的积分应用的id
    origin_order_id = models.IntegerField(default=0) # 原始(母)订单id，用于微众精选拆单
    purchase_price = models.FloatField(default=0)  # 采购单价

    class Meta(object):
        db_table = 'mall_order_has_product'

    # 填充特定的规格信息
    @property
    def get_specific_model(self):
        if hasattr(self, '_product_specific_model'):
            return self._product_specific_model
        else:
            try:
                self._product_specific_model = self.product.fill_specific_model(
                    self.product_model_name)
                return self._product_specific_model
            except:
                return None

    # 如果规格有图片就显示，如果没有，使用缩略图
    @property
    def order_thumbnails_url(self):
        if hasattr(self, '_order_thumbnails_url'):
            return self._order_thumbnails_url
        else:
            if self.get_specific_model:
                for model in self.get_specific_model:
                    if model['property_pic_url']:
                        self._order_thumbnails_url = model['property_pic_url']
                        return self._order_thumbnails_url
            # 没有图片使用商品的图片
            self._order_thumbnails_url = self.product.thumbnails_url
            return self._order_thumbnails_url


class OrderHasPromotion(models.Model):
    """
    <order, promotion>关联
    """
    order = models.ForeignKey(Order)
    webapp_user_id = models.IntegerField()  # WebApp用户的id
    promotion_id = models.IntegerField(default=0)  #促销id
    promotion_type = models.CharField(max_length=125, default='') #促销类型
    promotion_result_json = models.TextField(default='{}') #促销结果
    created_at = models.DateTimeField(auto_now_add=True) #创建时间
    integral_money = models.FloatField(default=0.0) # 积分抵扣钱数
    integral_count = models.IntegerField(default=0) # 使用的积分

    class Meta(object):
        db_table = 'mall_order_has_promotion'

    @property
    def promotion_result(self):
        data = json.loads(self.promotion_result_json)
        data['type'] = self.promotion_type
        return data


class OrderCardInfo(models.Model):
    """
    订单的微众卡信息
    """
    order_id = models.CharField(max_length=100)  # 订单号
    trade_id = models.CharField(max_length=100)  # 交易号
    used_card = models.CharField(max_length=1024)   # 订单使用的微众卡
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间

    class Meta(object):
        db_table = 'mall_order_card_info'
        verbose_name = '订单微众卡相关信息'
        verbose_name_plural = '订单微众卡相关信息'

GROUP_STATUS_ON = 0  # 团购进行中
GROUP_STATUS_OK = 1  # 团购成功
GROUP_STATUS_failure = 2  # 团购失败


class OrderHasGroup(models.Model):
    """
    <order, group>关联
    """
    order_id = models.CharField(max_length=100)  # 订单号(order中的order_id)
    group_id = models.CharField(max_length=100)
    activity_id = models.CharField(max_length=100)
    group_status = models.IntegerField(default=GROUP_STATUS_ON)
    webapp_user_id = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True) #创建时间
    webapp_id = models.CharField(max_length=20, verbose_name='店铺ID')  # webapp,订单成交的店铺id

    class Meta(object):
        db_table = 'mall_order_has_group'


#########################################################################
# 购物相关Model
#########################################################################
class ShoppingCart(models.Model):
    """
    购物车
    """
    webapp_user_id = models.IntegerField(default=0)  # WebApp用户
    product = models.ForeignKey(Product)  # 商品
    product_model_name = models.CharField(max_length=125)  # 商品规格名
    count = models.IntegerField(default=1)  # 商品数量
    created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

    class Meta(object):
        db_table = 'mall_shopping_cart'



#########################################################################
# 商品评价相关Model
#########################################################################
SCORE = (
    ('1', '1分'),
    ('2', '2分'),
    ('3', '3分'),
    ('4', '4分'),
    ('5', '5分'),
)

class OrderReview(models.Model):
    owner_id = models.IntegerField()  # 订单的主人
    order_id = models.IntegerField()  # 订单号
    member_id = models.IntegerField()  # 会员ID
    serve_score = models.CharField(  # 服务态度评分
        max_length=1,
        default='5'
    )
    deliver_score = models.CharField(  # 发货速度评分
        max_length=1,
        default='5'
    )
    process_score = models.CharField(  # 物流服务评分
        max_length=1,
        default='5'
    )

    class Meta(object):
        db_table = 'mall_order_review'


# 审核状态
PRODUCT_REVIEW_STATUS_BLOCKED = '-1'
PRODUCT_REVIEW_STATUS_UNPROCESSED = '0'
PRODUCT_REVIEW_STATUS_PASSED = '1'
PRODUCT_REVIEW_STATUS_PASSED_PINNED= '2'

PRODUCT_REVIEW_STATUS = (
    (PRODUCT_REVIEW_STATUS_BLOCKED,         '已屏蔽'),
    (PRODUCT_REVIEW_STATUS_UNPROCESSED,     '待审核'),
    (PRODUCT_REVIEW_STATUS_PASSED,          '已通过'),
    (PRODUCT_REVIEW_STATUS_PASSED_PINNED, '通过并置顶'),
)


class ProductReview(models.Model):
    """
    商品评价
    """
    member_id = models.IntegerField()
    owner_id = models.IntegerField()
    order_review = models.ForeignKey(OrderReview)
    order_id = models.IntegerField()  # 订单ID
    product_id = models.IntegerField()
    order_has_product = models.ForeignKey(OrderHasProduct)
    product_score = models.CharField(max_length=1, default='5')
    review_detail = models.TextField()  # 评价详情
    created_at = models.DateTimeField(auto_now=True)  # 评价时间
    top_time = models.DateTimeField(default=DEFAULT_DATETIME) # 置顶时间
    status = models.CharField(  # 审核状态
        max_length=2,
        choices=PRODUCT_REVIEW_STATUS,
        default='0')

    class Meta(object):
        db_table = 'mall_product_review'


class ProductReviewPicture(models.Model):
    """
    商品评价图片
    """
    product_review = models.ForeignKey(ProductReview)
    order_has_product = models.ForeignKey(OrderHasProduct)
    att_url = models.CharField(max_length=1024)  # 附件地址

    class Meta:
        verbose_name = "商品评价图片"
        verbose_name_plural = "商品评价图片"
        db_table = "mall_product_review_picture"




########################################################################
# OrderOperationLog:订单操作日志
########################################################################
class OrderOperationLog(models.Model):
    order_id = models.CharField(max_length=50)
    remark = models.TextField(default='')
    action = models.CharField(max_length=50)
    operator = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

    class Meta(object):
        db_table = 'mall_order_operation_log'
        verbose_name = '订单后台操作日志'
        verbose_name_plural = '订单后台操作日志'


########################################################################
# OrderStatusLog:订单状态日志
########################################################################
class OrderStatusLog(models.Model):
    order_id = models.CharField(max_length=50)
    from_status = models.IntegerField()
    to_status = models.IntegerField()
    remark = models.TextField(default='')
    operator = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

    class Meta(object):
        db_table = 'mall_order_status_log'
        verbose_name = '订单状态日志'
        verbose_name_plural = '订单状态日志'


########################################################################
# Supplier:供货商信息
########################################################################
class Supplier(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=16)  # 供货商名称
    responsible_person = models.CharField(max_length=100) # 供货商负责人
    supplier_tel = models.CharField(max_length=100) # 供货商电话
    supplier_address = models.CharField(max_length=256) # 供货商地址
    remark = models.CharField(max_length=256) # 备注
    is_delete = models.BooleanField(default=False)  # 是否已经删除
    created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

    class Meta(object):
        verbose_name = "供货商"
        verbose_name_plural = "供货商操作"
        db_table = "mall_supplier"





########################################################################
# MarketToolsIndustry: 行业信息
########################################################################
INDUSTR_IT = 0 #IT科技
INDUSTR_CONSUMER_GOODS = 1  #消费品
INDUSTR_AMOUNT = 2   #金融
INDUSTR_RESTAURANT = 3 #餐饮
INDUSTR_TRANSPORT = 4 #运输
INDUSTR_EDUCATION = 5 #教育education
INDUSTR_GOVERNMENT = 6 #government
INDUSTR_MEDICAL = 7 #medical
INDUSTR_TRAFFIC = 8 #traffic 交通
INDUSTR_ESTATE = 9 #state 房地产
INDUSTR_BUSINESS_SERVICE = 10 #business service 商业服务
INDUSTR_ENTERTAINMENT = 11 #entertainment 文体娱乐
INDUSTR_TRAVEL = 12 #旅游
INDUSTR_PRINTING = 13 #印刷 printing
INDUSTR_OTHER = 14 #其它
TYPE2INDUSTRY = {
    INDUSTR_IT: u'IT科技',
    INDUSTR_CONSUMER_GOODS: u'消费品',
    INDUSTR_AMOUNT: u'金融',
    INDUSTR_RESTAURANT: u'餐饮',
    INDUSTR_TRANSPORT: u'运输',
    INDUSTR_EDUCATION: u'教育',
    INDUSTR_GOVERNMENT: u'政府',
    INDUSTR_MEDICAL: u'医药',
    INDUSTR_TRAFFIC: u'交通',
    INDUSTR_ESTATE: u'房地产',
    INDUSTR_BUSINESS_SERVICE: u'商业服务',
    INDUSTR_ENTERTAINMENT: u'文体娱乐',
    INDUSTR_TRAVEL: u'旅游',
    INDUSTR_PRINTING: u'印刷',
    INDUSTR_OTHER: u'其他'
}
INDUSTRY2TYPE = {
    u'IT科技': INDUSTR_IT,
    u'消费品': INDUSTR_CONSUMER_GOODS,
    u'金融': INDUSTR_AMOUNT,
    u'餐饮': INDUSTR_RESTAURANT,
    u'运输': INDUSTR_TRANSPORT,
    u'教育': INDUSTR_EDUCATION,
    u'政府': INDUSTR_GOVERNMENT,
    u'医药': INDUSTR_MEDICAL,
    u'交通': INDUSTR_TRAFFIC,
    u'房地产': INDUSTR_ESTATE,
    u'商业服务': INDUSTR_BUSINESS_SERVICE,
    u'文体娱乐': INDUSTR_ENTERTAINMENT,
    u'旅游': INDUSTR_TRAVEL,
    u'印刷': INDUSTR_PRINTING,
    u'其他': INDUSTR_OTHER
}
class MarketToolsIndustry(models.Model):
    industry_type = models.IntegerField(default=INDUSTR_IT)
    industry_name = models.TextField() #模版id

    class Meta(object):
        db_table = 'market_tools_industry'
        verbose_name = '行业信息'
        verbose_name_plural = '行业信息'


########################################################################
# TemplateMessage: 模版消息  模版消息不同类型的行业模版格式不同
########################################################################
PAY_ORDER_SUCCESS = 0       #订单支付成功
PAY_DELIVER_NOTIFY = 1      #发货通知
COUPON_ARRIVAL_NOTIFY = 2   #优惠劵到账通知
COUPON_EXPIRED_REMIND = 3   #优惠劵过期提醒
class MarketToolsTemplateMessage(models.Model):
    industry = models.IntegerField(default=INDUSTR_IT)
    title = models.CharField(max_length=256) #标题
    send_point = models.IntegerField(default=PAY_ORDER_SUCCESS) #发送点
    attribute =models.TextField() #属性1  orderProductPrice:final_price,

    created_at = models.DateTimeField(auto_now_add=True) #添加时间

    class Meta(object):
        db_table = 'market_tools_template_message'
        verbose_name = '模板消息'
        verbose_name_plural = 'template_message'


########################################################################
# MarketToolsTemplateMessageDetail: 模版消息详情
########################################################################
MAJOR_INDUSTRY_TYPE = 0 #主营行业
DEPUTY_INDUSTRY_TYPE = 1 #副营行业
class MarketToolsTemplateMessageDetail(models.Model):
    owner = models.ForeignKey(User)
    template_message = models.ForeignKey(MarketToolsTemplateMessage)
    industry = models.IntegerField(default=INDUSTR_IT)
    template_id = models.TextField() #模版id
    first_text = models.CharField(max_length=1024)
    remark_text = models.CharField(max_length=1024)
    # type = models.SmallIntegerField(default=MAJOR_INDUSTRY_TYPE)
    # status = models.SmallIntegerField(default=0)
    type = models.IntegerField(default=MAJOR_INDUSTRY_TYPE)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True) #添加时间

    class Meta(object):
        db_table = 'market_tools_template_message_detail'
        verbose_name = '模板消息详情'
        verbose_name_plural = 'market_tools_template_message_detail'
        ordering = ['-status', 'type']


########################################################################
# MarketToolsTemplateMessageSendDetail: 模版消息发送信息
########################################################################
class MarketToolsTemplateMessageSendRecord(models.Model):
    owner = models.ForeignKey(User)
    template_id = models.TextField() #模版id
    member_id = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    order_id = models.CharField(max_length=200, default='')
    created_at = models.DateTimeField(auto_now_add=True) #添加时间

    class Meta(object):
        db_table = 'market_tools_template_message_send_record'
        verbose_name = '模板消息发送记录'
        verbose_name_plural = 'market_tools_template_message_send_record'


class MallOrderFromSharedRecord(models.Model):
    order_id = models.IntegerField()
    fmt = models.CharField(default='', max_length=255)
    url = models.CharField(default='', max_length=255)
    is_updated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

    class Meta(object):
        db_table = "mall_order_from_shared_record"


class WeizoomHasMallProductRelation(models.Model):
    owner = models.ForeignKey(User) # 微众系列的商户
    mall_id = models.IntegerField() # 供货商的owner_id
    mall_product_id = models.IntegerField() # 供货商商品
    weizoom_product_id = models.IntegerField() # 微众系列上架供货商的商品
    is_updated = models.BooleanField(default=False) # 是否需要更新
    is_deleted = models.BooleanField(default=False) # 供货商是否下架了商品
    sync_time = models.DateTimeField(auto_now_add=True) # 微众系列同步商品的时间
    delete_time = models.DateTimeField(auto_now=True) # 商品的失效时间
    created_at = models.DateTimeField(auto_now_add=True) # 添加时间

    class Meta(object):
        verbose_name = "微众系列同步其他商户商品的关系记录表"
        verbose_name_plural = "微众系列同步其他商户商品的关系"
        db_table = "mall_weizoom_has_mall_product_relation"


class ProductSearchRecord(models.Model):
    woid = models.IntegerField()
    webapp_user_id = models.IntegerField()
    is_deleted = models.BooleanField(default=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

    class Meta(object):
        verbose_name = "商品搜索记录"
        verbose_name_plural = "商品搜索记录"
        db_table = "mall_product_search_record"
