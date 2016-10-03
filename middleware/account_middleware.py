# -*- coding: utf-8 -*-

import settings
from eaglet.core import watchdog

from business.mall.corporation import Corporation
from business.mall.corporation_factory import CorporationFactory

class AccountMiddleware(object):
	def process_request(sel, req, resp):
		if '/user/access_token' in req.path or '/console/' in req.path:
			watchdog.info("skipped in WebAppAccountMiddleware. req.path: {}".format(req.path))
			return

		if settings.DEBUG:
			print '=====> req.params <====='
			print req.params
		corp_id = req.params.get('woid')
		if not corp_id:
			corp_id = req.params.get('corp_id')
		req.context['corp'] = Corporation(corp_id)
		CorporationFactory.set(req.context['corp'])
