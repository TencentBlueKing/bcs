# -*- coding: utf-8 -*-
"""
滚动升级操作
"""
import time

from .python_atom_sdk import *
sdk = AtomSDK()

from .constants import MESOS_DEPLOYMENT_RESOURCE, WAIT_POLLING_TIME
from .utils import validate_param, validate_gte_zero
from .polling_task import polling
from .base import get_project_id, get_resource_kind, get_namespace, get_app_name
from components import bcs_app


def get_cluster_id(params):
    cluster_id = params.get("cluster_id")
    validate_param(cluster_id, flag=u"集群")
    return cluster_id


def get_instance_count(params):
    instance_count = params.get("instance_count")
    validate_param(instance_count, flag=u"应用实例个数")
    return int(instance_count)


def get_tmpl_version(params):
    version_name = params.get("template_set_version")
    validate_param(version_name, flag=u"模板集版本")
    return version_name


def get_instance_id(cc_app_id, project_id, resource_kind, ns_name, app_name):
    data = bcs_app.get_instances(cc_app_id, project_id, resource_kind, ns_name)
    for info in data:
        if info["name"] == app_name:
            return info["id"]
    sdk.log.error(u"没有查询应用【%s】信息", app_name)
    exit(-1)


def get_version_id_by_name(cc_app_id, project_id, instance_id, version_name):
    data = bcs_app.get_versions_by_resource(cc_app_id, project_id, instance_id)
    for info in data:
        if info["name"] == version_name:
            return info["id"]
    sdk.log.error(u"没有查询到版本【%s】的信息", version_name)
    exit(-1)


def rollingupdate(cc_app_id, project_id, params):
    sdk.log.info(u"开始滚动升级...")
    cluster_id = get_cluster_id(params)
    cluster_list = bcs_app.get_cluster_list(project_id)
    if cluster_id not in [info["cluster_id"] for info in cluster_list]:
        sdk.log.error(u"当前项目没有查询到对应的集群信息，集群: %s", cluster_id)
        exit(-1)
    # 获取资源类型
    resource_kind = get_resource_kind(params)
    # 获取命名空间名称
    ns_name = get_namespace(params)
    instance_count = get_instance_count(params)
    app_name = get_app_name(params)
    # 获取应用ID
    instance_id = get_instance_id(cc_app_id, project_id, resource_kind, ns_name, app_name)
    # 获取版本ID
    version_name = get_tmpl_version(params)
    version_id = get_version_id_by_name(cc_app_id, project_id, instance_id, version_name)
    # 调用接口
    req_params = {
        "version_id": version_id,
        "category": resource_kind,
        "instance_num": instance_count
    }
    params_vars = params.get("vars") or '{}'
    data = {
        "variable": json.loads(params_vars)
    }
    bcs_app.rollingupdate_app_new(cc_app_id, project_id, instance_id, req_params, data)
    # 等待10s，然后再轮训
    time.sleep(WAIT_POLLING_TIME)
    # 轮训任务状态
    timeout = validate_gte_zero(params.get("timeout"), flag=u"任务超时时间")
    polling(cc_app_id, project_id, instance_id, timeout=timeout)
