# -*- coding: utf-8 -*-
# 获取公共参数及公共处理流程
from .python_atom_sdk import *

from .utils import validate_param
from .constants import MESOS_DEPLOYMENT_RESOURCE

sdk = AtomSDK()


def get_project_id(params):
    """获取项目的project_id"""
    project_id = params.get("project_id")
    validate_param(project_id, flag=u"项目信息")
    return project_id


def get_resource_kind(params):
    resource_kind = params.get("resource_kind")
    validate_param(resource_kind, flag=u"资源类型")
    if resource_kind != MESOS_DEPLOYMENT_RESOURCE:
        sdk.log.error(u"滚动升级允许的资源类型为Deployment")
        exit(-1)
    return resource_kind


def get_namespace(params):
    ns_name = params.get("namespace_name")
    validate_param(ns_name, flag=u"命名空间名称")
    return ns_name


def get_app_name(params):
    app_name = params.get("app_name")
    validate_param(app_name, flag=u"资源类型")
    return app_name
