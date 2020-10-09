# -*- coding: utf-8 -*-
"""
发送命令操作
"""
import json

from .python_atom_sdk import *

from .base import get_project_id, get_resource_kind, get_namespace, get_app_name
from .utils import validate_param, validate_gte_zero
from .polling_task import command_polling
from components import bcs_app

sdk = AtomSDK()


def get_command(params):
    command = params.get("command")
    validate_param(command, flag=u"命令")
    return [command]


def get_command_vars(params):
    command_vars = params.get("command_vars")
    if not command_vars:
        return []
    return [command_vars]


def get_username(params):
    username = params.get("username")
    return username or "root"


def get_workdir(params):
    workdir = params.get("workdir")
    return workdir


def get_privileged(params):
    privileged = params.get("privileged")
    return privileged or False


def get_reserve_time(params):
    reserve_time = params.get("reserve_time")
    return reserve_time


def get_vars(params):
    """command需要的格式为[{key1: val1}, {key2: val2}]
    """
    vars = params.get("dict_vars")
    if not vars:
        return []
    try:
        vars = json.loads(vars)
    except Exception as err:
        sdk.log.error(u"参数【环境变量】格式不正确, 错误: %s", str(err))
        exit(-1)
    if not vars:
        return []
    return ["%s=%s" %(key, val) for key, val in vars.items()]


def get_instance_id(cc_app_id, project_id, resource_kind, ns_name, app_name):
    data = bcs_app.get_instances(cc_app_id, project_id, resource_kind, ns_name)
    for info in data:
        if info["name"] == app_name:
            return info["id"]
    sdk.log.error(u"没有查询应用【%s】信息", app_name)
    exit(-1)


def command(cc_app_id, project_id, params):
    sdk.log.info(u"开始执行发送命令操作...")
    # 获取参数
    resource_kind = get_resource_kind(params)
    ns_name = get_namespace(params)
    app_name = get_app_name(params)
    # 获取app id
    instance_id = get_instance_id(cc_app_id, project_id, resource_kind, ns_name, app_name)
    command = get_command(params)
    command_vars = get_command_vars(params)
    # 组装为["命令", "参数"]
    command.extend(command_vars)
    req_data = {
        "env": get_vars(params),
        "command": command,
        "username": get_username(params),
        "privileged": get_privileged(params)
    }
    workdir = get_workdir(params)
    if workdir:
        req_data["work_dir"] = workdir
    reserve_time = get_reserve_time(params)
    if reserve_time:
        req_data["reserve_time"] = reserve_time
    task_id = bcs_app.send_command(cc_app_id, project_id, instance_id, req_data)
    # 开始轮训任务状态
    # 获取超时时间
    timeout = validate_gte_zero(params.get("timeout"), flag=u"任务超时时间")
    command_polling(cc_app_id, project_id, instance_id, task_id, timeout=timeout)
