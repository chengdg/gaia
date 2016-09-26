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

from core import paginator
from business.decorator import cached_context_property


class PropertyTemplate(business_model.Model):
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
		property_template = PropertyTemplate(model)

		return property_template

	def __init__(self, model=None):
		business_model.Model.__init__(self)

		if model:
			self._init_slot_from_model(model)

	def set_corp(self, corp):
		self.context['corp'] = corp

	def update(params):
		"""
		更新模板
		"""
		corp = self.context['corp']
		name = params['title']
		properties = params['new_properties']
		template_id = params['template_id']

		mall_models.ProductPropertyTemplate.update(name=name).dj_where(owner_id=corp.id, id=template_id).execute()

		mall_models.TemplateProperty.delete().dj_where(owner_id=corp.id, template_id=template_id).execute()
		for template_property in properties:
			mall_models.TemplateProperty.create(
				owner = corp.id,
				template = template_id,
				name = template_property['name'],
				value = template_property['value']
			)

	def delete(self):
		mall_models.ProductPropertyTemplate.delete().dj_where(owner_id=self.corp.id, id=template_id)

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