# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.pay_interface import PayInterface
from business.mall.weixin_pay_interface_config import WeixinPayConfig
from business.weixin.component_authed_appid_info import ComponentAuthedAppidInfo


class APayInterfaceConfig(api_resource.ApiResource):
    app = 'mall'
    resource = 'weixin_pay_interface_config'

    @param_required(['pay_interface_id', 'owner_id'])
    def get(args):
        pay_interface_id = args['pay_interface_id']
        owner_id = args['owner_id']
        pay_interface = PayInterface.from_id({'id': pay_interface_id})
        pay_interface_configs = pay_interface.configs
        if not pay_interface.should_create_related_config:
            app_id = ComponentAuthedAppidInfo.get_auth_appid_by_owner_id({'owner_id': owner_id})
        else:
            app_id = pay_interface_configs.auth_appid
        return {
            'pay_interface_type': pay_interface.type,
            'pay_interface_name': pay_interface.name,
            'pay_interface_config': pay_interface_configs,
            'auth_appid': app_id
        }


    @param_required(['owner_id', 'pay_version', 'app_id', 'partner_id', 'partner_key', 'pay_interface_id'])
    def put(args):
        pay_interface_id = args['pay_interface_id']
        owner_id = args['owner_id']
        pay_version = args['pay_version']
        if pay_version == '0':
            try:
                paysign_key = args['paysign_key']
            except KeyError:
                msg = unicode_full_stack()
                watchdog.error(msg)
                return 500, {'msg': 'Not has paysign key'}
        elif pay_version == '1':
            paysign_key = ''
        else:
            return 500, {'msg': 'pay version error'}
        app_id = args['app_id']
        partner_id = args['partner_id']
        partner_key = args['partner_key']

        pay_interface = PayInterface.from_id({'id': pay_interface_id})
        try:
            config = WeixinPayConfig.create({
                'owner': owner_id,
                'pay_version': pay_version,
                'app_id': app_id,
                'partner_id': partner_id,
                'partner_key': partner_key,
                'paysign_key': paysign_key,
                'app_secret': ''
            })
            pay_interface.update_related_config_id(config_id=config.id)
            return {'msg': "create success"}
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return 500, {'msg': 'create weixin pay interface config failed'}



    @param_required(['pay_interface_id','owner_id', 'pay_version', 'app_id', 'partner_id', 'partner_key'])
    def post(args):
        pay_interface_id = args['pay_interface_id']
        owner_id = args['owner_id']
        pay_version = args['pay_version']
        if pay_version == '0':
            try:
                paysign_key = args['paysign_key']
            except KeyError:
                msg = unicode_full_stack()
                watchdog.error(msg)
                return 500, {'msg': 'Not has paysign key'}
        elif pay_version == '1':
            paysign_key = ''
        else:
            return 500, {'msg': 'pay version error'}
        app_id = args['app_id']
        partner_id = args['partner_id']
        partner_key = args['partner_key']

        pay_interface = PayInterface.from_id({'id': pay_interface_id})
        weixin_pay_config = WeixinPayConfig.from_id({'id': pay_interface.related_config_id})
        try:
            weixin_pay_config.update(
                pay_version=pay_version,
                app_id=app_id,
                partner_id=partner_id,
                partner_key=partner_key,
                paysign_key=paysign_key
            )
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return 500, {'msg': 'update weixin pay interface config failed'}
