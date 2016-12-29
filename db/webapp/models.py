# -*- coding: utf-8 -*-

from eaglet.core.db import models

from db.account.models import User, UserProfile

#########################################################################
# App：App信息
#########################################################################
class WebApp(models.Model):
    owner = models.ForeignKey(User)
    appid = models.CharField(max_length=16)
    name = models.CharField(max_length=100, default='')

    class Meta(object):
        db_table = 'webapp'

#########################################################################
# PageVisitLog：Page访问日志
#########################################################################
class PageVisitLog(models.Model):
    webapp_id = models.CharField(max_length=16)
    token = models.CharField(max_length=64, blank=True)
    url = models.CharField(max_length=1024)
    is_from_mobile_phone = models.BooleanField()
    create_date = models.DateField(auto_now_add=True) #访问日期
    created_at = models.DateTimeField(auto_now_add=True) #访问时间

    class Meta(object):
        db_table = 'webapp_page_visit_log'


#########################################################################
# PageVisitDailyStatistics：Page访问统计结果
#########################################################################
URL_TYPE_ALL = 0
URL_TYPE_SPECIFIC = 1
USER_STATUSES = (
    (URL_TYPE_ALL, u'总计'),
    (URL_TYPE_SPECIFIC, u'独立')
)
class PageVisitDailyStatistics(models.Model):
    webapp_id = models.CharField(max_length=16)
    url_type = models.IntegerField(default=URL_TYPE_SPECIFIC, choices=USER_STATUSES)
    url = models.CharField(max_length=1024, default='')
    pv_count = models.IntegerField(default=0) #pv
    uv_count = models.IntegerField(default=0) #uv
    data_date = models.DateField() #统计日期

    class Meta(object):
        db_table = 'webapp_page_visit_daily_statistics'

