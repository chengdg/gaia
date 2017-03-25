# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required


class APostageConfigs(api_resource.ApiResource):
    """
    运费模板集合
    """
    app = 'mall'
    resource = 'postage_configs'

    @param_required(['corp_id'])
    def get(args):
        corp = args['corp']
        postage_configs = corp.postage_config_repository.get_postage_configs()

        datas = []
        for postage_config in postage_configs:
            default_config = postage_config.default_config
            data = {
                "id": postage_config.id,
                "name": postage_config.name,
                "is_used": postage_config.is_used,
                "is_system_level_config": postage_config.is_system_level_config,
                "is_enable_special_config": postage_config.is_enable_special_config,
                "is_enable_free_config": postage_config.is_enable_free_config,
                "default_config": {
                    "first_weight": default_config.first_weight,
                    "first_weight_price": default_config.first_weight_price,
                    "added_weight": default_config.added_weight,
                    "added_weight_price": default_config.added_weight_price
                },
                "special_configs": []
            }

            for special_config in postage_config.special_configs:
                data['special_configs'].append({
                    "id": special_config.id,
                    "destinations": special_config.destinations,
                    "first_weight": special_config.first_weight,
                    "first_weight_price": special_config.first_weight_price,
                    "added_weight": special_config.added_weight,
                    "added_weight_price": special_config.added_weight_price
                })

            for free_config in postage_config.free_configs:
                data['free_configs'].append({
                    "id": free_config.id,
                    "destinations": free_config.destinations,
                    "condition": free_config.condition,
                    "value": free_config.condition_value
                })

            datas.append(data)

        return {
            'postage_configs': datas
        }