# -*- coding: utf-8 -*-
import json

from eaglet.core import watchdog
from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource

from business import model as business_model
from db.account import models as account_model
from db.mall import models as mall_models


class PostageConfig(business_model.Model):
    """
    订单
    """

    __slots__ = (
        'id',
        'special_configs',
        'free_configs',
        'owner_id',
        'config'
    )
# -*- coding: utf-8 -*-
import json

from eaglet.core import watchdog
from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource

from business import model as business_model
from db.account import models as account_model
from db.mall import models as mall_models


class PayInterface(business_model.Model):
    """
    订单
    """

    __slots__ = (
        'id',
        'special_configs',
        'free_configs',
        'owner_id',
        'config'
    )

    def __init__(self, owner_id, id, special_configs, free_configs, config):
        business_model.Model.__init__(self)

        self.id = id,
        self.owner_id = owner_id,
        self.special_configs = special_configs
        self.free_configs = free_configs
        self.config = config
