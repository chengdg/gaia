# -*- coding: utf-8 -*-
__author__ = 'charles'


from eaglet.core import api_resource
from eaglet.decorator import param_required
# from eaglet.core import watchdog
# from eaglet.core.exceptionutil import unicode_full_stack

from business.account.user_profile import UserProfile


class AUserProfileList(api_resource.ApiResource):
    """
    商户列表
    """

    app = 'mall'
    resource = 'user_list'

    @param_required(['page', 'page_count'])
    def get(self):
        """
        获取商户列表
        page -- 页码
        page_count -- 每页显示多少记录
        """
        page = self.get('page', 1)
        page_count = self.get('page_count', 15)
        if page == '0':
            page = 1
        if page_count == '0':
            page_count = 15
        data = UserProfile.from_page({'page': page,
                                      'page_count': page_count})
        result = []
        for user in data.get('users'):
            temp = {'user_id': user.user_id,
                    'webapp_id': user.webapp_id,
                    'store_name': user.store_name,
                    'user_name': user.username}
            result.append(temp)
        return {
            'users': result,
            'counts': data.get('counts')
        }
