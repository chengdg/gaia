#coding: utf8

import logging

_SERVICE_LIST = {
}

def register(msg_name):
	def wrapper(function):
		_SERVICE_LIST[msg_name] = function
		logging.info("registered service: {} => {}".format(msg_name, function))
		return function
	return wrapper


def find_service(msg_name):
	return _SERVICE_LIST.get(msg_name)