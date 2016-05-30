# -*- coding: utf-8 -*-

from db.account import models as account_models
from eaglet.core.cache import utils as cache_util

class ApiAuthMiddleware(object):
	def process_request(self, req, resp):
		user = account_models.User.select().dj_where(username='jobs').get()

		counter = cache_util.get('counter')
		if not counter:
			counter = 0
		else:
			counter = int(counter)
		print 'counter is: ', counter
		counter += 1
		cache_util.set('counter', counter)
		print 'in api auth middleware...'