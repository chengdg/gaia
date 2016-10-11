# -*- coding: utf-8 -*-

import settings

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
        else:
            return name

    def get_filter_value(key, filter_options):
        _, _, match_strategy = key[2:].split('-')
        if match_strategy == 'range':
            value = json.loads(filter_options[key])
            return tuple(value)
        else:
            return filter_options[key]

    def parse(self, filters, filter2field=None):
        peewee_query = {}
        if not filters:
            return peewee_query

        for filter_express, value in filters.items():
            if not filter_express.startswith('__f-'):
                continue

            key = self.get_filter_key(filter_express)
            peewee_query[key] = value

        return peewee_query

    @staticmethod
    def get():
        return FilterParser()