# -*- coding: utf-8 -*-

# __author__ = 'charles'


import urllib2
from db.mall import models as webapp_models
from django.conf import settings
from celery import task
from eaglet.core.cache.utils import delete_cache
import settings

from business.account.user_profile import UserProfile


@task(name='clear synced product cache')
def clear_sync_product_cache(product_id=None):
	"""
	清理同步商品的缓存
	"""
	# weapp_owner_id = UserProfile.from_webapp_type()
	# user_profile = UserProfile.from_webapp_type({'webapp_type': 2})
	# if not user_profile:
	# 	return None
	# weapp_owner_id = user_profile[0].user_id
	pools = webapp_models.ProductPool.select().dj_where(product_id=product_id,
												status=webapp_models.PP_STATUS_ON)
	weapp_owner_ids = [pool.woid for pool in pools]
	for weapp_owner_id in weapp_owner_ids:

		key = settings.REDIS_CACHE_KEY + 'webapp_product_detail_{wo:%s}_{pid:%s}' % (weapp_owner_id, product_id)
		delete_cache(key)
		update_product_list_cache(webapp_owner_id=weapp_owner_id)
		purge_webapp_page_from_varnish_cache(weapp_owner_id, product_id)


def update_product_list_cache(webapp_owner_id):
	"""

	@param webapp_owner_id:
	@return:
	"""
	# 先清缓存,以防异步任务失败
	key = settings.REDIS_CACHE_KEY + 'webapp_products_categories_{wo:%s}' % webapp_owner_id
	api_key = 'api' + key
	delete_cache(key)
	delete_cache(api_key)


def request_url(url2method):
	if url2method:
		for key, value in url2method.items():
			print value, ">>>>>>>key_url:", key
			request = urllib2.Request(key)
			request.get_method = lambda: value
			x = urllib2.urlopen(request)


def purge_webapp_page_from_varnish_cache(woid, project_id=0):
	if settings.EN_VARNISH:
		url2method = {}
		if project_id == 0:
			# 首先清理首页varnish
			home_project = webapp_models.Project.objects.filter(owner=woid, is_active=True)[0]
			url = "http://{}/termite2/webapp_page/?workspace_id=home_page&webapp_owner_id={}&workspace_id={}&project_id=0".format(
				settings.DOMAIN, woid, home_project.workspace_id)
			url2method[url] = "BAN"

			url = "http://{}/termite2/webapp_page/?workspace_id={}&webapp_owner_id={}&project_id=0".format(
				settings.DOMAIN, home_project.workspace_id, woid)
			url2method[url] = "PURGE"

		else:
			project = webapp_models.Project.objects.get(id=project_id)
			if project.is_active:
				home_project = webapp_models.Project.objects.filter(owner=woid, is_active=True)[0]
				url = "http://{}/termite2/webapp_page/?workspace_id=home_page&webapp_owner_id={}&workspace_id={}&project_id=0".format(
					settings.DOMAIN, woid, home_project.workspace_id)
				url2method[url] = "PURGE"

			url = "http://{}/termite2/webapp_page/?workspace_id=home_page&project_id={}&webapp_owner_id={}".format(
				settings.DOMAIN, project.id, woid)
			url2method[url] = "PURGE"

			url = "http://{}/termite2/webapp_page/?workspace_id=home_page&pwebapp_owner_id={}&roject_id={}".format(
				settings.DOMAIN, woid, project.id)
			url2method[url] = "PURGE"

			url = "http://{}/termite2/webapp_page/?workspace_id={}&webapp_owner_id={}&project_id=0".format(
				settings.DOMAIN, project.workspace_id, woid)
			url2method[url] = "PURGE"

		request_url(url2method)

