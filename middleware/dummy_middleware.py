# -*- coding: utf-8 -*-
import logging
#from eaglet.core.cache import utils as cache_utils

class DummyMiddleware(object):
	def process_request(self, request, response):
		logging.info('in dummy middleware')
		# TODO: place your codes here
		return
