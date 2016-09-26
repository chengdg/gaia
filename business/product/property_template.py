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

	def update(self, name, properties):
		"""
		更新模板
		"""
		pass