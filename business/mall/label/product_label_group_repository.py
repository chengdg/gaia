# -*- coding: utf-8 -*-
from business import model as business_model
from business.mall.corporation_factory import CorporationFactory
from db.mall import models as mall_models
from business.mall.label.product_label_group import ProductLabelGroup


class ProductLabelGroupRepositroy(business_model.Service):
	def get_label_groups(self):
		models = mall_models.ProductLabelGroup.select().dj_where(owner_id=self.corp.id, is_deleted=False)
		product_label_groups = [ProductLabelGroup(model) for model in models]
		return product_label_groups

	def delete_label_group(self, label_group_id):
		#查询出需要删除的分类中的标签
		deleted_labels = mall_models.ProductLabel.select().dj_where(label_group_id=label_group_id)
		deleted_label_ids = [str(l.id) for l in deleted_labels]
		#首先删除所有的标签
		weizoom_corp = CorporationFactory.get_weizoom_corporation()
		weizoom_corp.product_label_repository.delete_labels(deleted_label_ids)
		#然后删除分组
		print label_group_id
		mall_models.ProductLabelGroup.update(is_deleted=True).dj_where(id=label_group_id).execute()