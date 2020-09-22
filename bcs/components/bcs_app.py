# -*- coding: utf-8 -*-

from bcs.python_atom_sdk import *
sdk = AtomSDK()

from .base import http_request
from .auth import get_access_token

APIGW_HOST = sdk.get_sensitive_conf("APIGW_HOST")


def get_cc_app_id(project_id):
    """通过project_id获取关联的cmdb id
    """
    url = "{}/api/apigw/bcs-cc/prod/projects/{}/".format(APIGW_HOST, project_id)
    resp = bcs_app_request("GET", url)
    cc_app_id = resp.get("data", {}).get("cc_app_id")
    if not cc_app_id:
        sdk.log.error(u"查询绑定的cmdb id为空")
        exit(-1)
    return cc_app_id


def get_cluster_list(project_id):
    url = "{}/api/apigw/bcs-cc/prod/projects/{}/clusters/".format(APIGW_HOST, project_id)
    params = {"desire_all_data": 1}
    resp = bcs_app_request("GET", url, params=params)
    data = resp.get("data") or {}
    cluster_list = data.get("results") or []
    if not cluster_list:
        sdk.log.error(u"查询项目下的集群信息为空")
        exit(-1)
    return cluster_list


def get_template_sets(cc_app_id, project_id):
    url = "{}/api/apigw/paas-cd/prod/apps/cc_app_ids/{}/projects/{}/musters/".format(
        APIGW_HOST, cc_app_id, project_id
    )
    return bcs_app_request("GET", url).get("data") or {}


def get_template_set_versions(cc_app_id, project_id, tmpl_set_id):
    url = "{}/api/apigw/paas-cd/prod/apps/cc_app_ids/{}/projects/{}/musters/{}/versions/".format(
        APIGW_HOST, cc_app_id, project_id, tmpl_set_id
    )
    return bcs_app_request("GET", url).get("data") or {}


def get_version_detail(cc_app_id, project_id, version_id):
    url = "{}/api/apigw/paas-cd/prod/apps/cc_app_ids/{}/projects/{}/versions/{}/templates/".format(
        APIGW_HOST, cc_app_id, project_id, version_id
    )
    return bcs_app_request("GET", url).get("data") or {}


def create_app(cc_app_id, project_id, data):
    url = "{}/api/apigw/paas-cd/prod/apps/cc_app_ids/{}/projects/{}/instances/".format(
        APIGW_HOST, cc_app_id, project_id
    )
    return bcs_app_request("POST", url, data=data).get("data") or {}


def get_instances(cc_app_id, project_id, resource_kind, ns_name=None):
    url = "{}/api/apigw/paas-cd/prod/apps/cc_app_ids/{}/projects/{}/instances/".format(
        APIGW_HOST, cc_app_id, project_id
    )
    params = {
        "category": resource_kind
    }
    if ns_name:
        params["namespace"] = ns_name
    return bcs_app_request("GET", url, params=params).get("data") or {}


def get_versions_by_resource(cc_app_id, project_id, instance_id):
    url = "{}/api/apigw/paas-cd/prod/apps/cc_app_ids/{}/projects/{}/instances/{}/versions/".format(
        APIGW_HOST, cc_app_id, project_id, instance_id
    )
    return bcs_app_request("GET", url).get("data") or []


def rollingupdate_app(cc_app_id, project_id, params, data):
    url = "{}/api/apigw/paas-cd/prod/apps/cc_app_ids/{}/projects/{}/instances/batch_update/".format(
            APIGW_HOST, cc_app_id, project_id
    )
    return bcs_app_request("PUT", url, params=params, data=data)


def rollingupdate_app_new(cc_app_id, project_id, instance_id, params, data):
    url = "{}/api/apigw/paas-cd/prod/apps/cc_app_ids/{}/projects/{}/instances/{}/update//".format(
            APIGW_HOST, cc_app_id, project_id, instance_id
    )
    return bcs_app_request("PUT", url, params=params, data=data)


def get_app_status(cc_app_id, project_id, instance_id):
    url = "{}/api/apigw/paas-cd/prod/apps/cc_app_ids/{}/projects/{}/instances/{}/status/".format(
        APIGW_HOST, cc_app_id, project_id, instance_id
    )
    return bcs_app_request("GET", url)


def send_command(cc_app_id, project_id, instance_id, data):
    url = "{}/api/apigw/paas-cd/prod/apps/cc_app_ids/{}/projects/{}/instances/{}/command/".format(
        APIGW_HOST, cc_app_id, project_id, instance_id
    )
    data = bcs_app_request("POST", url, data=data, add_access_token_for_data=True).get("data") or {}
    if not data.get("task_id"):
        sdk.log.error(u"获取任务ID异常，taskid: %s", data.get("task_id"))
        exit(-1)
    return data["task_id"]


def get_task_status(cc_app_id, project_id, instance_id, task_id):
    url = "{}/api/apigw/paas-cd/prod/apps/cc_app_ids/{}/projects/{}/instances/{}/command/status/".format(
        APIGW_HOST, cc_app_id, project_id, instance_id
    )
    params = {"task_id": task_id}
    return bcs_app_request("GET", url, params=params).get("data") or {}


def recreate_app(cc_app_id, project_id, data):
    url = "{}/api/apigw/paas-cd/prod/apps/cc_app_ids/{}/projects/{}/instances/batch_recreate/".format(
        APIGW_HOST, cc_app_id, project_id
    )
    return bcs_app_request("POST", url, data=data)


def scale_app(cc_app_id, project_id, params, data):
    url = "{}/api/apigw/paas-cd/prod/apps/cc_app_ids/{}/projects/{}/instances/batch_scale/".format(
        APIGW_HOST, cc_app_id, project_id
    )
    return bcs_app_request("PUT", url, params=params, data=data)


def signal_for_application(cc_app_id, project_id, data):
    url = "{}/api/apigw/paas-cd/prod/apps/cc_app_ids/{}/projects/{}/applications/batch_signal/".format(
        APIGW_HOST, cc_app_id, project_id
    )
    return bcs_app_request("POST", url, data=data)


def signal_for_deployment(cc_app_id, project_id, data):
    url = "{}/api/apigw/paas-cd/prod/apps/cc_app_ids/{}/projects/{}/deployments/batch_signal/".format(
        APIGW_HOST, cc_app_id, project_id
    )
    return bcs_app_request("POST", url, data=data)


def delete_app(cc_app_id, project_id, data):
    url = "{}/api/apigw/paas-cd/prod/apps/cc_app_ids/{}/projects/{}/instances/batch_delete/".format(
        APIGW_HOST, cc_app_id, project_id
    )
    return bcs_app_request("DELETE", url, data=data)


def bcs_app_request(method, url, params=None, data=None, add_access_token_for_data=False):
    access_token = get_access_token()
    if params:
        params.update({"access_token": access_token})
    else:
        params = {"access_token": access_token}

    if add_access_token_for_data:
        data.update({"access_token": access_token})

    return http_request(method, url, params=params, data=data, headers={"Content-Type": "application/json"})
