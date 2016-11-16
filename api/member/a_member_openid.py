# # -*- coding: utf-8 -*-
# import json
# from datetime import datetime
#
# from eaglet.core import api_resource, paginator
# from eaglet.decorator import param_required
#
# from business.member.social_account import SocialAccount
# from business.member.member import Member
#
# class AMemberOpenId(api_resource.ApiResource):
#     """
#     通过会员ID获取openid
#     """
#     app = "member"
#     resource = "member_openid"
#
#     @param_required(['member_id'])
#     def get(args):
#         member = Member.from_id({'id': args['member_id']})
#         if not member:
#             return {}
#         member_dict = member.to_dict()
#         social_account = SocialAccount.from_member_id({'member_id': args['member_id']})
#         if not social_account:
#             return {}
#         else:
#             member_dict.update({'openid': social_account.to_dict()['openid']})
#         member_dict.update({
#                 'username': member.username_for_html,
#                 'grade': member.grade.to_dict()
#             })
#         return {
#
#             'member': member_dict
#         }