# -*- coding: utf-8 -*-

import settings
import json

class FilterParser(object):
    """
    解析filter dict，并生成可用于peewee的查询条件
    """

    def __init__(self):
        pass

    def get_filter_key(self, key, filter2field=None):
        _, name, match_strategy = key[2:].split('-')
        if filter2field:
            name = filter2field.get(name, name)

        if match_strategy == 'equal':
            return name
        elif match_strategy == 'contain' or match_strategy == 'contains':
            return '%s__icontains' % name
        elif match_strategy == 'gte':
            return '%s__gte' % name
        elif match_strategy == 'lte':
            return '%s__lte' % name
        elif match_strategy == 'range':
            return '%s__range' % name
        elif match_strategy == 'notin':
            return '%s__notin' % name
        elif match_strategy == 'in':
            return '%s__in' % name
        else:
            return name

    def get_filter_value(self, key, filter_options):
        _, _, match_strategy = key[2:].split('-')
        if match_strategy == 'range' or match_strategy == 'in' or match_strategy == 'notin':
            value = json.loads(filter_options[key])
            return tuple(value)
        else:
            return filter_options[key]

    def parse(self, filters, filter2field=None):
        """
        将filters中的所有filter转换成peewee查询条件
        """
        peewee_query = {}
        if not filters:
            return peewee_query

        for filter_express, value in filters.items():
            if not filter_express.startswith('__f-'):
                continue

            key = self.get_filter_key(filter_express, filter2field)

            if value:
                #当value有效时，才记录其为过滤项，可以解决dj_where(id__in=[])的问题
                peewee_query[key] = self.get_filter_value(filter_express, filters)

        return peewee_query

    def parse_key(self, filters, key, filter2field=None):
        """
        将filters中的一个filter转换成peewee查询条件
        """
        peewee_query = {}
        if not filters:
            return peewee_query

        if not key in filters:
            return peewee_query

        value = filters[key]
        key = self.get_filter_key(key, filter2field)
        peewee_query[key] = value

        return peewee_query

    def extract_by_keys(self, filters, key_map):
        """
        获取filters中的由key_map指定的子集
        """
        result = {}
        for key, maped_key in key_map.items():
            if not maped_key:
                maped_key = key
            result[maped_key] = filters[key]
        return result

    @staticmethod
    def get():
        return FilterParser()