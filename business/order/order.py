# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from eaglet.core import watchdog
from eaglet.decorator import param_required

from business import model as business_model
from db.mall import models as mall_models


class Order(business_model.Model):
	"""
	支付信息
	"""

	__slots__ = (
		'id',
		'owner_id',
		'type',
		'description',
		'is_active',
		'related_config_id',
		'name',
		'should_create_related_config'
	)

	def __init__(self, db_model=None):
		business_model.Model.__init__(self)