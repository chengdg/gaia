# # -*- coding: utf-8 -*-
#
# import json
#
# from eaglet.core import api_resource, paginator
# from eaglet.decorator import param_required
# from eaglet.core import watchdog
# from eaglet.core.exceptionutil import unicode_full_stack
#
# from business.member.member import Member
#
#
# class AMemberList(api_resource.ApiResource):
#     """
#     会员列表
#     """
#     app = 'member'
#     resource = 'member_list'
#
#     @param_required(['webapp_id', 'page', 'count_per_page'])
#     def get(args):
#         webapp_id = int(args['webapp_id'])
#         members = Member.from_webapp_id({'webapp_id': webapp_id})
#
#         # 分页
#         cur_page = int(args['page'])
#         count_per_page = int(args['count_per_page'])
#         pageinfo, members = paginator.paginate(members, cur_page, count_per_page)
#
#         items = []
#         for member in members:
#             items.append(member.to_dict('username', 'username_for_html', 'user_icon', 'grade_name', 'tags'))
#
#         return {
#             'items': items,
#             'pageinfo': pageinfo.to_dict()
#         }