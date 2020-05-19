# -*- coding: utf-8 -*-
import time

from .python_atom_sdk import *
sdk = AtomSDK()

from .base import get_resource_kind, get_namespace, get_app_name
from .utils import validate_param, validate_digit
from .polling_task import polling
from .constants import WAIT_POLLING_TIME
from components import bcs_app


def get_instance_id(cc_app_id, project_id, resource_kind, ns_name, app_name):
    data = bcs_app.get_instances(cc_app_id, project_id, resource_kind, ns_name)
    for info in data:
        if info["name"] == app_name:
            return info["id"]
    sdk.log.error(u"没有查询应用【%s】信息", app_name)
    exit(-1)


def get_instance_count(params):
    instance_count = params.get("instance_count")
    instance_count = validate_param(instance_count, flag=u"应用实例个数")
    return instance_count


def scale(cc_app_id, project_id, params):
    """应用扩缩容功能
    """
    sdk.log.info(u"应用开始重新创建...")
    ns_name = get_namespace(params)
    resource_kind = get_resource_kind(params)
    app_name = get_app_name(params)
    instance_id = get_instance_id(cc_app_id, project_id, resource_kind, ns_name, app_name)
    instance_count = get_instance_count(params)
    # 下发任务
    params = {"instance_num": instance_count}
    data = {"inst_id_list": [instance_id]}
    bcs_app.scale_app(cc_app_id, project_id, params, data)
    # 等待10s
    time.sleep(WAIT_POLLING_TIME)
    # 开始轮训任务
    polling(cc_app_id, project_id, instance_id)
