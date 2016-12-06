# -*- coding: utf-8 -*-
"""
素材
"""
from eaglet.core import paginator
from eaglet.core import watchdog

from business.common.page_info import PageInfo
from eaglet.decorator import cached_context_property
from eaglet.decorator import param_required

from business import model as business_model
from business.weixin.weixin_news import WeixinNews

from db.weixin import models as weixin_models


class WeixinNewsRepository(business_model.Service):

	def get_news_by_material_ids(self, ids):
		db_models = weixin_models.News.select().dj_where(material_id__in=ids)
		news_models = []
		for model in db_models:
			news_models.append(WeixinNews(model))

		return news_models

