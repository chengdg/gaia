# -*- coding: utf-8 -*-
import json

from eaglet.decorator import cached_context_property

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
		'webapp_id',
		'username',

		'company_name',
		'settlement_type',
		'divide_rebate',
		'clear_period',
		'customer_from',
		'max_product_count',
		'classification_ids',

		'contact',
		'contact_phone',
		'valid_time_from',
		'valid_time_to',
		'note',

		'created_at',
		'status',

		'pre_sale_tel',
		'after_sale_tel',
		'service_tel',
		'service_qq_first',
		'service_qq_second'
	)

	def __init__(self, owner_id):
		business_model.Model.__init__(self)
		self.id = owner_id
		self.company_name = ''
		self.status = 0
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

	@cached_context_property
	def details(self):
		"""
		填充corp详情
		"""
		corp_model = account_model.CorpInfo.select().dj_where(id=self.id).first()
		if corp_model:
			self.name = corp_model.name
			self.company_name = corp_model.company_name
			self.settlement_type = corp_model.settlement_type
			self.divide_rebate = corp_model.divide_rebate
			self.clear_period = corp_model.clear_period
			self.customer_from = corp_model.customer_from
			self.max_product_count = corp_model.max_product_count
			self.classification_ids = corp_model.classification_ids
			self.contact = corp_model.contact
			self.contact_phone = corp_model.contact_phone
			self.note = corp_model.note
			self.created_at = corp_model.created_at
			self.status = int(corp_model.status)
			self.pre_sale_tel = corp_model.pre_sale_tel
			self.after_sale_tel = corp_model.after_sale_tel
			self.service_tel = corp_model.service_tel
			self.service_qq_first = corp_model.service_qq_first
			self.service_qq_second = corp_model.service_qq_second

		return self

	def __update(self, args, update_field_list):
		update_data = dict()
		for field_name in update_field_list:
			if ':' in field_name:
				transfer_type = field_name.split(':')[1]
				field_name = field_name.split(':')[0]
				field_value = args.get(field_name)

				if transfer_type == 'bool':
					field_value = field_value in ("True", "true", True)
				elif transfer_type == "float":
					field_value = float(field_value)
			else:
				field_value = args.get(field_name)

			if not field_value == None:
				update_data[field_name] = field_value

		account_model.CorpInfo.update(**update_data).dj_where(id=self.id).execute()

	def update(self, args):
		corp_model = account_model.CorpInfo.select().dj_where(id=self.id).first()
		if not corp_model:
			account_model.CorpInfo.create(
				id = self.id,
				status = True
			)
		self.update_base_info(args)
		if not self.is_weizoom_corp():
			self.update_mall_info(args)
			self.update_service_info(args)

	def update_service_info(self, args):
		update_field_list = ['pre_sale_tel', 'after_sale_tel', 'service_tel', 'service_qq_first', 'service_qq_second']
		self.__update(args, update_field_list)

	def update_mall_info(self, args):
		"""
		更新商户商城配置
		"""
		update_field_list = ['settlement_type', 'clear_period',
							 'divide_rebate:float', 'max_product_count', 'classification_ids']
		self.__update(args, update_field_list)

	def update_base_info(self, args):
		"""
		更新帐号信息
		"""
		update_field_list = ['name', 'company_name', 'note', 'contact', 'contact_phone']
		self.__update(args, update_field_list)

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