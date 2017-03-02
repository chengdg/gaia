# -*- coding: utf-8 -*-

from util.command import BaseCommand
from db.mall import models as mall_models

class Command(BaseCommand):
	help = "insure the product_count field of mall_classification"
	args = ''
	
	def handle(self, **options):
		all_classifications = mall_models.Classification.select()
		all_classification_ids = [c.id for c in all_classifications]

		print 'reset product_count to 0'
		mall_models.Classification.update(product_count=0).execute()

		# classification_id2info = {c.id: c for c in all_classifications}

		relations = mall_models.ClassificationHasProduct.select().dj_where(classification_id__in=all_classification_ids)

		deleted_product_ids = [p.id for p in mall_models.Product.select().dj_where(is_deleted=True)]

		classification_has_products = dict()
		print 'collect relations'
		for relation in relations:
			classification_id = relation.classification_id
			product_id = relation.product_id
			if product_id in deleted_product_ids:
				print 'product({}) been deleted'.format(product_id)
				continue
			if not classification_has_products.has_key(classification_id):
				classification_has_products[classification_id] = [product_id]
			else:
				classification_has_products[classification_id].append(product_id)

		print 'sync datas'
		for db_model in all_classifications:
			products = classification_has_products.get(db_model.id)
			if not products == None:
				product_count = len(products)
				mall_models.Classification.update(product_count=product_count).dj_where(id=db_model.id).execute()
				print u'update classification({}.product_count) === >{}'.format(db_model.name, product_count)
				# father_id = db_model.father_id
				# while father_id > 0:
				# 	father_model = mall_models.Classification.select().dj_where(id=father_id).first()
				# 	product_count = father_model.product_count + product_count
				# 	father_model.product_count = product_count
				# 	father_model.save()
				# 	print u'update father classification({}.product_count) === >{}'.format(father_model.name, product_count)
				# 	father_id = classification_id2info[father_id].father_id