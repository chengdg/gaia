# -*- coding: utf-8 -*-

from business import model as business_model
from business.coupon.coupon_repository import CouponRepository
from business.coupon.coupon_rule_repository import CouponRuleRepository
from business.deprecated.wepage_project_repository import WepageProjectRepository
from business.member.member_grade_repository import MemberGradeRepository
from business.member.member_repository import MemberRepository
from business.order.delivery_item_repository import DeliveryItemRepository
from business.order.order_export_job_repository import OrderExportJobRepository
from business.order.order_repository import OrderRepository
from business.order.config.order_config_repository import OrderConfigRepository
from db.account import models as account_model


from business.product.product_shelf import ProductShelf
from business.product.product_pool import ProductPool
from business.product.property_template.property_template_repository import PropertyTemplateRepository
from business.product.model.product_model_property_repository import ProductModelPropertyRepository

from business.mall.product_pending_stock.pending_product_repository import PendingProductRepository
from business.mall.category.category_repository import CategoryRepository
from business.mall.image_group.image_group_repository import ImageGroupRepository
from business.mall.pay.pay_interface_repository import PayInterfaceRepository
from business.mall.logistics.postage_config_repository import PostageConfigRepository
from business.mall.logistics.express_delivery_repository import ExpressDeliveryRepository
from business.mall.logistics.limit_zone_repository import LimitZoneRepository
from business.mall.logistics.province_city_repository import ProvinceCityRepository
from business.mall.config.mall_config_repository import MallConfigRepository
from business.mall.notify.notification_repository import NotificationRepository
from business.mall.supplier.supplier_repository import SupplierRepository

from business.mall.classification.product_classification_repository import ProductClassificationRepository
from business.mall.label.product_label_repository import ProductLabelRepository
from business.mall.label.product_label_group_repository import ProductLabelGroupRepositroy

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
		'webapp_id',
		'username'
	)

	def __init__(self, owner_id):
		self.id = owner_id
		self.name = 'unknown'
		if owner_id:
			_account_user_profile = account_model.UserProfile.select().dj_where(user_id=owner_id).first()
			self.webapp_id = _account_user_profile.webapp_id

			if _account_user_profile.webapp_type == account_model.WEBAPP_TYPE_MALL:
				self.type = 'normal'
			elif _account_user_profile.webapp_type == account_model.WEBAPP_TYPE_WEIZOOM_MALL:
				self.type = 'self_run'
			elif _account_user_profile.webapp_type == account_model.WEBAPP_TYPE_WEIZOOM:
				self.type = 'weizoom_corp'
			elif _account_user_profile.webapp_type == account_model.WEBAPP_TYPE_MULTI_SHOP:
				self.type = 'multi_shop'
			else:
				self.type = 'unknown'

			_user = account_model.User.select().dj_where(id=owner_id).first()
			self.username = _user.username
		else:
			self.webapp_id = 0
			self.type = 'normal'

	def is_self_run_platform(self):
		"""
		判断是否是自营平台
		"""
		return self.type == 'self_run'

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
	def category_repository(self):
		return CategoryRepository.get(self)

	@property
	def image_group_repository(self):
		return ImageGroupRepository.get(self)

	@property
	def product_property_template_repository(self):
		return PropertyTemplateRepository.get(self)

	@property
	def pending_product_repository(self):
		return PendingProductRepository(self)

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