# -*- coding: utf-8 -*-
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack


def not_retry(func):
	"""
	即使handler处理消息失败，也标记消息为已处理
	@param func:
	@return:
	"""
	def wrapper(*args, **kw):
		try:
			return func(*args, **kw)
		except:
			watchdog.alert({
				'uuid': 'order_trade_error',
				'traceback': unicode_full_stack()
			})

	return wrapper