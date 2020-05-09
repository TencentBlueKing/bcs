# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from .python_atom_sdk import *
sdk = AtomSDK()

from .rollingupdate import rollingupdate
from .command import command
from .create import create
from .recreate import recreate
from .scale import scale
from .signal import signal
from .delete import delete

from .constants import MESOS_RESOURCE_KIND_MAP
from .base import get_project_id, get_resource_kind
from components import bcs_app

###########################################################
# 因为蓝盾和容器服务的项目现阶段没有关联，因此，需要用户自己选择项目
###########################################################

OPER_FUNC_MAP = {
    "rollingupdate": rollingupdate,
    "command": command,
    "create": create,
    "recreate": recreate,
    "scale": scale,
    "signal": signal,
    "delete": delete
}


def get_func(params):
    oper_type = params.get("oper_type")
    if oper_type not in OPER_FUNC_MAP:
        sdk.log.error(u"操作类型不正确，当前的操作类型为: %s", oper_type)
        exit(-1)
    return OPER_FUNC_MAP[oper_type]


def main():
    # 获取project id
    params = sdk.get_input()
    project_id = get_project_id(params)
    cc_app_id = bcs_app.get_cc_app_id(project_id)
    # 针对mesos，仅支持
    if get_resource_kind(params) not in MESOS_RESOURCE_KIND_MAP.keys():
        sdk.log.error(u"资源类型不正确，MESOS仅支持【%s】", ";".join(MESOS_RESOURCE_KIND_MAP.keys()))
        exit(-1)
    # 执行相应的操作
    get_func(params)(cc_app_id, project_id, params)
