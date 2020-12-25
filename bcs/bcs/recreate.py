# -*- coding: utf-8 -*-
import time

from components import bcs_app

from .python_atom_sdk import *
sdk = AtomSDK()

from .base import get_resource_kind, get_namespace, get_app_name
from .utils import validate_gte_zero
from .polling_task import polling
from .constants import WAIT_POLLING_TIME


def get_instance_id(cc_app_id, project_id, resource_kind, ns_name, app_name):
    data = bcs_app.get_instances(cc_app_id, project_id, resource_kind, ns_name)
    for info in data:
        if info["name"] == app_name:
            return info["id"]
    sdk.log.error(u"没有查询应用【%s】信息", app_name)
    exit(-1)


def recreate(cc_app_id, project_id, params):
    """重新创建功能
    """
    sdk.log.info(u"应用开始重新创建...")
    ns_name = get_namespace(params)
    resource_kind = get_resource_kind(params)
    app_name = get_app_name(params)
    instance_id = get_instance_id(cc_app_id, project_id, resource_kind, ns_name, app_name)
    # 触发重建任务
    data = {
        "inst_id_list": [instance_id]
    }
    bcs_app.recreate_app(cc_app_id, project_id, data)
    # 等待10s
    time.sleep(WAIT_POLLING_TIME)
    # 轮训重建任务
    timeout = validate_gte_zero(params.get("timeout"), flag=u"任务超时时间")
    polling(cc_app_id, project_id, instance_id, timeout=timeout)
