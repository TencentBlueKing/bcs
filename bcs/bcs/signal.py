# -*- coding: utf-8 -*-

from .python_atom_sdk import *
sdk = AtomSDK()

from .utils import validate_param, validate_digit
from .constants import MESOS_APPLICATION_RESOURCE
from components import bcs_app

from .base import get_resource_kind, get_namespace, get_app_name


def get_instance_id(cc_app_id, project_id, resource_kind, ns_name, app_name):
    data = bcs_app.get_instances(cc_app_id, project_id, resource_kind, ns_name)
    for info in data:
        if info["name"] == app_name:
            return info["id"]
    sdk.log.error(u"没有查询应用【%s】信息", app_name)
    exit(-1)


def get_process_name(params):
    process_name = params.get("process_name")
    validate_param(process_name, flag=u"进程名称")
    return process_name


def get_signal_value(params):
    signal_val = params.get("signal")
    validate_digit(signal_val, flag=u"信号值")
    return signal_val


def signal(cc_app_id, project_id, params):
    """发送信号功能
    """
    sdk.log.info(u"开始发送信号...")
    ns_name = get_namespace(params)
    resource_kind = get_resource_kind(params)
    app_name = get_app_name(params)
    instance_id = get_instance_id(cc_app_id, project_id, resource_kind, ns_name, app_name)
    data = {
        "inst_id_list": [instance_id],
        "signal_info": {
            "process_name": get_process_name(params),
            "signal": get_signal_value(params)
        }
    }
    if resource_kind == MESOS_APPLICATION_RESOURCE:
        bcs_app.signal_for_application(cc_app_id, project_id, data)
        return
    bcs_app.signal_for_deployment(cc_app_id, project_id, data)
    sdk.log.info(u"信号发送成功!")
