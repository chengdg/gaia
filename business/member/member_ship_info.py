# -*- coding: utf-8 -*-
import json
from bs4 import BeautifulSoup
import math
from datetime import datetime

from eaglet.decorator import param_required
from eaglet.core.cache import utils as cache_util
from db.member import models as member_models
from eaglet.core import watchdog
from business import model as business_model
import settings
from eaglet.decorator import cached_context_property
from business.common.encode_district_service import EncodeDistrictService


class MemberShipInfo(business_model.Model):
	"""
	会员的收货地址
	"""
	__slots__ = (
		'id',
		'receiver_name', # 收货人姓名
		'phone', # 收货人电话
		'address', # 收货人地址
		'area_code', #地区编码, 格式: 1_1_8
		'area', #地区, 格式："北京市 北京市 海淀区"
		'is_selected', # 是否选中
		'created_at'
	)

	def __init__(self, db_model):
		business_model.Model.__init__(self)
		self.context['db_model'] = db_model
		if db_model:
			self._init_slot_from_model(db_model)
			self.phone = db_model.ship_tel
			self.address = db_model.ship_address
			self.area_code = db_model.area
			self.area = EncodeDistrictService.get().decode(db_model.area)
			self.receiver_name = db_model.ship_name