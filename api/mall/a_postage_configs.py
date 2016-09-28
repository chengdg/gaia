# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.mall.postage_config import PostageConfig


class APostageConfigs(api_resource.ApiResource):
    """
    运费模板集合
    """
    app = 'mall'
    resource = 'postage_configs'

    @param_required(['corp'])
    def get(args):
        corp = args['corp']
        postage_configs = corp.postage_config_repository.get_postage_configs()

        datas = []
        for postage_config in postage_configs:
            data = {
                "id": postage_config.id,
                "name": postage_config.name,
                "is_used": postage_config.is_used,
                "is_system_level_config": postage_config.is_system_level_config,
                "is_enable_special_config": postage_config.is_enable_special_config,
                "is_enable_free_config": postage_config.is_enable_free_config,
                "first_weight": postage_config.first_weight,
                "first_weight_price": postage_config.first_weight_price,
                "added_weight": postage_config.added_weight,
                "added_weight_price": postage_config.added_weight_price,
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

            datas.append(data)

        return {
            'postage_configs': datas
        }