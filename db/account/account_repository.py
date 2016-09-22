# -*- coding: utf-8 -*-

import models

####  只有一个地方与数据库交互

class User(object):
	'''
	直接与DB层交互，领域中其它都是从这里入口
	'''
	def __init__(self, owner_id):
		self.model = models.User.select().dj_where(id=owner_id)

	def get_profile(self):
		return models.UserProfile.get(user=self.model)


