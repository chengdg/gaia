# -*- coding: utf-8 -*-
__author__ = 'charles'


from eaglet.core import api_resource
from eaglet.decorator import param_required
# from eaglet.core import watchdog
# from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.logistics.postage_config_factory import PostageConfigFactory
from business.member.member_grade import MemberGrade

class ADefaultConfigs(api_resource.ApiResource):
    """
    商户的默认商城配置
    """

    app = 'mall'
    resource = 'default_configs'

    @param_required(['corp_id'])
    def put(args):
        PostageConfigFactory.get(args['corp']).make_sure_default_postage_config_exists()

        corp = args['corp']
        MemberGrade.create_default_member_grade_for_corp(corp)

        integral_strategy = corp.mall_config_repository.get_integral_strategy()
        return {}
