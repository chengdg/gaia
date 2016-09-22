# -*- coding: utf-8 -*-

import settings
from eaglet.core import watchdog

from core.redirects import HTTPMiddlewareError
from business.mall.corporation import Corporation

class AccountMiddleware(object):
	def process_request(sel, req, resp):
		if '/user/access_token' in req.path or '/console/' in req.path:
			watchdog.info("skipped in WebAppAccountMiddleware. req.path: {}".format(req.path))
			return

		woid = req.params.get('woid')
		req.context['corp'] = Corporation(woid)
