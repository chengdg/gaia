# -*- coding: utf-8 -*-
import json

from eaglet.core import watchdog
from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource

CORPORATION = None

class CorporationFactory(object):
	@staticmethod
	def set(corporation):
		global CORPORATION
		CORPORATION = corporation

	@staticmethod
	def get():
		global CORPORATION
		return CORPORATION
