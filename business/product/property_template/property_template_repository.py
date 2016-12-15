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



from business.decorator import cached_context_property
from business.product.property_template.product_property_template import ProductPropertyTemplate


class PropertyTemplateRepository(business_model.Service):
	def get_templates(self):
		"""
		获得corp的所有template集合
		"""
		templates = []
		template_models = mall_models.ProductPropertyTemplate.select().dj_where(owner_id=self.corp.id)
		for template_model in template_models:
			templates.append(ProductPropertyTemplate.from_model({
				'model': template_model
			}))

		return templates

	def get_template(self, template_id):
		"""
		获得属于corp的，template_id指定的template对象
		"""
		template_model = mall_models.ProductPropertyTemplate.select().dj_where(owner_id=self.corp.id, id=template_id).get()

		template = ProductPropertyTemplate.from_model({
			'model': template_model
		})

		return template

	def delete_template(self, template_id):
		"""
		删除template_id指定的template
		"""
		mall_models.TemplateProperty.delete().dj_where(owner_id=self.corp.id, template_id=template_id).execute()
		mall_models.ProductPropertyTemplate.delete().dj_where(owner_id=self.corp.id, id=template_id).execute()
