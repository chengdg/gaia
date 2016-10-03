# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.core import watchdog
from eaglet.decorator import param_required
from eaglet.core.exceptionutil import unicode_full_stack

from business.mall.pay.pay_interface import PayInterface
from business.mall.pay.ali_pay_config import AliPayConfig


class AAliPayInterfaceConfig(api_resource.ApiResource):
    app = 'mall'
    resource = 'ali_pay_interface_config'

    @param_required(['pay_interface_id', 'owner_id'])
    def get(args):
        pay_interface_id = args['pay_interface_id']
        pay_interface = PayInterface.from_id({'id': pay_interface_id})
        pay_interface_configs = pay_interface.configs

        return {
            'pay_interface_type': pay_interface.type,
            'pay_interface_name': pay_interface.name,
            'pay_interface_config': pay_interface_configs
        }


    @param_required(['owner_id', 'pay_version', 'partner', 'key', 'private_key', 'ali_public_key', 'seller_email', 'pay_interface_id'])
    def put(args):
        pay_interface_id = args['pay_interface_id']
        owner_id = args['owner_id']
        pay_version = args['pay_version']
        partner = args['partner']
        key = args['key']
        private_key = args['private_key']
        ali_public_key = args['ali_public_key']
        seller_email = args['seller_email']

        pay_interface = PayInterface.from_id({'id': pay_interface_id})
        try:
            config = AliPayConfig.create({
                'owner': owner_id,
                'pay_version': pay_version,
                'partner': partner,
                'key': key,
                'private_key': private_key,
                'ali_public_key': ali_public_key,
                'seller_email': seller_email
            })
            pay_interface.update_related_config_id(config_id=config.id)
            return {'msg': "create success"}
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return 500, {'msg': 'create ali pay interface config failed'}



    @param_required(['pay_interface_id','owner_id', 'pay_version', 'partner', 'key', 'private_key', 'ali_public_key', 'seller_email'])
    def post(args):
        pay_interface_id = args['pay_interface_id']
        owner_id = args['owner_id']
        pay_version = args['pay_version']
        partner = args['partner']
        key = args['key']
        private_key = args['private_key']
        ali_public_key = args['ali_public_key']
        seller_email = args['seller_email']

        pay_interface = PayInterface.from_id({'id': pay_interface_id})
        Ali_pay_config = AliPayConfig.from_id({'id': pay_interface.related_config_id})
        try:
            Ali_pay_config.update(
                pay_version=pay_version,
                partner=partner,
                key=key,
                private_key=private_key,
                ali_public_key=ali_public_key,
                seller_email=seller_email
            )
            return {'msg': "update success"}
        except:
            msg = unicode_full_stack()
            watchdog.error(msg)
            return 500, {'msg': 'update ali pay interface config failed'}
