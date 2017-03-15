# -*- coding: utf-8 -*-
import json

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required

from business.common.page_info import PageInfo
from business.member.member import Member

class AMemberIntegralLogs(api_resource.ApiResource):
    """
    会员积分日志集合
    """
    app = "member"
    resource = "integral_logs"

    @param_required(['corp_id', 'member_id'])
    def get(args):
        corp = args['corp']

        target_page = PageInfo.create({
            "cur_page": int(args.get('cur_page', 1)),
            "count_per_page": int(args.get('count_per_page', 10))
        })

        datas = []
        member = corp.member_repository.get_member_by_id(args['member_id'])
        integral_logs, pageinfo =  member.get_integral_logs(target_page)
        for integral_log in integral_logs:
            datas.append({
                'id': integral_log.id,
                'event': integral_log.event,
                'reason': integral_log.reason,
                'actor': integral_log.actor,
                'integral_increment': integral_log.integral_increment,
                'current_integral': integral_log.current_integral,
                'created_at': integral_log.created_at.strftime('%Y-%m-%d %H:%M')
            })

        return {
            'pageinfo': pageinfo.to_dict(),
            'integral_logs': datas
        }
