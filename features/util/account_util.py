# -*- coding: utf-8 -*-
from hashlib import md5


from db.account import models as account_models
from db.weixin import models as weixin_user_models
from db.webapp import models as webapp_models
from db.mall import models as mall_models
from features.util import bdd_util


MIXUP_FACTOR = 3179
WEIXIN_SITE_DOMAIN = 'm.weizoom.com'

GENERAL_CORP = account_models.WEBAPP_TYPE_MALL
WEIZOOM_CORP = account_models.WEBAPP_TYPE_WEIZOOM
SELF_RUN_PLATFORM = account_models.WEBAPP_TYPE_WEIZOOM_MALL


def __make_password(raw_password):
    import hashlib

    algorithm = 'sha1'
    salt = '69e44'
    hash = hashlib.sha1(salt + raw_password).hexdigest()
    return "%s$%s$%s" % (algorithm, salt, hash)


def __binding_wexin_mp_account(user=None):
    """
    绑定公众号
    """
    account_models.UserProfile.update(is_mp_registered=True).execute()

    #创建微信第三方开发平台数据
    if weixin_user_models.ComponentInfo.select().dj_where(is_active=True).count() == 0:
        component_info = weixin_user_models.ComponentInfo.create(
            app_id="wx8209f1f63f0b1d26",
            app_secret="component_secret",
            component_verify_ticket="",
            token="",
            ase_key="",
            component_access_token="",
            is_active=True
        )
    else:
        component_info = weixin_user_models.ComponentInfo.select().dj_where(is_active=True).get()

    if user:
        count = weixin_user_models.WeixinMpUser.select().dj_where(owner_id=user.id).count()
        if count == 0:
            mpuser = weixin_user_models.WeixinMpUser.create(
                owner = user,
                username = '',
                password= '',
                is_certified = True,
                is_service = True,
                is_active = True
            )

            weixin_user_models.WeixinMpUserAccessToken.create(mpuser=mpuser, is_active=True, app_id=user.id, app_secret='app_secret',  access_token='access_token')
            weixin_user_models.MpuserPreviewInfo.create(mpuser=mpuser, name=mpuser.username)
            auth_appid = weixin_user_models.ComponentAuthedAppid.create(component_info=component_info,user_id=user.id,authorizer_appid=user.id,is_active=True)

            weixin_user_models.ComponentAuthedAppidInfo.create(
                auth_appid=auth_appid,
                nick_name='',
                head_img='',
                service_type_info=2,
                verify_type_info=0,
                user_name='',
                alias='',
                qrcode_url='',
                appid=user.id,
                func_info=''
            )
        else:
            weixin_user_models.WeixinMpUser.update(is_certified=True, is_service=True, is_active=True).dj_where(owner_id=user.id).execute()
            if weixin_user_models.ComponentAuthedAppid.select().dj_where(component_info=component_info,user_id=user.id,authorizer_appid=user.id,is_active=True).count() == 0:
                auth_appid = weixin_user_models.ComponentAuthedAppid.create(component_info=component_info,user_id=user.id,authorizer_appid=user.id,is_active=True)
                weixin_user_models.ComponentAuthedAppidInfo.objects.create(
                    auth_appid=auth_appid,
                    nick_name='',
                    head_img='',
                    service_type_info=2,
                    verify_type_info=0,
                    user_name='',
                    alias='',
                    qrcode_url='',
                    appid=user.id,
                    func_info=''
                )


def __create_corp(username, display_name, webapp_type):
    """
    创建系统用户
    """
    if not display_name:
        display_name = username

    try:
        user = account_models.User.select().dj_where(username=username).get()
        #已经存在，不再创建
    except:
        user = account_models.User.create(
            username = username,
            first_name = display_name,
            password = __make_password('test')
        )

        profile = account_models.UserProfile.create(
            user = user,
            manager_id = user.id,
            webapp_id = 0,
            webapp_type = webapp_type
        )

        webapp_id = MIXUP_FACTOR + profile.id
        mp_url = 'http://%s/weixin/%d/' % (WEIXIN_SITE_DOMAIN, webapp_id)

        token_str = ('*)|%s12@' % mp_url).replace(WEIXIN_SITE_DOMAIN, 'balabalame')
        mp_token = md5(token_str).hexdigest()[1:-1]

        account_models.UserProfile.update(webapp_id=str(webapp_id), mp_url=mp_url, mp_token=mp_token).dj_where(id=profile.id).execute()

        webapp_models.WebApp.create(
            appid = '%s' % webapp_id,
            owner = user,
        )

        __binding_wexin_mp_account(user)

    client = bdd_util.login(user)
    data = {
        'corp_id': user.id
    }
    response = client.put('/mall/default_configs/', data)
    bdd_util.assert_api_call_success(response)

    return user


def __create_supplier(user):
    mall_models.Supplier.create(
        owner=user,
        name=user.username,
        supplier_tel='10086',
        supplier_address=u'火星',
        remark='aaaaaa'

    )

def create_general_corp(username, display_name=None):
    user = __create_corp(username, display_name, GENERAL_CORP)
    __create_supplier(user)
    return user


def create_weizoom_corp(username, display_name=None):
    return __create_corp(username, display_name, SELF_RUN_PLATFORM)


def create_self_run_platform(username, display_name=None):
    return __create_corp(username, display_name, WEIZOOM_CORP)
