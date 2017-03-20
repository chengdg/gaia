# -*- coding: utf-8 -*-
import json

from eaglet.decorator import cached_context_property
from eaglet.utils.resource_client import Resource

from business import model as business_model
from business.coupon.coupon_repository import CouponRepository
from business.coupon.coupon_rule_repository import CouponRuleRepository
from business.deprecated.wepage_project_repository import WepageProjectRepository
from business.member.member_grade_repository import MemberGradeRepository
from business.member.member_repository import MemberRepository
from business.order.delivery_item_repository import DeliveryItemRepository
from business.order.order_export_job_repository import OrderExportJobRepository
from business.export.export_job_repository import ExportJobRepository
from business.order.order_repository import OrderRepository
from business.order.config.order_config_repository import OrderConfigRepository
from db.account import models as account_model


from business.product.product_shelf import ProductShelf
from business.product.product_pool import ProductPool
from business.product.global_product_repository import GlobalProductRepository
from business.product.property_template.property_template_repository import PropertyTemplateRepository
from business.product.model.product_model_property_repository import ProductModelPropertyRepository

from business.mall.category.category_repository import CategoryRepository
from business.mall.image_group.image_group_repository import ImageGroupRepository
from business.mall.pay.pay_interface_repository import PayInterfaceRepository
from business.mall.logistics.postage_config_repository import PostageConfigRepository
from business.mall.logistics.shipper_repository import ShipperRepository
from business.mall.logistics.express_bill_account_repository import ExpressBillAccountRepository
from business.mall.logistics.express_delivery_repository import ExpressDeliveryRepository
from business.mall.logistics.limit_zone_repository import LimitZoneRepository
from business.mall.logistics.province_city_repository import ProvinceCityRepository
from business.mall.config.mall_config_repository import MallConfigRepository
from business.mall.notify.notification_repository import NotificationRepository
from business.mall.supplier.supplier_repository import SupplierRepository

from business.mall.product_classification.product_classification_repository import ProductClassificationRepository
from business.mall.product_label.product_label_repository import ProductLabelRepository
from business.mall.product_label.product_label_group_repository import ProductLabelGroupRepositroy

from business.mall.promotion.promotion_repository import PromotionRepository

from business.weixin.material_repository import MaterialRepository
from business.weixin.weixin_news_repository import WeixinNewsRepository
from business.mall.template_message.template_message_detail_repository import TemplateMessageDetailRepository
from business.weixin.mpuser_access_token_repository import MpuserAccessTokenRepository
from business.member.social_account_repository import SocialAccountRepository



class Corporation(business_model.Model):
	"""
	商家
	"""
	__slots__ = (
		'id',
		'name',
		'type',
		'corp_type',
		'webapp_id',
		'username',

		'company_name',
		'settlement_type',
		'divide_rebate',
		'min_cps_profit',
		'clear_period',
		'customer_from',
		'max_product_count',
		'classification_ids',
		'risk_money',
		'rules', #社群商品分发规则

		'status',
	)

	def __init__(self, owner_id):
		business_model.Model.__init__(self)
		self.id = owner_id
		self.company_name = ''
		self.status = 0
		print owner_id
		if owner_id:
			_account_user_profile = account_model.UserProfile.select().dj_where(user_id=owner_id).first()
			self.webapp_id = _account_user_profile.webapp_id

			if _account_user_profile.webapp_type == account_model.WEBAPP_TYPE_MALL:
				self.type = 'normal'
			elif _account_user_profile.webapp_type == account_model.WEBAPP_TYPE_WEIZOOM_MALL:
				self.type = 'self_run'
				self.corp_type = 'community'
			elif _account_user_profile.webapp_type == account_model.WEBAPP_TYPE_WEIZOOM:
				self.type = 'weizoom_corp'
				self.corp_type = 'weizoom'
			elif _account_user_profile.webapp_type == account_model.WEBAPP_TYPE_MULTI_SHOP:
				self.type = 'multi_shop'
			elif _account_user_profile.webapp_type == account_model.WEBAPP_TYPE_SUPPLIER:
				self.type = 'supplier'
				self.corp_type = 'supplier'
			else:
				self.type = 'unknown'
				self.corp_type = 'unknown'

			_user = account_model.User.select().dj_where(id=owner_id).first()
			self.username = _user.username
		else:
			self.webapp_id = 0
			self.type = 'normal'

	@cached_context_property
	def details(self):
		"""
		填充corp详情
		区分供货商和采购商(社群)
		"""
		if self.is_community():
			resp = Resource.use('wcas').get({
				'resource': 'corp.community',
				'data': {
					'corp_id': self.id
				}
			})
			community_info = resp['data']
			if community_info:
				self.name = community_info['name']
				self.settlement_type = community_info['settlement_type']
				self.divide_rebate = community_info['divide_rebate']
				self.risk_money = community_info['risk_money']
				self.rules = [{
				  	'config_type': rule['config_type'],
				  	'config_property': rule['config_property'],
				  	'config_value': rule['config_value']
				} for rule in community_info['rules']]
		elif self.is_supplier():
			resp = Resource.use('wcas').get({
				'resource': 'corp.supplier',
				'data': {
					'corp_id': self.id
				}
			})
			supplier_info = resp['data']
			if supplier_info:
				self.name = supplier_info['name']
				self.company_name = supplier_info['company_name']
				self.settlement_type = supplier_info['settlement_type']
				self.divide_rebate = supplier_info['divide_rebate']
				self.min_cps_profit = supplier_info['min_cps_profit']
				self.clear_period = supplier_info['clear_period']
				self.customer_from = supplier_info['customer_from']
				self.max_product_count = int(supplier_info['max_product_count'])
				self.classification_ids = supplier_info['classification_ids']
				self.status = supplier_info['status']
		else:
			pass

		return self

	def is_self_run_platform(self):
		"""
		判断是否是自营平台
		"""
		return self.type == 'self_run'

	def is_supplier(self):
		"""
		判断是否供货商
		"""
		return self.corp_type == 'supplier'

	def is_community(self):
		"""
		判断是否社群
		"""
		return self.corp_type == 'community'

	def is_weizoom_corp(self):
		"""
		判断是否是微众公司账号
		"""
		return self.type == 'weizoom_corp'

	def is_multi_shop(self):
		"""
		判断是否是多门店公司
		"""
		return self.type == 'multi_shop'

	@property
	def insale_shelf(self):
		product_shelf = ProductShelf.get({
			"corp": self,
			'type': 'in_sale'
		})

		return product_shelf

	@property
	def forsale_shelf(self):
		product_shelf = ProductShelf.get({
			"corp": self,
			'type': 'for_sale'
		})

		return product_shelf

	@property
	def product_pool(self):
		return ProductPool.get_for_corp({
			"corp": self
		})

	@property
	def global_product_repository(self):
		return GlobalProductRepository.get(self)

	@property
	def category_repository(self):
		return CategoryRepository.get(self)

	@property
	def image_group_repository(self):
		return ImageGroupRepository.get(self)

	@property
	def product_property_template_repository(self):
		return PropertyTemplateRepository.get(self)

	@property
	def product_model_property_repository(self):
		return ProductModelPropertyRepository.get(self)

	@property
	def order_repository(self):
		return OrderRepository.get({'corp': self})

	@property
	def delivery_item_repository(self):
		return DeliveryItemRepository.get({'corp': self})

	@property
	def pay_interface_repository(self):
		return PayInterfaceRepository(self)

	@property
	def postage_config_repository(self):
		return PostageConfigRepository(self)

	@property
	def shipper_repository(self):
		return ShipperRepository(self)

	@property
	def express_bill_account_repository(self):
		return ExpressBillAccountRepository(self)

	@property
	def mall_config_repository(self):
		return MallConfigRepository(self)

	@property
	def express_delivery_repository(self):
		return ExpressDeliveryRepository(self)

	@property
	def notification_repository(self):
		return NotificationRepository(self)

	@property
	def supplier_repository(self):
		return SupplierRepository(self)

	@property
	def product_classification_repository(self):
		return ProductClassificationRepository(self)

	@property
	def coupon_repository(self):
		return CouponRepository(self)

	@property
	def coupon_rule_repository(self):
		return CouponRuleRepository(self)

	@property
	def member_repository(self):

		return MemberRepository(self)

	@property
	def limit_zone_repository(self):
		return LimitZoneRepository(self)

	@property
	def product_label_repository(self):
		return ProductLabelRepository(self)

	@property
	def product_label_group_repository(self):
		return ProductLabelGroupRepositroy(self)

	@property
	def province_city_repository(self):
		return ProvinceCityRepository(self)

	@property
	def wepage_project(self):
		return WepageProjectRepository(self)

	@property
	def promotion_repository(self):
		return PromotionRepository(self)

	@property
	def order_config_repository(self):
		return OrderConfigRepository(self)

	@property
	def order_export_job_repository(self):
		return OrderExportJobRepository(self)

	@property
	def export_job_repository(self):
		return ExportJobRepository(self)

	@property
	def material_repository(self):
		return MaterialRepository(self)

	@property
	def weixin_news_repository(self):
		return WeixinNewsRepository(self)

	@property
	def template_message_detail_repository(self):
		return TemplateMessageDetailRepository(self)

	@property
	def mpuser_access_token_repository(self):
		return MpuserAccessTokenRepository(self)

	@property
	def social_account_repository(self):
		return SocialAccountRepository(self)

	@property
	def member_grade_repository(self):
		return MemberGradeRepository(self)