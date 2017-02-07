# -*- coding: utf-8 -*-

import os
import logging


PROJECT_HOME = os.path.dirname(os.path.abspath(__file__))

MODE = os.environ.get('_SERVICE_MODE', 'develop')
SERVICE_NAME = 'gaia'
DEV_SERVER_MULTITHREADING = False
WEAPP_DOMAIN = "weapp.weizoom.com"
HERMES_DOMAIN = "weapp.weizoom.com"
# DB_HOST = os.environ.get('DB_HOST', None) or '103.29.16.139'
DB_HOST = os.environ.get('DB_HOST', 'db.dev.com')
DB_PORT = os.environ.get('DB_PORT', '3306')

DATABASES = {
    'default': {
        'ENGINE': 'mysql+retry',
        #'NAME': 'new_zeus',
        'NAME': 'weapp',
        'USER': 'weapp',
        'PASSWORD': 'weizoom',
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        # 'HOST': '103.29.16.139',#WEAPP_DB_HOST,
        # 'PORT': '',
        'CONN_MAX_AGE': 100
    }
}


MIDDLEWARES = [
    'eaglet.middlewares.debug_middleware.QueryMonitorMiddleware',
    'eaglet.middlewares.debug_middleware.RedisMiddleware',
    'eaglet.middlewares.zipkin_middleware.ZipkinMiddleware',
    #账号信息中间件
    #'middleware.webapp_account_middleware.WebAppAccountMiddleware',
    'middleware.account_middleware.AccountMiddleware',
]
#sevice celery 相关
EVENT_DISPATCHER = 'redis'

#信息输出配置
DUMP_API_CALL_RESULT = True
DUMP_FORMATTED_INNER_ERROR_MSG = False
ENABLE_CONSOLE = (os.environ.get('_ENABLE_API_SERVICE_CONSOLE', '0') == '1')

# settings for WAPI Logger
if 'develop' == MODE:
    WAPI_LOGGER_ENABLED = False # Debug环境下不记录wapi详细数据
    WAPI_LOGGER_SERVER_HOST = 'mongo.weapp.com'
    WAPI_LOGGER_SERVER_PORT = 27017
    WAPI_LOGGER_DB = 'wapi'
    IMAGE_HOST = ''
    PAY_HOST = 'api.weapp.com'
    #sevice celery 相关
    EVENT_DISPATCHER = 'local'
    ENABLE_SQL_LOG = False

    WEAPP_HOST = "http://dev.weapp.com/"
    H5_HOST = "http://h5.weapp.com/"

    DUMP_READABLE_EXCEPTION_STACK = True
    ENABLE_SQL_LOG = False #是否dump peewee产生的sql查询
else:
    # 真实环境暂时关闭
    #WAPI_LOGGER_ENABLED = False
    # 生产环境开启API Logger
    WAPI_LOGGER_ENABLED = False
    WAPI_LOGGER_SERVER_HOST = 'mongo.weapp.com'
    WAPI_LOGGER_SERVER_PORT = 27017
    WAPI_LOGGER_DB = 'wapi'
    IMAGE_HOST = 'http://dev.weapp.com'
    PAY_HOST = 'api.weapp.com'
    ENABLE_SQL_LOG = False
    WEAPP_HOST = "http://weapp.weizoom.com/"
    H5_HOST = "http://mall.weizoom.com/"
    ENABLE_SQL_LOG = False #是否dump peewee产生的sql查询

if 'develop' == MODE:
    DEBUG = True
elif 'test' == MODE:
    DEBUG = True
else:
    DEBUG = False

#缓存相关配置
REDIS_HOST = os.environ.get('_REDIS_HOST', 'redis.weapp.com')
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

MAIL_NOTIFY_USERNAME = u'noreply@notice.weizoom.com'
MAIL_NOTIFY_PASSWORD = u'Weizoom2015'
MAIL_NOTIFY_ACCOUNT_SMTP = u'smtp.dm.aliyun.com'


# settings for WAPI Logger
# if MODE == 'develop' or MODE == 'test':
if 'develop' == MODE or'test' == MODE:
    EN_VARNISH = False
    #WAPI_ACCESS_TOKEN_REQUIRED = True
else:

    EN_VARNISH = True

if 'develop' == MODE:
    DOMAIN = 'dev.weapp.com'
    H5_DOMAIN = 'mall.weizoom.com'
elif 'test' == MODE:
    DOMAIN = 'testweapp.weizoom.com'
    H5_DOMAIN = 'mall.weizoom.com'
else:
    DOMAIN = 'weapp.weizoom.com'
    H5_DOMAIN = 'mall.weizoom.com'


if 'deploy' == MODE:
    MNS_ACCESS_KEY_ID = 'LTAICKQ4rQBofAhF'
    MNS_ACCESS_KEY_SECRET = 'bPKU71c0cfrui4bWgGPO96tLiOJ0PZ'
    MNS_ENDPOINT = 'http://1615750970594173.mns.cn-hangzhou.aliyuncs.com/'
    MNS_SECURITY_TOKEN = ''

else:
    MNS_ACCESS_KEY_ID = 'LTAICKQ4rQBofAhF'
    MNS_ACCESS_KEY_SECRET = 'bPKU71c0cfrui4bWgGPO96tLiOJ0PZ'
    MNS_ENDPOINT = 'https://1615750970594173.mns.cn-beijing.aliyuncs.com/'
    MNS_SECURITY_TOKEN = ''

if 'develop' == MODE:
    MESSAGE_DEBUG_MODE = True
else:
    MESSAGE_DEBUG_MODE = False


REDIS_QUEUE_DB = 8
TOPIC2QUEUES = {
    'test-topic': ['test-order-trade-center'],
    'test-weixin-topic': ['test-weixin-topic']
}

# BDD_SERVER相关配置
BDD_SERVER2PORT = {
    'weapp': 8170,
    'weizoom_card': 8171,
    'apiserver': 8172
}

PROMOTION_RESULT_VERSION = '2' #促销结果数据版本号

# redis锁，前缀lk
REGISTERED_LOCK_NAMES = {
	'__prefix': 'lk:',
	'order_action': 'o_ac:',
}