# -*- coding: utf-8 -*-
from datetime import datetime
import json
from bdem import msgutil

import settings
from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource

from db.mall import models as mall_models
from db.mall import promotion_models
from db.account import models as account_models
from business.account.user_profile import UserProfile
from business import model as business_model
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
from settings import PANDA_IMAGE_DOMAIN
from services.product_service.task import clear_sync_product_cache


from business.decorator import cached_context_property
from business.product.product_template_property import ProductTemplateProperty


class ProductPropertyTemplate(business_model.Model):
	"""
	商品属性模板
	"""
	__slots__ = (
		'id',
		'name',
		'created_at'
	)

	@staticmethod
	@param_required(['model'])
	def from_model(args):
		model = args['model']
		property_template = ProductPropertyTemplate(model)

		return property_template

	def __init__(self, model=None):
		business_model.Model.__init__(self)

		if model:
			self._init_slot_from_model(model)

	def set_corp(self, corp):
		self.context['corp'] = corp

	@property
	def properties(self):
		"""
		获取template中的template_property对象集合
		"""
		models = mall_models.TemplateProperty.select().dj_where(template_id=self.id)

		template_properties = []
		for property_model in models:
			template_properties.append(ProductTemplateProperty.from_model({
				'model': property_model
			}))

		return template_properties

	def update(self, params):
		"""
		更新模板

		Args:
          title: 属性模板标题
          new_properties: 需要新建的property集合
          update_properties: 需要更新的property集合
          deleted_property_ids: 需要删除的property的id集合
		"""
		corp = self.context['corp']
		template_id = self.id

		#更新template name
		name = params['title']
		mall_models.ProductPropertyTemplate.update(name=name).dj_where(owner_id=corp.id, id=template_id).execute()

		#更新已存在的template property
		update_properties = params['update_properties']
		for template_property in update_properties:
			mall_models.TemplateProperty.update(name=template_property['name'], value=template_property['value']).dj_where(owner_id=corp.id, template_id=template_id, id=template_property['id']).execute()

		#创建新的template property
		new_properties = params['new_properties']
		for template_property in new_properties:
			mall_models.TemplateProperty.create(
				owner = corp.id,
				template = template_id,
				name = template_property['name'],
				value = template_property['value']
			)

		#删除需要删除的template property
		deleted_property_ids = params['deleted_property_ids']
		mall_models.TemplateProperty.delete().dj_where(owner_id=corp.id, template_id=template_id, id__in=deleted_property_ids).execute()

	@staticmethod
	def create(params):
		corp = params['corp']
		name = params['title']
		properties = params['new_properties']

		template = mall_models.ProductPropertyTemplate.create(
			owner = corp.id,
			name = name
		)

		for template_property in properties:
			mall_models.TemplateProperty.create(
				owner = corp.id,
				template = template,
				name = template_property['name'],
				value = template_property['value']
			)