# -*- coding: utf-8 -*-

from eaglet.decorator import param_required
from eaglet.core import api_resource
from business import model as business_model
from db.mall import models as mall_models
from util import regional_util


class OrderFactory(business_model.Model):
    """
    Order工厂类
    """
    