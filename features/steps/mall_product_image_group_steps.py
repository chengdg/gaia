# -*- coding: utf-8 -*-
import json

from behave import *
from features.util import bdd_util
from db.mall import models as mall_models
from db.account import models as account_models


@when(u"{user}添加图片分组")
def step_impl(context, user):
    image_groups = json.loads(context.text)
    if not type(image_groups) == list:
        image_groups = [image_groups]

    for image_group in image_groups:
        for image in image_group['images']:
            image['id'] = -1
            image['width'] = '640'
            image['height'] = '640'
        image_group['images'] = json.dumps(image_group['images'])
        image_group['corp_id'] = context.corp.id

        url = '/mall/image_group/'
        response = context.client.put(url, image_group)
        bdd_util.assert_api_call_success(response)


@then(u"{user}能获取图片分组列表")
def step_impl(context, user):
    url = '/mall/image_groups/?corp_id=%d' % context.corp.id
    response = context.client.get(url)
    actual = response.data['image_groups']
    for image_group in actual:
        for image in image_group['images']:
            image['path'] = image['url']

    expected = json.loads(context.text)
    bdd_util.assert_list(expected, actual)


@then(u"{user}能获取图片分组'{image_group_name}'")
def step_impl(context, user, image_group_name):
    db_image_group = mall_models.ImageGroup.select().dj_where(
        owner_id=context.corp.id,
        name=image_group_name
    ).get()

    url = '/mall/image_group/?corp_id=%d&image_group_id=%d' % (context.corp.id, db_image_group.id)
    response = context.client.get(url)
    images = response.data['image_group']['images']
    for image in images:
        image['path'] = image['url']
    actual = {
        "images": images
    }

    expected = json.loads(context.text)
    bdd_util.assert_dict(expected, actual)


@when(u"{user}更新图片分组'{image_group_name}'")
def step_impl(context, user, image_group_name):
    db_image_group = mall_models.ImageGroup.select().dj_where(
        owner_id=context.corp.id,
        name=image_group_name
    ).get()

    image_group = json.loads(context.text)
    for image in image_group['images']:
        image['id'] = -1
        image['width'] = '640'
        image['height'] = '640'
    image_group['images'] = json.dumps(image_group['images'])
    image_group['image_group_id'] = db_image_group.id
    image_group['corp_id'] = context.corp.id

    url = '/mall/image_group/'
    response = context.client.post(url, image_group)
    bdd_util.assert_api_call_success(response)


@when(u"{user}删除图片分组'{image_group_name}'")
def step_delete_image_group(context, user, image_group_name):
    db_image_group = mall_models.ImageGroup.select().dj_where(
        owner_id=context.corp.id,
        name=image_group_name
    ).get()

    data = {
        "corp_id": context.corp.id,
        "image_group_id": db_image_group.id
    }
    response = context.client.delete('/mall/image_group/', data)
    bdd_util.assert_api_call_success(response)
