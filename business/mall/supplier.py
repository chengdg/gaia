# -*- coding: utf-8 -*-
from eaglet.decorator import param_required

from db.mall import models as mall_models
from business import model as business_model

class Supplier(business_model.Model):
    __slots__ = (
        'id',
        'name',
        'responsible_person',
        'supplier_tel',
        'supplier_address',
        'remark',
        'is_delete',
        'created_at'
    )

    def __init__(self, model):
        business_model.Model.__init__(self)

        self.context['db_model'] = model
        if model:
            self._init_slot_from_model(model)

    @staticmethod
    @param_required(['db_model'])
    def from_model(args):
        model = args['db_model']
        product = Product(model)
        return product

    @staticmethod
    @param_required(['id'])
    def from_id(args):
        supplier_db_model = mall_models.Supplier.get(id=args['id'])
        return Supplier(supplier_db_model)

    @staticmethod
    @param_required(['ids'])
    def from_id(args):
        supplier_db_models = mall_models.Supplier.select.dj_where(id__in=args['ids'])
        suppliers = []
        for model in supplier_db_models:
            suppliers.append(Supplier(model))
        return suppliers

    @staticmethod
    @param_required(['ids'])
    def get_id_2_supplier_name(args):
        supplier_db_models = mall_models.Supplier.select().dj_where(id__in=args['ids'])
        id2supplier_name = {}
        for model in supplier_db_models:
            id2supplier_name[model.id] = model.name
        return id2supplier_name