# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.account.user_profile import UserProfile


class AZypcInfo(api_resource.ApiResource):
    """
    获取自营平台相关的信息
    """
    app = 'account'
    resource = 'zypt_info'

    @param_required(['mall_type'])
    def get(args):
        mall_type = args['mall_type']
        if mall_type == '1':
            zypc_info = []
            user_profiles = UserProfile.from_mall_type({'mall_type': mall_type})
            for profile in user_profiles:
                zypc_info.append({
                        'user_id': profile.user_id,
                        'webapp_id': profile.webapp_id,
                        'store_name': profile.store_name
                    })

        return zypc_info