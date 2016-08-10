# -*- coding: utf-8 -*-
import json
from datetime import datetime

from eaglet.core import api_resource, paginator
from eaglet.decorator import param_required

from business.mall.order_product_relation import OrderProductRelation
from business.mall.order import Order
from business.mall.order_items import OrderItems
from business.account.user_profile import UserProfile
from business.mall.order_has_group import OrderHasGroup

class AOrderList(api_resource.ApiResource):
    """
    订单列表
    """
    app = 'order'
    resource = 'order_list'

    @param_required(['owner_id', 'cur_page', 'count_per_page'])
    def get(args):
        """
        订单列表
        """
        no_required = [ # 表内查询
            'order_id',  # 订单号精确查找   解决
            'ship_name',  # 发货地址  表中存在 解决
            'ship_tel',   # 收货人姓名   表中存在 解决
            
            'express_number', # 快递号   表中存在 解决
            'source',  # 订单来源：1:商城；0本店  表中存在--> order_source   解决
            'status',  # 订单状态    表中存在   解决
            'is_first_order',  # 是否首单   解决
            'pay_type',  # 支付方式：参考weapp.mall.models.PAYTYPE2NAME    表中存在   ----> pay_interface_type 解决
            'type',  #订单类型  解决

            'product_name',  # 商品名称    解决
            'is_used_weizoom_card', # 是否使用微众卡
            
            #########1,2##################
            'date_interval',  # 查询时间：2014-10-07|2014-10-08，注：使用‘|’区分，该参数和date_interval_type结合使用
            'date_interval_type',  #时间类型：1 下单时间 2 付款时间 3 发货时间 4 退款时间 5 退款完成时间 6 订单完成时间 7 订单取消时间

            'supplier_type'  #订单供货商类型
            ]
        special_filter = [  #,表外查询

        ]
        # print 'kjdjsj-----230230========================order_list', args
        filter_param = {}
        special_filter_param = {}
        filter_datetime_param = {}
        other_params = {}
        order_list = []
        for key in args:
            if key in no_required:
                if key == 'source':
                    filter_param['order_source'] = args[key]
                elif key == 'pay_type':
                    filter_param['pay_interface_type'] = args[key]
                elif key == 'date_interval_type':
                    pass
                elif key == 'is_used_weizoom_card':
                    special_filter_param[key] = True if args[key] == '1' else False
                elif key == 'date_interval':
                    date_interval = args['date_interval'].split('|')
                    format_datetime = '%Y-%m-%d %H:%M:%S'

                    filter_datetime_param['date_interval_type'] = args['date_interval_type']
                    if ':' in date_interval[0]:
                        filter_datetime_param['_begin'] = datetime.strptime('{0}'.format(date_interval[0]), format_datetime)
                        filter_datetime_param['_end'] = datetime.strptime('{0}'.format(date_interval[1]), format_datetime)
                    else:
                        filter_datetime_param['_begin'] = datetime.strptime('{0} 00:00:00'.format(date_interval[0]), format_datetime)
                        filter_datetime_param['_end'] = datetime.strptime('{0} 23:59:59'.format(date_interval[1]), format_datetime)                       
                     
                elif key == 'is_first_order':
                    filter_param['is_first_order'] = True if args[key] == '1' else False
                elif key == 'product_name':
                    special_filter_param[key] = args[key]
                elif key == 'sort_attr':
                    other_params[key] = args[key]
                else:
                    filter_param[key] = args[key]
        # print filter_param
        # print special_filter_param
        # print filter_datetime_param
        order_list, order_select_query = Order.from_owner_id({'owner_id': args['owner_id']})
        # print order_list, order_select_query

        # import pdb
        # pdb.set_trace()
        if not order_list and  not order_select_query:
            msg = u'owner_id={0} 没有订单'.format(args['owner_id'])
            order_list = []
        if filter_param or special_filter_param or filter_datetime_param:   # 筛选
            # filter_param['owner_id'] = args['owner_id']
            # TODO 过滤各种可能性
            order_list = AOrderList.filter_order(filter_param, order_select_query, special_filter_param, filter_datetime_param, other_params)

        #分页
        cur_page = int(args.get('cur_page', 1))
        count_per_page = int(args.get('count_per_page', 10))
        pageinfo, order_list = paginator.paginate(order_list, cur_page, count_per_page, query_string=args.get('query_string', ''))
        orders = []
        for order in order_list:
            order_obj = order.to_dict()
            # import pdb
            # pdb.set_trace()
            groups = AOrderList.get_order_groups(order)
            rets = {
                'total_price': order.context['db_model'].get_total_price(),
                'come': order.context['db_model'].order_source,
                'pay_interface_name': order.context['db_model'].get_pay_interface_name,
                'order_status': order.get_status_text,
                'express_number': order.context['db_model'].express_number,
                'remark': order.context['db_model'].remark,
                'pay_time': order.context['db_model'].payment_time,
                'is_group_buying': order.is_group_buy,
                'cancel': order.order_cancel , # 取消订单时间
                'refound_time':  order.order_refound_time, #退款时间
                'refound_finish_time': order.order_refound_finish_time, #退款完成时间
                'finish_time':  '', #订单完成时间
                'save_money': float('%.2f' % order.get_save_money),# 优惠金额
                'pay_money': float('%.2f' % order.get_pay_money), # 订单总额order.final_price + order.weizoom_card_money
                'parent_action': '', # 主订单可操作行为
                'groups':  groups, #group
                'member_is_subscribed': '', # 会员是否关注
            }
            order_obj.update(rets)
            orders.append(order_obj)
        return {
            'orders': orders,
            'pageinfo': pageinfo.to_dict(),
        }

    @staticmethod
    def filter_order(filter_params, order_select_query, special_filter_param, filter_datetime_param, other_params={}):
        order_list = []
        # orders = order_select_query.filter(**filter_params)
        opt = {
            'db_filter_params': filter_params,    # 表内字段查询
            'orders_select_query': order_select_query,   #  查询结果集
            'special_filter_param': special_filter_param,   # 表外字段查询
            'filter_datetime_param': filter_datetime_param, # 时间查询
            'other_params': other_params
        }
        orders  = Order.from_filter_params(opt)
        if isinstance(orders, list):
            order_list += orders
        else:    
            order_list.append(orders)
        return [order  for order in order_list if order]

    @staticmethod
    def get_order_groups(order):
        # TODO 实现折单   在完完善
        groups = []
        group_order_relations = OrderHasGroup.from_webapp_id({'webapp_id': order.context['db_model'].webapp_id})
        if group_order_relations:
            group_order_ids = [r.order_id for r in group_order_relations]
        else:
            group_order_ids = []
       # 微众系列子订单
        if order.is_has_fackorder: #有子订单
            pass
        else:
            # import pdb
            # pdb.set_trace()

            group_order = {
                'id': order.id,
                'status': order.get_status_text,
                'order_status': order.status,
                'express_company_name': order.express_company_name,
                'express_number': order.express_number,
                'leader_name': order.leader_name,
                'type': order.type,
                 'actions': order.get_order_actions, 
            } 
            if order.supplier:
                pass
            else:
                group = {
                    'id': order.supplier,
                    'fackorder': group_order,
                    "products": order.products
                }
            groups.append(group)
        return groups

