# -*- coding: utf-8 -*-
import json

import datetime
from behave import *
from features.util import bdd_util
from db.mall import models as mall_models
from db.account import models as account_models
from db.station_message import models as message_models


@when(u"{user}新增站内消息")
def step_add_station_message(context, user):
	messages = json.loads(context.text)
	for message in messages:
		data = {
			'corp_id': context.corp.id,
			'title': message['title'],
			'content': message['content']
		}
		response = context.client.put('/message/message/', data)
		bdd_util.assert_api_call_success(response)


@then(u"{user}查看站内消息列表")
@when(u"{user}查看站内信息列表")
def step_get_messages(context, user):
	data = {
		'corp_id': context.corp.id
	}
	response = context.client.get('/message/messages/', data)
	messages = response.data['messages']
	actual = [{'title': msg['title'], 'creat_time': msg['created_at']} for msg in messages]
	expected = bdd_util.table2dict(context)
	# expected = []
	bdd_util.print_json(expected)
	now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
	expected = [{'title': msg['title'], 'creat_time': now_time} for msg in context.table]
	bdd_util.assert_list(expected, actual)


@then(u"{user}查看消息'{title}'")
@when(u"{user}查看'{title}'的详情")
def step_get_message(context, user, title):
	message = message_models.Message.select().dj_where(title=title).get()
	data = {
		'id': message.id
	}

	response = context.client.get('/message/message/', data)

	message = response.data['message']
	att = message['attachments']

	actual = {
		'title': message['title'],
		'content': message['content'],
		'accessory': att if len(att) > 0 else None
	}

	expected = json.loads(context.text)
	bdd_util.assert_dict(expected, actual)


@when(u"{user}编辑站内消息'{title}'")
def step_edit_message(context, user, title):
	message = message_models.Message.select().dj_where(title=title).get()

	new_message = json.loads(context.text)
	data = {
		'id': message.id,
		'title': new_message['title'],
		'content': new_message['content'],
		'attachments': json.dumps(new_message['accessory'])
	}
	response = context.client.post('/message/message/', data)
	bdd_util.assert_api_call_success(response)


@when(u"{user}删除站内消息'{title}'")
def step_delete_category(context, user, title):
	message = message_models.Message.select().dj_where(title=title).get()
	data = {
		'id': message.id
	}
	response = context.client.delete('/message/message/', data)
	bdd_util.assert_api_call_success(response)

