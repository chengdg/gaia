#coding: utf8
import copy
from datetime import datetime
import json

from eaglet.core.db import models
from db.account.models import User, UserProfile
from eaglet.core import watchdog
import settings
from business.mall.express import util as express_util

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
# 发货人相关Model
#########################################################################

class ShipperMessages(models.Model):
	"""	
	发货人信息
	"""
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=50) #发货人
	tel_number = models.CharField(max_length=15) #手机号
	province = models.CharField(max_length=50) #发货地区省
	city = models.CharField(max_length=50) #市
	district = models.CharField(max_length=512) #区/县
	address = models.CharField(max_length=256) #详细地址
	postcode = models.CharField(max_length=50) #邮政编码
	company_name = models.CharField(max_length=50) #单位名称
	remark = models.TextField(null=True) #备注
	is_active = models.BooleanField(default=False) #是否默认
	is_deleted = models.BooleanField(default=False) #是否删除
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'mall_shipper_messages'

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
	supplier_id = models.IntegerField(default=0) # 供货商的id

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


# #######        供货商实现        ####
# 五五分成
SUPPLIER_TYPE_DIVIDE = 0
# 零售返点
SUPPLIER_TYPE_RETAIL = 1
# 固定低价
SUPPLIER_TYPE_FIXED = 2
# 普通供货商
SUPPLIER_TYPE_NORMAL = -1

# 结算账期  1【自然月】   2【15天】   3【自然周】
SUPPLIER_SETTLEMENT_PERIOD_MONTH = 1
SUPPLIER_SETTLEMENT_PERIOD_15TH_DAY = 2
SUPPLIER_SETTLEMENT_PERIOD_WEEK = 3

class Supplier(models.Model):
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=200)  # 供货商名称
	responsible_person = models.CharField(max_length=100)  # 供货商负责人
	supplier_tel = models.CharField(max_length=100)  # 供货商电话
	supplier_address = models.CharField(max_length=256)  # 供货商地址
	remark = models.CharField(max_length=256)  # 备注
	type = models.IntegerField(default=SUPPLIER_TYPE_NORMAL)
	is_delete = models.BooleanField(default=False)  # 是否已经删除
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间
	settlement_period = models.IntegerField(default=SUPPLIER_SETTLEMENT_PERIOD_MONTH)

	class Meta(object):
		verbose_name = "供货商"
		verbose_name_plural = "供货商操作"
		db_table = "mall_supplier"


class SupplierPostageConfig(models.Model):
	supplier_id = models.IntegerField(default=0)
	product_id = models.IntegerField(default=0)
	condition_type = models.CharField(
		max_length=25,
		default='money')  # 免邮条件类型, 共有'count', 'money'两种
	condition_money = models.DecimalField(max_digits=65, decimal_places=2, null=True) #免邮的消费金额
	condition_count = models.IntegerField(default=0)  # 免邮商品数量
	postage = models.DecimalField(max_digits=65, decimal_places=2, null=True) #邮费
	status = models.BooleanField(default=True) # 是否启用邮费配置
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

	class Meta(object):
		db_table = 'mall_supplier_postage_config'
		verbose_name = '供货商邮费配置'
		verbose_name_plural = '供货商邮费配置'


class SupplierDivideRebateInfo(models.Model):
	"""
	供货商五五分成信息(不一定是五成)--目前只有首月五五分成,以后可能扩展成,不同额度不同返点.
	"""
	# 供货商id
	supplier_id = models.IntegerField()
	# 钱额度
	divide_money = models.IntegerField()
	# 基础返点
	basic_rebate = models.IntegerField()
	# 在此额度内返点
	rebate = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	is_deleted = models.BooleanField(default=False)

	class Meta(object):
		db_table = 'supplier_divide_rebate_info'


class SupplierRetailRebateInfo(models.Model):
	"""
	零售返点的供货商的返点信息(包括团购)
	"""
	# 供货商id
	supplier_id = models.IntegerField()
	# 平台id(如果支持团购) 0的表示改供货商的基础扣点; 0的默认值表示改供货商的基础扣点
	# 如果有owner_id说明该扣点是属于团购扣点
	owner_id = models.IntegerField(default=0)
	# 扣点
	rebate = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	is_deleted = models.BooleanField(default=False)

	class Meta(object):
		db_table = 'supplier_retail_rebate_info'



# 一级分类
FIRST_CLASSIFICATION = 1
# 二级分类
SECONDARY_CLASSIFICATION = 2
# 分类上线（类似于未删除）
CLASSIFICATION_ONLINE = 1
# 分类下线（类似于删除）
CLASSIFICATION_OFFLINE = 0
class Classification(models.Model):
	"""
	商品分类
	"""
	owner_id = models.IntegerField(default=0)
	name = models.CharField(max_length=1024) #分类名
	level = models.IntegerField(default=FIRST_CLASSIFICATION) #分类等级
	status = models.IntegerField(default=CLASSIFICATION_ONLINE)
	father_id = models.IntegerField(default=-1) #父级分组id
	product_count = models.IntegerField(default=0) #分类商品数量
	note = models.CharField(max_length=1024, default='') #分组备注
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

	class Meta(object):
		verbose_name = "商品分类"
		verbose_name_plural = "商品分类"
		db_table = "mall_classification"


class ClassificationHasProduct(models.Model):
	"""
	商品分类拥有商品的关系表
	"""
	classification = models.ForeignKey(Classification)
	product_id = models.IntegerField(default=-1)
	woid = models.IntegerField(default=-1)
	display_index = models.IntegerField(default=-1)
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

	class Meta(object):
		verbose_name = "商品分类与商品的关系"
		verbose_name_plural = "商品分类与商品的关系"
		db_table = "mall_classification_has_product"
		

class ClassificationQualification(models.Model):
	"""
	商品分类配置的特殊资质
	"""
	classification = models.ForeignKey(Classification)
	name = models.CharField(max_length=48, default='') #资质名称
	created_at = models.DateTimeField(auto_now_add=True) #创建时间

	class Meta(object):
		db_table = 'mall_classification_qualification'

class ClassificationHasLabel(models.Model):
	"""
	商品分类有什么标签
	"""
	classification = models.ForeignKey(Classification)
	label_id = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'mall_classification_has_label'


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


PRODUCT_ZONE_NO_LIMIT = 0 #不限制
PRODUCT_ZONE_FORBIDDEN_SALE = 1 #禁售
PRODUCT_ZONE_ONLY_SALE = 2 #仅售

PRODUCT_STATUS = {
	'NOT_YET': 0, #尚未提交审核
	'SUBMIT': 1, #提交审核
	'REFUSED': 2 #驳回
}

class Product(models.Model):
	"""
	商品

	表名：mall_product
	"""
	owner = models.ForeignKey(User, related_name='user-product')
	name = models.CharField(max_length=256)  # 商品名称
	physical_unit = models.CharField(default='', max_length=256)  # 计量单位
	price = models.FloatField(default=0.0)  # 商品价格
	introduction = models.CharField(max_length=256, default='')  # 商品简介
	weight = models.FloatField(default=0.0)  # 重量
	thumbnails_url = models.CharField(max_length=1024, default='')  # 商品缩略图
	pic_url = models.CharField(max_length=1024, default='')  # 商品图
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
	purchase_price = models.FloatField(default=0.0) # 进货价格(结算价)
	is_enable_bill = models.BooleanField(default=False)  # 商品是否开具发票
	is_delivery = models.BooleanField(default=False) # 是否勾选配送时间
	buy_in_supplier = models.BooleanField(default=False) # 记录下单位置是商城还是供货商，0是商城1是供货商
	limit_zone_type = models.IntegerField(default=PRODUCT_ZONE_NO_LIMIT) # 0不限制 1禁售 2仅售
	limit_zone = models.IntegerField(default=0) # 限制地区的模板id

	#待审核商品
	is_pre_product = models.BooleanField(default=False)  # 是否待审核商品
	status = models.IntegerField(default=PRODUCT_STATUS['NOT_YET'])  # 审核状态
	refuse_reason = models.TextField(default='')  # 驳回原因
	is_updated = models.BooleanField(default=False) #是否已更新
	is_accepted = models.BooleanField(default=True)  # 审核是否已通过

	class Meta(object):
		db_table = 'mall_product'

class CategoryHasProduct(models.Model):
	"""
	<category, product>关系
	"""
	product = models.ForeignKey(Product)
	category = models.ForeignKey(ProductCategory)
	display_index = models.IntegerField(default=9999999, null=True)  # 分组商品排序
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


ORDER_PAY_ACTION = {
	'name': u'支付',
	'action': 'pay',
	'class_name': 'xa-pay',
	'button_class': 'btn-success'
}
ORDER_SHIP_ACTION = {
	'name': u'发货',
	'action': 'ship',
	'class_name': 'xa-order-delivery',
	'button_class': 'btn-danger'
}
ORDER_FINISH_ACTION = {
	'name': u'标记完成',
	'action': 'finish',
	'class_name': 'xa-finish',
	'button_class': 'btn-success'
}
ORDER_CANCEL_ACTION = {
	'name': u'取消订单',
	'action': 'cancel',
	'class_name': 'xa-cancelOrder',
	'button_class': 'btn-danger'
}
ORDER_REFUNDIND_ACTION = {
	'name': u'申请退款',
	'action': 'return_pay',
	'class_name': 'xa-refund',
	'button_class': 'btn-danger'
}
ORDER_UPDATE_PRICE_ACTION = {
	'name': u'修改价格',
	'action': 'update_price',
	'class_name': 'xa-update-price',
	'button_class': 'btn-danger'
}
ORDER_UPDATE_EXPREDSS_ACTION = {
	'name': u'修改物流',
	'action': 'update_express',
	'class_name': 'xa-order-delivery',
	'button_class': 'btn-danger'
}
ORDER_REFUND_SUCCESS_ACTION = {
	'name': u'退款成功',
	'action': 'return_success',
	'class_name': 'xa-refundSuccess',
	'button_class': 'btn-danger'
}

PAY_INTERFACE_ALIPAY = 0
PAY_INTERFACE_TENPAY = 1
PAY_INTERFACE_WEIXIN_PAY = 2
PAY_INTERFACE_COD = 9
PAY_INTERFACE_PREFERENCE = 10
PAY_INTERFACE_BEST_PAY = 11
PAY_INTERFACE_KANGOU = 12
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
	PAY_INTERFACE_WEIZOOM_COIN: u"微众卡支付",
	PAY_INTERFACE_BEST_PAY: u"翼支付",
	PAY_INTERFACE_KANGOU: u"看购支付"
}
PAYNAME2TYPE = {
	u'优惠抵扣':PAY_INTERFACE_PREFERENCE,
	u'支付宝': PAY_INTERFACE_ALIPAY,
	u'财付通': PAY_INTERFACE_TENPAY,
	u'微信支付': PAY_INTERFACE_WEIXIN_PAY,
	u'货到付款': PAY_INTERFACE_COD,
	u"微众卡支付": PAY_INTERFACE_WEIZOOM_COIN
}
PAYTYPE2STR = {
	-1: u'unknown',
	PAY_INTERFACE_PREFERENCE: u'preference',
	PAY_INTERFACE_ALIPAY: u'alipay',
	PAY_INTERFACE_TENPAY: u'tenpay',
	PAY_INTERFACE_WEIXIN_PAY: u'weixin_pay',
	PAY_INTERFACE_COD: u'cod',
	PAY_INTERFACE_WEIZOOM_COIN: u"weizoom_coin",
	PAY_INTERFACE_BEST_PAY: u"best_pay",
	PAY_INTERFACE_KANGOU: u"kangou_pay"
}

PAYSTR2TYPE = {
	u'unknown': -1,
	u'preference': PAY_INTERFACE_PREFERENCE,
	u'alipay': PAY_INTERFACE_ALIPAY,
	u'tenpay': PAY_INTERFACE_TENPAY,
	u'weixin_pay': PAY_INTERFACE_WEIXIN_PAY,
	u'cod': PAY_INTERFACE_COD,
	u"weizoom_coin": PAY_INTERFACE_WEIZOOM_COIN,
	u"best_pay": PAY_INTERFACE_BEST_PAY,
	u"kangou_pay": PAY_INTERFACE_KANGOU
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

V2 = 0
WEIXIN_PAY_V2 = V2
V3 = 1
WEIXIN_PAY_V3 = V3
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




ALIPAY_SIGN_TYPES = (
		('MD5', 'MD5'),
		('0001', '0001(RSA)')
	)
ALI_PAY_V2 = '0'
ALI_PAY_V5 = '1'

ALIPAY_PAY_VERSION = (
	(ALI_PAY_V2, 'v2'),
	(ALI_PAY_V5, 'v5')
)
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
	purchase_price = models.FloatField(default=0.0)  # 商品结算价格
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

MEANINGFUL_WORD2ORDER_STATUS = {
	"created": ORDER_STATUS_NOT,
	"cancelled": ORDER_STATUS_CANCEL,
	"paid": ORDER_STATUS_PAYED_NOT_SHIP,
	"shipped": ORDER_STATUS_PAYED_SHIPED,
	"finished": ORDER_STATUS_SUCCESSED,
	"refunding": ORDER_STATUS_REFUNDING,
	"refunded": ORDER_STATUS_REFUNDED,

}
ORDER_STATUS2MEANINGFUL_WORD = {
	ORDER_STATUS_NOT: "created",
	ORDER_STATUS_CANCEL: "cancelled",
	ORDER_STATUS_PAYED_NOT_SHIP: "paid",
	ORDER_STATUS_PAYED_SHIPED: "shipped",
	ORDER_STATUS_SUCCESSED: "finished",
	ORDER_STATUS_REFUNDING: "refunding",
	ORDER_STATUS_REFUNDED: "refunded",
	ORDER_STATUS_GROUP_REFUNDING: "refunding",
	ORDER_STATUS_GROUP_REFUNDED: "refunded"
}



# 权重小的优先
# 订单状态优先级由低到高排序为：
# 待支付->待发货->已发货->退款中->已完成->退款完成->已取消
ORDER_STATUS2DELIVERY_ITEM_WEIGHT = {
	ORDER_STATUS_NOT: 1,
	ORDER_STATUS_PAYED_NOT_SHIP: 2,
	ORDER_STATUS_PAYED_SHIPED: 3,
	ORDER_STATUS_REFUNDING: 4,
	ORDER_STATUS_SUCCESSED: 5,
	ORDER_STATUS_REFUNDED:6,
	ORDER_STATUS_CANCEL: 7
}

DELIVERY_ITEM_WEIGHT2ORDER_STATUS = {
	1: ORDER_STATUS_NOT,
	2: ORDER_STATUS_PAYED_NOT_SHIP,
	3: ORDER_STATUS_PAYED_SHIPED,
	4: ORDER_STATUS_REFUNDING,
	5: ORDER_STATUS_SUCCESSED,
	6: ORDER_STATUS_REFUNDED,
	7: ORDER_STATUS_CANCEL
}




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
	buyer_name = models.CharField(max_length=100)  # 购买人姓名,已废弃
	buyer_tel = models.CharField(max_length=100, default='')  # 购买人电话,已废弃
	ship_name = models.CharField(max_length=100)  # 收货人姓名
	ship_tel = models.CharField(max_length=100)  # 收货人电话
	ship_address = models.CharField(max_length=200)  # 收货人地址
	area = models.CharField(max_length=100) # 收货人地区编码
	status = models.IntegerField(default=ORDER_STATUS_NOT)  # 订单状态
	order_source = models.IntegerField(default=ORDER_SOURCE_OWN)  # 订单来源 0本店 1商城 已废弃，新订单使用默认值兼容老数据，已废弃
	bill_type = models.IntegerField(default=ORDER_BILL_TYPE_NONE)  # 发票类型 2016-01-20重新启用by Eugene
	bill = models.CharField(max_length=100, default='')  # 发票信息 2016-01-20重新启用by Eugene
	remark = models.TextField(default='')  # 备注
	supplier_remark = models.TextField(default='')  # 供应商备注
	product_price = models.FloatField(default=0.0)  # 商品金额（应用促销后的商品总价），已废弃
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
	type = models.CharField(max_length=50, default=PRODUCT_DEFAULT_TYPE)  # 产品的类型，微众商城启用
	integral_each_yuan = models.IntegerField(verbose_name='一元是多少积分', default=-1)
	reason = models.CharField(max_length=256, default='')  # 取消订单原因，已废弃
	update_at = models.DateTimeField(auto_now=True)  # 订单信息更新时间 2014-11-11
	weizoom_card_money = models.FloatField(default=0.0)  # 微众卡抵扣金额
	promotion_saved_money = models.FloatField(default=0.0)  # 促销优惠金额（只在含限时抢购商品时产生）
	edit_money = models.FloatField(default=0.0)  # 商家修改差价：final_price（计算公式得） - final_price（商家修改成的）= edit_money
	origin_order_id = models.IntegerField(default=0) # 订单的主键id（即母订单主键id
	# origin_order_id=-1表示有子订单，>0表示有父母订单，=0为默认数据
	supplier = models.IntegerField(default=0) # 订单供货商，用于微众精选拆单，对应mall_supplier表的主键id
	is_100 = models.BooleanField(default=True) # 是否是快递100能够查询的快递
	delivery_time = models.CharField(max_length=50, default='')  # 配送时间字符串
	is_first_order = models.BooleanField(default=False) # 是否是用户的首单
	supplier_user_id = models.IntegerField(default=0) # 订单供货商user的id，用于系列拆单
	total_purchase_price = models.FloatField(default=0)  # 总订单采购价格
	# bid = models.CharField(max_length=100)  # 订单号
	member_card_money = models.FloatField(
		default=0.0)  # 会员卡抵扣金额  alter table mall_order add column member_card_money float default 0;

	class Meta(object):
		db_table = 'mall_order'
		verbose_name = '订单'
		verbose_name_plural = '订单'


# added by chuter
########################################################################
# OrderPaymentInfo: 订单支付信息,已废弃
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
	grade_discounted_money = models.FloatField(default=0.0)  # 折扣金额,会员等级价折扣金额
	integral_sale_id = models.IntegerField(default=0) #使用的积分应用的id
	origin_order_id = models.IntegerField(default=0) # 原始(母)订单id，用于微众精选拆单
	purchase_price = models.FloatField(default=0)  # 采购单价

	class Meta(object):
		db_table = 'mall_order_has_product'


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


class OrderHasRefund(models.Model):
		origin_order_id = models.IntegerField(default=0)  # 原始订单id，用于微众精选拆单
		delivery_item_id = models.IntegerField(default=0)  # 对应出货单主键id
		cash = models.FloatField(default=0.0)
		weizoom_card_money = models.FloatField(default=0.0)  # 微众卡抵扣金额
		integral = models.IntegerField(default=0)  # 积分
		integral_money = models.FloatField(default=0)  # 积分对应金额,退款当时的
		coupon_money = models.FloatField(default=0)  # 优惠券金额
		created_at = models.DateTimeField(auto_now_add=True)  # 添加时间
		total = models.FloatField(default=0)  # 积分
		finished = models.BooleanField(default=False)  # 是否退款完成
		member_card_money = models.FloatField(default=0.0)  # 会员卡抵扣金额

		class Meta(object):
			db_table = 'mall_order_has_refund'
			verbose_name = '子订单退款信息'
			verbose_name_plural = '子订单退款信息'

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
MESSAGE_STATUS_ON = 1 # 启用
MESSAGE_STATUS_OFF = 0 # 不启用
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


PP_STATUS_OFF = 0 #商品下架(待售)
PP_STATUS_ON = 1 #商品上架
PP_STATUS_DELETE = -1 #商品删除 不在当前供应商显示
PP_STATUS_ON_POOL = 2 #商品在商品池中显示

PP_TYPE_SYNC = 1 #从其他商品池同步而来的商品
PP_TYPE_CREATE = 2 #商户自身创建的商品
class ProductPool(models.Model):
	woid = models.IntegerField() #自营平台woid
	product_id = models.IntegerField() #商品管理上传的商品id
	status = models.IntegerField(default=PP_STATUS_ON_POOL) #商品状态
	type = models.IntegerField(default=PP_TYPE_SYNC) #商品类型
	display_index = models.IntegerField()  # 显示的排序
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间
	sync_at = models.DateTimeField(null=True, blank=True)  # 上架时间
	# 是否处理过cps推广
	is_cps_promotion_processed = models.BooleanField(default=False)

	class Meta(object):
		verbose_name = "商品池商品"
		verbose_name_plural = "商品池商品"
		db_table = "product_pool"


class PandaHasProductRelation(models.Model):
	"""
	panda同步过来的商品中间关系
	"""
	panda_product_id = models.IntegerField()
	weapp_product_id = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

	class Meta(object):
			verbose_name = "panda同步过来的商品中间关系"
			verbose_name_plural = "panda同步过来的商品中间关系"
			db_table = "panda_has_product_relation"


class ProductLimitPurchasePrice(models.Model):
	"""
	8000商品限时结算价格
	"""
	product_id = models.IntegerField(),
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()

	class Meta:
		verbose_name = "商品池商品"
		verbose_name_plural = "商品池商品"
		db_table = "product_limit_purchase_price"

class WxCertSettings(models.Model):
	"""
	存储微信每个帐号的证书文件地址
	"""
	owner = models.ForeignKey(User)  # 活动所有者
	cert_path = models.CharField(default="", max_length=1024)  # 证书存储路径
	up_cert_path = models.CharField(default="", max_length=2048)  # 证书又拍云存储路径

	key_path = models.CharField(default="", max_length=1024)  # 证书key存储路径
	up_key_path = models.CharField(default="", max_length=2048)  # 证书key又拍云存储路径

	class Meta(object):
		verbose_name = "微信证书文件地址"
		verbose_name_plural = "微信证书文件地址"
		db_table = "mall_weixin_cert"


########################################################################
# Workspace: 一个工作空间，可包含多个Project
########################################################################
class Workspace(models.Model):
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=50)  # 名字
	inner_name = models.CharField(max_length=50)  # 内部名字
	data_backend = models.CharField(max_length=50)  # 数据源
	source_workspace_id = models.IntegerField(default=0)  # 源workspace的id
	template_project_id = models.IntegerField(default=0)  # 模板project的id
	template_name = models.CharField(max_length=125, default='default')  # 首页模板名
	backend_template_name = models.CharField(max_length=125, default='default')  # 非首页模板名
	is_deleted = models.BooleanField(default=False)  # 是否已删除
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间
	display_index = models.IntegerField(default=1)  # 显示排序

	@staticmethod
	def get_market_tool_workspace(owner, market_tool_name):
		'''market_tool_name的格式为: market_tool:vote'''
		workspace = Workspace()
		workspace.owner = owner
		workspace.data_backend = market_tool_name
		return workspace

	@staticmethod
	def get_app_workspace(owner, app_name):
		'''app的格式为: app:app1'''
		workspace = Workspace()
		workspace.owner = owner
		workspace.data_backend = app_name
		return workspace

	class Meta(object):
		db_table = 'webapp_workspace'
		verbose_name = 'APP'
		verbose_name_plural = 'APP'


class Project(models.Model):
	"""
	Project: 一个项目，可包含多个Page
	"""
	owner = models.ForeignKey(User)
	workspace = models.ForeignKey(Workspace)
	name = models.CharField(max_length=50) #项目名
	inner_name = models.CharField(max_length=50) #内部名字
	type = models.CharField(max_length=50) #项目类型
	css = models.TextField() #css内容
	pagestore = models.CharField(max_length=50, default='mongo') #使用的pagestore类型
	source_project_id = models.IntegerField(default=0) #源project的id
	datasource_project_id = models.IntegerField(default=0) #提供数据源的project
	template_project_id = models.IntegerField(default=0) #模板project的id
	is_enable = models.BooleanField(default=False) #是否开启模板项目
	cover_name = models.CharField(default='', max_length=50) #封面图片名
	site_title = models.CharField(default='', max_length=50) #模板项目名
	is_active = models.BooleanField(default=False) #是否启用该微页面
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	@staticmethod
	def get_market_tool_project(owner, market_tool_name):
		'''market_tool_name的格式为: market_tool:vote'''
		project = Project()
		project.id = '%s:%d' % (market_tool_name, owner.id)
		project.owner = owner
		project.type = 'market_tool'
		return project

	@staticmethod
	def get_app_project(owner, app_name):
		'''app_name的格式为: apps:vote'''
		project = Project()
		project.id = '%s:%d' % (app_name, owner.id)
		project.owner = owner
		project.type = 'app'
		return project

	class Meta(object):
		db_table = 'webapp_project'
		verbose_name = '项目'
		verbose_name_plural = '项目'

#########################################################################
# ImageGroup：图片分组
#########################################################################
class ImageGroup(models.Model):
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=125, default='')  # 图片分组名
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

	class Meta(object):
		db_table = 'mall_image_group'
		verbose_name = '商城图片分组'
		verbose_name_plural = '商城图片分组'


#########################################################################
# Image：图片
#########################################################################
class Image(models.Model):
	owner = models.ForeignKey(User)
	group = models.ForeignKey(ImageGroup)
	title = models.CharField(max_length=125, default='')  # 图片标题
	url = models.CharField(max_length=256, default='')  # 图片url
	width = models.IntegerField()  # width
	height = models.IntegerField()  # height
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

	class Meta(object):
		db_table = 'mall_image'
		verbose_name = '商城图片'
		verbose_name_plural = '商城图片'


PLACE_ORDER = 0  # 下单
PAY_ORDER = 1  # 付款
SHIP_ORDER = 2  # 发货
SUCCESSED_ORDER = 3  # 完成
CANCEL_ORDER = 4  # 已取消
class UserOrderNotifySettings(models.Model):
	"""
	发送订单邮件信息配置
	"""
	user = models.ForeignKey(User)
	emails = models.TextField(default='')  # '|'分割
	black_member_ids = models.TextField(default='')  # '|'分割，会员id
	status = models.IntegerField(default=0)
	is_active = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'user_order_notify_setting'

class ProductLimitZoneTemplate(models.Model):
	"""
	商品仅售和禁售的模板
	"""
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=64)  # 模板名称
	provinces = models.CharField(max_length=1024) # 所有省id
	cities = models.CharField(max_length=4096) # 所有城市id
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

	class Meta(object):
		verbose_name = "商品仅售和禁售的模板"
		verbose_name_plural = "商品仅售和禁售的模板"
		db_table = "mall_product_limit_zone_template"

class ProductLabelGroup(models.Model):
	"""
	商品标签的分类（分组）
	"""
	owner_id = models.IntegerField(default=0)
	name = models.CharField(max_length=256, null=True)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'mall_product_label_group'
		verbose_name = '标签分类'


class ProductLabel(models.Model):
	"""
	商品标签
	"""
	label_group_id = models.IntegerField(default=0)
	owner_id = models.IntegerField(default=0)
	name = models.CharField(max_length=256)
	created_at = models.DateTimeField(auto_now_add=True)
	is_deleted = models.BooleanField(default=False)

	class Meta(object):
		db_table = 'mall_product_label'
		verbose_name = '标签'

class ProductHasLabel(models.Model):
	"""
	商品有哪些标签
	"""
	product_id = models.IntegerField(null=False)
	label_id = models.IntegerField(null=False)
	# -1表示改标签是商品自己的标签不是分类的标签
	classification_id = models.IntegerField(default=-1)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'mall_product_has_label'


#status: 0未完成,1完成,2失败
#type: 0会员,1所有订单 2商品评价导出 3财务审核 4在售商品 5待售商品
#########################################################################
# ExportJob: 导出任务
#########################################################################
WORD2EXPORT_JOB_TYPE = {
	'all_orders': 1,
	'financial_audit_orders': 3
}

class ExportJob(models.Model):
	woid = models.IntegerField()
	type = models.IntegerField(default=0)
	status = models.BooleanField(default=False) # 其实是表示是否完成的bool
	processed_count = models.IntegerField() # 已处理数量
	count = models.IntegerField()   # 总数量
	is_download = models.BooleanField(default=False, verbose_name='是否下载')
	param = models.CharField(max_length=1024)
	file_path = models.CharField(max_length=256)
	update_at = models.DateTimeField(verbose_name='更新时间', auto_now=True)
	created_at = models.DateTimeField(verbose_name='创建时间')

	class Meta(object):
		db_table = 'export_job'


PROMOTING = 1  # 推广中
PROMOTE_OVER = 2  # 推广结束


class PromoteDetail(models.Model):
	"""
	推广信息
	"""
	product_id = models.IntegerField()
	# 推广状态 （未推广，推广中，已结束）   推广设置中展示：未推广，已结束。推广明细中：推广中，已结束
	promote_status = models.IntegerField(default=PROMOTING)

	promote_money = models.FloatField(default=0, help_text=u'推广费用/件')
	promote_stock = models.IntegerField(default=1, help_text=u'推广库存')
	promote_time_from = models.DateTimeField(auto_now_add=True)
	promote_time_to = models.DateTimeField(auto_now_add=True)
	promote_sale_count = models.IntegerField(default=0, help_text=u'推广销量')
	promote_total_money = models.FloatField(default=0, help_text=u'推广费用总费用')
	is_new = models.BooleanField(default=True, help_text=u'是否已读')  # 是否已读
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'mall_promote_detail'
