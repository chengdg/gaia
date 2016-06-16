# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from business.account.user_profile import UserProfile

class AStoreName(api_resource.ApiResource):
    """
    供货商名称
    """
    app = "mall"
    resource = "store_name"

    @param_required(['webapp_ids'])
    def get(args):
        webapp_ids = args['webapp_ids'].split("_")
        webapp_id2store_name = []
        if webapp_ids:
            webapp_id2store_name = UserProfile.get_webapp_id_2_store_name({'webapp_ids': webapp_ids})
        return {'webapp_id2store_name': webapp_id2store_name}