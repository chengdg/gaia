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
from business.weixin.material import Material

from db.weixin import models as weixin_models


class MaterialRepository(business_model.Service):

	def get_materials(self, params, target_page):

		db_models = self.__get_material_models(params)

		pageinfo, db_models = paginator.paginate(db_models, target_page.cur_page, target_page.count_per_page)

		materials_models = []
		for model in db_models:
			materials_models.append(Material(model))

		return pageinfo, materials_models

	def __get_material_models(self, params):

		selected_material_id = params.get('selected_material_id', 0)
		title = params.get('query', None)

		if title and len(title) > 0:
			# 需求说只显示单图文即可
			materials_models = weixin_models.Material.select(weixin_models.Material.id).dj_where(owner=self.corp.id, is_deleted=False, type=weixin_models.SINGLE_NEWS_TYPE).order_by(params.get('sort_attr', '-id'))
			material_ids = [ material.id for material in materials_models]
			target_material_ids = [news.material_id for news in weixin_models.News.select().dj_where(material_id__in=material_ids, title__icontains=title)]
			materials = weixin_models.Material.select().dj_where(owner=self.corp.id, is_deleted=False, id__in=target_material_ids)
		else:
			# 需求说只显示单图文即可
			materials = weixin_models.Material.select().dj_where(owner=self.corp.id, is_deleted=False, type=weixin_models.SINGLE_NEWS_TYPE)

		if params.get('from', '') == 'share_page_config':
			materials = materials.filter(type=weixin_models.SINGLE_NEWS_TYPE)

		return materials

