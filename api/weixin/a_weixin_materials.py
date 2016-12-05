# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required

from business.common.page_info import PageInfo


class AWeixinMaterials(api_resource.ApiResource):
	"""
	图文资源
	"""
	app = 'weixin'
	resource = 'materials'

	@param_required(['corp'])
	def get(args):
		corp = args['corp']
		material_repository = corp.material_repository
		news_repository = corp.weixin_news_repository
		
		target_page = PageInfo.create({
			"cur_page": int(args.get('cur_page', 1)),
			"count_per_page": int(args.get('count_per_page', 4))
		})
		selected_material_id = int(args.get('selected_material_id', 0))
		data = {
			'selected_material_id': selected_material_id,
			'query': args.get('query', None),
			'share_from': args.get('from', ''),
			'sort_attr': args.get('sort_attr', '-id')
		}
		# 获取素材
		pageinfo, materials = material_repository.get_materials(data, target_page)

		material_ids = []
		id2material = {}
		for material in materials:
			material_ids.append(material.id)
			material.newses = []
			id2material[material.id] = material

		# 获取图文消息
		news = news_repository.get_news_by_material_ids(material_ids) #		

		for new in news:
			id2material[new.material_id].newses.append({
				"id": new.id,
				"title": new.title
			})

		datas = []
		for material in materials:
			datas.append({
				"id": material.id,
				"created_at": material.created_at.strftime("%Y-%m-%d %H:%M:%S"),
				"type": 'single' if material.type == u'单图文消息' else 'multi',
				"newses": material.newses,
				"isChecked": True if material.id == selected_material_id else False
			})

		return {
			'page_info': pageinfo.to_dict(),
			'materials': datas
		}
