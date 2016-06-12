# -*- coding: utf-8 -*-

import os
import logging


DEBUG = True
PROJECT_HOME = os.path.dirname(os.path.abspath(__file__))

MODE = 'debug'
SERVICE_NAME = 'zeus'
DEV_SERVER_MULTITHREADING = True
DOMAIN = "dev.weapp.com"
DATABASES = {
    'default': {
        'ENGINE': 'mysql+retry',
        'NAME': 'weapp',
        'USER': 'weapp',
        'PASSWORD': 'weizoom',
        'HOST': 'db.zeus.com',
        'PORT': '',
        'CONN_MAX_AGE': 100
    },
    'watchdog': {
        'ENGINE': 'mysql+retry',
        'NAME': 'weapp',
        'USER': 'weapp',
        'PASSWORD': 'weizoom',
        'HOST': 'db.zeus.com',
        'PORT': '',
        'CONN_MAX_AGE': 100
    }
}


MIDDLEWARES = [
    'eaglet.middlewares.debug_middleware.QueryMonitorMiddleware',
    'eaglet.middlewares.debug_middleware.RedisMiddleware',

    #账号信息中间件
    #'middleware.webapp_account_middleware.WebAppAccountMiddleware',
]
#sevice celery 相关
EVENT_DISPATCHER = 'redis'

# settings for WAPI Logger
if MODE == 'develop':
    WAPI_LOGGER_ENABLED = False # Debug环境下不记录wapi详细数据
    WAPI_LOGGER_SERVER_HOST = 'mongo.weapp.com'
    WAPI_LOGGER_SERVER_PORT = 27017
    WAPI_LOGGER_DB = 'wapi'
    IMAGE_HOST = 'http://dev.weapp.com'
    PAY_HOST = 'api.weapp.com'
    #sevice celery 相关
    EVENT_DISPATCHER = 'local'
    ENABLE_SQL_LOG = False

    logging.basicConfig(
        format='[%(asctime)s] %(name)s %(levelname)s %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO
    )
    WEAPP_HOST = "http://dev.weapp.com/"
    H5_HOST = "http://h5.weapp.com/"
else:
    # 真实环境暂时关闭
    #WAPI_LOGGER_ENABLED = False
    # 生产环境开启API Logger
    WAPI_LOGGER_ENABLED = True
    WAPI_LOGGER_SERVER_HOST = 'mongo.weapp.com'
    WAPI_LOGGER_SERVER_PORT = 27017
    WAPI_LOGGER_DB = 'wapi'
    IMAGE_HOST = 'http://dev.weapp.com'
    PAY_HOST = 'api.weapp.com'
    ENABLE_SQL_LOG = False

    logging.basicConfig(
        format='[%(asctime)s] %(name)s %(levelname)s %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO
    )
    WEAPP_HOST = "http://weapp.weizoom.com/"
    H5_HOST = "http://mall.weizoom.com/"

#缓存相关配置
REDIS_HOST = 'redis.weapp.com'
REDIS_PORT = 6379
REDIS_CACHES_DB = 1
REDIS_CACHE_KEY = ':1:api'

#BDD相关配置
WEAPP_DIR = '../weapp'
WEAPP_BDD_SERVER_HOST = '127.0.0.1'
WEAPP_BDD_SERVER_PORT = 8170
ENABLE_BDD_DUMP_RESPONSE = True

#watchdog相关
WATCH_DOG_DEVICE = 'mysql'
WATCH_DOG_LEVEL = 200
IS_UNDER_BDD = False
# 是否开启TaskQueue(基于Celery)
TASKQUEUE_ENABLED = True


# Celery for Falcon
INSTALLED_TASKS = [
    #'resource.member.tasks',
    # 'core.watchdog.tasks',
    'wapi.tasks',

    # 'services.example_service.tasks.example_log_service',
    # 'services.order_notify_mail_service.task.notify_order_mail',
    # 'services.record_member_pv_service.task.record_member_pv',
    # 'services.update_member_from_weixin.task.update_member_info',
]

#redis celery相关
REDIS_SERVICE_DB = 2

CTYPT_INFO = {
    'id': 'weizoom_h5',
    'token': '2950d602ffb613f47d7ec17d0a802b',
    'encodingAESKey': 'BPQSp7DFZSs1lz3EBEoIGe6RVCJCFTnGim2mzJw5W4I'
}

COMPONENT_INFO = {
    'app_id' : 'wx9b89fe19768a02d2',
}
