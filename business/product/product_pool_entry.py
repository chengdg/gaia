# coding=utf-8
# -*- utf-8 -*-

import copy

from eaglet.decorator import param_required
from eaglet.core import paginator

from bdem import msgutil
from business import model as business_model
from business.product.product import Product
from db.mall import models as mall_models
from gaia_conf import TOPIC
from fill_product_detail_service import FillProductDetailService
from business.mall.corporation_factory import CorporationFactory
from business.common.filter_parser import FilterParser

NEW_PRODUCT_DISPLAY_INDEX = 9999999


class ProductPoolEntry(business_model.Model):
	__slots__ = (
		'id',
		'display_index',
		'sync_at',
		'product_id',
	)

	def __init__(self, model=None):
		business_model.Model.__init__(self)
		
		if model:
			self._init_slot_from_model(model)

	