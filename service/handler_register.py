#coding: utf8

import logging

MESSAGE2HANDLER = {
}

def register(msg_name):
	def wrapper(function):
		function.__name__ = '%s_handler' % msg_name
		MESSAGE2HANDLER[msg_name] = function
		logging.info("register message handler: {} => {}".format(msg_name, function))
		return function
	return wrapper


def find_message_handler(msg_name):
	return MESSAGE2HANDLER.get(msg_name)
