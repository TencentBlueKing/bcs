# -*- coding: utf-8 -*-

from bcs.python_atom_sdk import *
sdk = AtomSDK()

from .base import http_request

APP_CODE = sdk.get_sensitive_conf("APP_CODE")
APP_SECRET = sdk.get_sensitive_conf("APP_SECRET")
IAM_HOST = sdk.get_sensitive_conf("IAM_HOST")


def get_access_token():
    """获取非用户态access_token
    """
    if not IAM_HOST:
        sdk.log.error(u"IAM HOST为空，请在【设置】->【私有配置】中设置配置【IAM_HOST】对应的值")
        exit(-1)
    url = "{}/bkiam/api/v1/auth/access-tokens".format(IAM_HOST)
    data = {
        'grant_type': 'client_credentials',
        'id_provider': 'client'
    }
    headers = {
        "X-BK-APP-CODE": APP_CODE,
        "X-BK-APP-SECRET": APP_SECRET

    }
    resp = http_request("POST", url, data=data, headers=headers)
    access_token = resp.get("data", {}).get("access_token")
    if not access_token:
        sdk.log.error(u"获取access_token失败")
        exit(-1)
    return access_token

