# -*- coding: utf-8 -*-
import time

from .python_atom_sdk import *
sdk = AtomSDK()

from . import base as params_utils
from components import bcs_app
from .constants import DELETE_OPER, WAIT_POLLING_TIME

from .polling_task import polling


def get_instance_id(cc_app_id, project_id, resource_kind, ns_name, app_name):
    data = bcs_app.get_instances(cc_app_id, project_id, resource_kind, ns_name)
    for info in data:
        if info["name"] == app_name:
            return info["id"]
    sdk.log.error(u"没有查询应用【%s】信息", app_name)
    exit(-1)


def delete(cc_app_id, project_id, params):
    """应用删除操作
    """
    sdk.log.info(u"开始执行删除操作...")
    ns_name = params_utils.get_namespace(params)
    resource_kind = params_utils.get_resource_kind(params)
    app_name = params_utils.get_app_name(params)
    instance_id = get_instance_id(cc_app_id, project_id, resource_kind, ns_name, app_name)
    # 下发删除操作
    data = {
        "inst_id_list": [instance_id]
    }
    bcs_app.delete_app(cc_app_id, project_id, data)
    # 等待10s
    time.sleep(WAIT_POLLING_TIME)
    # 轮训任务
    polling(cc_app_id, project_id, instance_id, op_type=DELETE_OPER)
