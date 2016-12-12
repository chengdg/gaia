# -*- coding: utf-8 -*-
import logging
from copy import copy, deepcopy
from bdem import msgutil

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models
from eaglet.core import paginator

from business.product.product import Product
from business.mall.corporation_factory import CorporationFactory
from gaia_conf import TOPIC


class ProductClassificationQualification(business_model.Model):
	"""
	商品分组特殊资质
	"""
	__slots__ = (
		'id',
		'name',
		'created_at',
	)

	def __init__(self, model=None):
		business_model.Model.__init__(self)

		self.context['db_model'] = model
		if model:
			self._init_slot_from_model(model)
