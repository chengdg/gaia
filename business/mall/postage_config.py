# -*- coding: utf-8 -*-
import json

from eaglet.core import watchdog
from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource

from business import model as business_model
from db.account import models as account_model
from db.mall import models as mall_models


class PostageConfig(business_model.Model):
    """
    订单
    """

    __slots__ = (
        'id',
        'special_configs',
        'free_configs',
        'owner_id',
        'config'
    )

    def __init__(self, owner_id, id, special_configs, free_configs, config):
        business_model.Model.__init__(self)

        self.id = id,
        self.owner_id = owner_id,
        self.special_configs = special_configs
        self.free_configs = free_configs
        self.config = config

    @staticmethod
    @param_required(['id'])
    def get(args):
        id = args['id']
        owner_id = args['owner_id']
        postage_config = mall_models.PostageConfig.select().dj_where(id=id, owner_id=owner_id, is_delete=False).first()

        special_configs = map(lambda x: x.to_dict(),
                              mall_models.SpecialPostageConfig.select().dj_where(postage_config=postage_config))

        free_configs = map(lambda x: x.to_dict(),
                           mall_models.FreePostageConfig.select().dj_where(postage_config=postage_config))

        return PostageConfig(owner_id,id, special_configs, free_configs, postage_config.to_dict())
    
    @staticmethod
    @param_required([])
    def put(args):
        """

         创建运费模板

         Method: POST

         @param name 运费模板名
         @param firstWeight  默认运费的首重
         @param firstWeightPrice  默认运费的首重价格
         @param addedWeight  默认运费的续重
         @param addedWeightPrice  默认运费的续重价格
         @param isEnableSpecialConfig 是否启用“特殊地区运费”
         @param specialConfigs 特殊地区运费信息的json字符串
         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.c}
                 [{
                         destination: [上海, 北京, ...],
                         firstWeight: 1.0,
                         firstWeightPrice: 5.5,
                         addedWeight: 0.5,
                         addedWeightPrice: 3.0
                 }, {
                         ......
                 }]
         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
         @param isEnableFreeConfig 是否启用“特殊地区包邮条件”
         @param freeConfigs 特殊地区包邮条件的json字符串
         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.c}
                 [{
                         destination: [上海, 北京, ...],
                         condition: 'count', //count代表数量，price代表价格
                         value: 3 //condition条件需要满足的值
                 }, {
                         ......
                 }]
         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
         """
        name = args['name']
        first_weight = round(float(args['firstWeight']), 1)
        first_weight_price = round(float(args['firstWeightPrice']), 2)
        added_weight = round(float(args['addedWeight']), 1)
        added_weight_price = round(float(args['addedWeightPrice']), 2)
        is_enable_special_config = (args.get('isEnableSpecialConfig', 'false') == 'true')
        special_configs = json.loads(args.get('specialConfigs', '[]'))
        is_enable_free_config = (args.get('isEnableFreeConfig', 'false') == 'true')
        free_configs = json.loads(args.get('freeConfigs', '[]'))
        owner_id = args['owner_id']
        owner = account_model.User.get(id=owner_id)

        # 更新当前被使用的postage config状态
        mall_models.PostageConfig.update(is_used=False).dj_where(owner=owner, is_used=True)

        postage_config = mall_models.PostageConfig.create(
            owner=owner,
            name=name,
            first_weight=first_weight,
            first_weight_price=first_weight_price,
            added_weight=added_weight,
            added_weight_price=added_weight_price,
            is_enable_special_config=is_enable_special_config,
            is_enable_free_config=is_enable_free_config,
            is_used=True
        )

        if is_enable_special_config:

            for special_config in special_configs:
                special_config = mall_models.SpecialPostageConfig.create(
                    owner=owner,
                    postage_config=postage_config,
                    destination=','.join(special_config.get('destination', [])),
                    first_weight=round(float(special_config.get('firstWeight', 0.0)), 1),
                    first_weight_price=round(float(special_config.get('firstWeightPrice', 0.0)), 2),
                    added_weight=round(float(special_config.get('addedWeight', 0.0)), 1),
                    added_weight_price=round(float(special_config.get('addedWeightPrice', 0.0)), 2)
                )
        if is_enable_free_config:
            for free_config in free_configs:
                free_config = mall_models.FreePostageConfig.objects.create(
                    owner=owner,
                    postage_config=postage_config,
                    destination=','.join(free_config.get('destination', [])),
                    condition=free_config.get('condition', 'count'),
                    condition_value=free_config.get('value', 1)
                )


    @staticmethod
    @param_required([])
    def delete(args):
        mall_models.PostageConfig.update(is_used=False, is_deleted=True).dj_where(owner_id=args['owner_id'], id=args['id']).execute()
        mall_models.PostageConfig.update(is_used=True).dj_where(owner_id=args['owner_id'], is_system_level_config=True).execute()
        
    @staticmethod
    @param_required([])
    def update(args):
        is_used = args.get('is_used', None)
        name = args.get('name', None)
        owner_id = args['owner_id']
        if is_used and not name:
            mall_models.PostageConfig.update(is_used=False).dj_where(owner_id=owner_id, is_used=True).execute()
            mall_models.PostageConfig.update(is_used=True).dj_where(owner_id=owner_id, id=id).execute()
            return

        name = args['name']
        first_weight = args['firstWeight']
        first_weight_price = args['firstWeightPrice']
        added_weight = args['addedWeight']
        added_weight_price = args['addedWeightPrice']
        is_enable_special_config = (
            args.get(
                'isEnableSpecialConfig',
                'false') == 'true')
        special_configs = json.loads(args.get('specialConfigs', '[]'))
        is_enable_free_config = (
            args.get(
                'isEnableFreeConfig',
                'false') == 'true')
        free_configs = json.loads(args.get('freeConfigs', '[]'))

        mall_models.PostageConfig.update(
            name=name,
            first_weight=first_weight,
            first_weight_price=first_weight_price,
            added_weight=added_weight,
            added_weight_price=added_weight_price,
            is_enable_special_config=is_enable_special_config,
            is_enable_free_config=is_enable_free_config
        ).dj_where(id=id).execute()

        # 更新special config
        if is_enable_special_config:
            special_config_ids = set([config['id'] for config in special_configs])
            existed_special_config_ids = set(
                [config.id
                for config in
                mall_models.SpecialPostageConfig.select.dj_where(postage_config_id=id)])
            for special_config in special_configs:
                config_id = special_config['id']
                if config_id < 0:
                    special_config = mall_models.SpecialPostageConfig.create(
                        owner_id=owner_id,
                        postage_config_id=id,
                        destination=','.join(special_config.get('destination', [])),
                        first_weight=special_config.get('firstWeight', 0.0),
                        first_weight_price=special_config.get('firstWeightPrice', 0.0),
                        added_weight=special_config.get('addedWeight', 0.0),
                        added_weight_price=special_config.get('addedWeightPrice', 0.0)
                    )
                else:
                    mall_models.SpecialPostageConfig.update(
                        destination=','.join(special_config.get('destination', [])),
                        first_weight=special_config.get('firstWeight', 0.0),
                        first_weight_price=special_config.get('firstWeightPrice', 0.0),
                        added_weight=special_config.get('addedWeight', 0.0),
                        added_weight_price=special_config.get('addedWeightPrice', 0.0)
                    ).dj_where(id=config_id).execute()

            ids_to_be_delete = existed_special_config_ids - special_config_ids
            mall_models.SpecialPostageConfig.delete().dj_where(id__in=ids_to_be_delete)

        # 更新free config
        if is_enable_free_config:
            free_config_ids = set([config['id'] for config in free_configs])
            existed_free_config_ids = set(
                [config.id
                for config in
                mall_models.FreePostageConfig.select().dj_where(
                    postage_config_id=id)])
            for free_config in free_configs:
                config_id = free_config['id']
                if config_id < 0:
                    free_config = mall_models.FreePostageConfig.create(
                        owner_id=owner_id,
                        postage_config_id=id,
                        destination=','.join(free_config.get('destination', [])),
                        condition=free_config.get('condition', 'count'),
                        condition_value=free_config.get('value', 1)
                    )
                else:
                    mall_models.FreePostageConfig.update(
                        destination=','.join(free_config.get('destination', [])),
                        condition=free_config.get('condition', 'count'),
                        condition_value=free_config.get('value', 1).dj_where(id=config_id).execute()
                    )
            ids_to_be_delete = existed_free_config_ids - free_config_ids
            mall_models.FreePostageConfig.delete().dj_where(id__in=ids_to_be_delete).execute()
