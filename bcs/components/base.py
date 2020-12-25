# -*- coding: utf-8 -*-
import json

import requests

from bcs.python_atom_sdk import *
sdk = AtomSDK()

# 兼容字符串code
SUCCESS_CODE = [0, "0"]
TIMEOUT = 600
STATUS404 = 404


def http_request(method, url, params=None, data=None, **kwargs):
    try:
        resp = requests.request(method, url, params=params, json=data, timeout=TIMEOUT, **kwargs)
    except requests.exceptions.RequestException as e:
        sdk.log.error("request exceptions, %s", e)
        exit(-1)
    except Exception as e:
        sdk.log.error("request error, %s", e)
        exit(-1)

    resp_json = resp.json()
    # 判断是否为404
    if resp_json.get("code") == STATUS404:
        sdk.log.error("request api error, status code is 404")
        exit(-1)
    # 判断返回码是否正确
    if resp_json.get("code") not in SUCCESS_CODE:
        sdk.log.error("request api error, url: %s error: %s", url, resp_json.get("message"))
        exit(-1)

    return resp_json
