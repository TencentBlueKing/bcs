# -*- coding: utf-8 -*-

from .python_atom_sdk import *
sdk = AtomSDK()


def validate_param(value, flag=""):
    if not value:
        sdk.log.error(u"参数【%s】不能为空", flag)
        exit(-1)

    return value


def validate_digit(value, flag=""):
    if not str(value).isdigit():
        sdk.log.error(u"参数【%s】不能为空", flag)
        exit(-1)
    
    return int(value)


def validate_gte_zero(value, flag=""):
    if not str(value).isdigit():
        sdk.log.error(u"参数【%s】不能为空", flag)
        exit(-1)
    # 转换为整数
    value = int(value)
    # 判断值大于0
    if value <= 0:
        sdk.log.error(u"参数【%s】不能必须大于0", flag)
        exit(-1)
    return value
