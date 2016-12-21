# -*- coding:utf-8 -*-

import types
import json

from behave import *
from features.util import bdd_util


@then(u"{user}获得订单列表")
def step_impl(context, user):
	url = '/order/orders/?corp_id=%d' % context.corp.id
	response = context.client.get(url)
	bdd_util.assert_api_call_success(response)
	actual = response.data["orders"]
	expected = json.loads(context.text)
	bdd_util.assert_list(expected, actual)
