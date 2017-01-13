# -*- coding: utf-8 -*-
import json
from bdem import msgutil

from eaglet.core import watchdog
from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource

from business import model as business_model
from db.account import models as account_model
from db.mall import models as mall_models

from business.mall.logistics.area_postage_config import AreaPostageConfig
from business.mall.logistics.free_postage_config import FreePostageConfig
from business.mall.logistics.shipper import Shipper
from gaia_conf import TOPIC

class ShipperRepository(business_model.Service):

	def get_shipper(self, shipper_id):
		"""
		获得指定的发货人
		"""
		shipper_model = mall_models.ShipperMessages.select().dj_where(owner_id=self.corp.id, id=shipper_id).get()

		shipper = Shipper(shipper_model)
		return shipper

	def delete_shipper(self, shipper_id):
		"""
		删除指定的发货人
		"""
		mall_models.ShipperMessages.delete().dj_where(owner_id=self.corp.id, id=shipper_id).execute()

	def get_shippers(self):
		"""
		获取corp中所有的发货人
		"""
		shipper_models = mall_models.ShipperMessages.select().dj_where(owner_id=self.corp.id,is_deleted=False).order_by(mall_models.ShipperMessages.created_at)
		datas = []
		for model in shipper_models:
			shipper = Shipper(model)
			datas.append(shipper)
		return datas