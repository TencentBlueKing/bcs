# -*- coding: utf-8 -*-
import time

from .python_atom_sdk import *
sdk = AtomSDK()

from .base import get_resource_kind, get_namespace
from .utils import validate_param
from .constants import MESOS_RESOURCE_KIND_MAP, WAIT_POLLING_TIME
from .polling_task import polling
from components import bcs_app


def get_cluster_id(params):
    cluster_id = params.get("cluster_id")
    validate_param(cluster_id, flag=u"集群")
    return cluster_id


def get_tmpl_set(params):
    tmpl_set_name = params.get("template_set")
    validate_param(tmpl_set_name, flag=u"模板集")
    return tmpl_set_name


def get_tmpl_set_version(params):
    tmpl_set_version = params.get("template_set_version_for_create")
    validate_param(tmpl_set_version, flag=u"模板集版本")
    return tmpl_set_version


def get_tmpl(params):
    tmpl_name = params.get("template_name")
    validate_param(tmpl_name, flag=u"模板")
    return tmpl_name


def get_tmpl_set_id(tmpl_set_name, tmpl_set_data):
    for info in tmpl_set_data: 
        if info["name"] == tmpl_set_name:
            return info["id"]
    sdk.log.error(u"没有查询到模板集【%s】", tmpl_set_name)
    exit(-1)


def get_tmpl_version_info(tmpl_set_version, tmpl_set_versions):
    for info in tmpl_set_versions:
        if info["version"] == tmpl_set_version:
            return info
    sdk.log.error(u"没有查询到版本为【%s】的模板集", tmpl_set_version)
    exit(-1)


def get_tmpl_detail(resource_kind, version_tmpls, tmpl_name):
    tmpl_kind = MESOS_RESOURCE_KIND_MAP.get(resource_kind)
    if not tmpl_kind:
        sdk.log.error(u"类型不正确，仅支持【%s】类型", ";".join(MESOS_RESOURCE_KIND_MAP.keys()))
        exit(-1)
    kind_data = version_tmpls.get(tmpl_kind)
    if not kind_data:
        sdk.log.error(u"模板集中没有查询到对应的类型【%s】模板", resource_kind)
        exit(-1)
    # 获取模板信息
    for info in kind_data:
        if info["name"] == tmpl_name:
            return info
    sdk.log.error(u"模板集中没有查询到模板，类型:%s, 名称: %s", resource_kind, tmpl_name)
    exit(-1)


def create(cc_app_id, project_id, params):
    """创建实例操作
    """
    sdk.log.info(u"模板集实例化...")
    # 通过模板集名称获取模板集ID
    tmpl_set_data = bcs_app.get_template_sets(cc_app_id, project_id)
    tmpl_set_name = get_tmpl_set(params)
    tmpl_set_id = get_tmpl_set_id(tmpl_set_name, tmpl_set_data)
    # 获取版本信息
    tmpl_set_versions = bcs_app.get_template_set_versions(cc_app_id, project_id, tmpl_set_id)
    tmpl_set_version = get_tmpl_set_version(params)
    version_info = get_tmpl_version_info(tmpl_set_version, tmpl_set_versions)
    # 获取版本对应的模板详情
    version_tmpls = bcs_app.get_version_detail(cc_app_id, project_id, version_info["id"])
    resource_kind = get_resource_kind(params)
    tmpl_name = get_tmpl(params)
    tmpl_info = get_tmpl_detail(resource_kind, version_tmpls, tmpl_name)
    cluster_id = get_cluster_id(params)
    params_vars = json.loads(params.get("vars") or "{}")
    ns_name = get_namespace(params)
    data = {
        "cluster_ns_info": {
            cluster_id: {
                ns_name: params_vars
            }
        },
        "version_id": version_info["id"],
        "show_version_id": version_info["show_version_id"],
        "show_version_name": version_info["show_version_name"],
        "instance_entity": {
            resource_kind: [tmpl_info]
        }
    }
    # 下发实例化任务
    data = bcs_app.create_app(cc_app_id, project_id, data)
    instance_id_list = data.get("inst_id_list")
    if not instance_id_list:
        sdk.log.error(u"实例化应用异常，没有生成对应的应用ID")
        exit(-1)
    # 等待10s
    time.sleep(WAIT_POLLING_TIME)
    # 轮训任务状态
    polling(cc_app_id, project_id, instance_id_list[0])
