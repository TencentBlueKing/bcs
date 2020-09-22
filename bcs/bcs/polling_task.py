# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta

from .python_atom_sdk import *

from bcs.constants import POLLING_TIMEOUT, NORMAL_STATUS, INTERVAL, ABNORMAL_STATUS
from components import bcs_app
from bcs import constants

sdk = AtomSDK()


def polling(cc_app_id, project_id, instance_id, op_type=None):
    end_time = datetime.now() + timedelta(seconds=constants.POLLING_TIMEOUT)
    while(True):
        if datetime.now() > end_time:
            sdk.log.error(u"轮训应用状态超时")
            exit(-1)
        try:
            resp = bcs_app.get_app_status(cc_app_id, project_id, instance_id)
        except Exception:
            time.sleep(INTERVAL)
            continue
        app_status = resp.get("data") or {}
        if not app_status and op_type == constants.DELETE_OPER:
            sdk.log.info(u"删除成功!")
            exit(0)
        if app_status.get("status") == NORMAL_STATUS:
            sdk.log.info(u"任务执行成功！")
            exit(0)
        if app_status.get("status") == ABNORMAL_STATUS:
            sdk.log.error(u"执行失败，错误：%s", resp.get("message"))
            exit(-1)
        # 设置间隔，默认为5s
        time.sleep(INTERVAL)


def command_polling(cc_app_id, project_id, instance_id, task_id):
    """轮训command任务执行状态
    """
    end_time = datetime.now() + timedelta(seconds=constants.POLLING_COMMAND_TIMEOUT)
    while(True):
        if datetime.now() > end_time:
            sdk.log.error(u"轮训任务状态超时")
            break
        try:
            data = bcs_app.get_task_status(cc_app_id, project_id, instance_id, task_id)
        except Exception:
            time.sleep(INTERVAL)
            continue
        # 解析任务状态
        status_data = data.get("status") or {}
        taskgroups = status_data.get("taskgroups") or []
        # 记录状态，当为稳定状态时，认为任务结束
        status_list = []
        for tg in taskgroups:
            tasks = tg.get("tasks") or []
            for t in tasks:
                if t.get("status") == constants.TASK_FAILED_STATUS:
                    sdk.log.error(u"命令执行失败，%s", t.get("message"))
                    exit(-1)
                if t.get("status") == constants.TASK_FINISH_STATUS:
                    inspect = t.get("commInspect") or {}
                    if inspect.get("exitCode") != 0:
                        sdk.log.error(u"命令执行失败，%s", inspect.get("stderr"))
                        exit(-1)
                status_list.append((t.get("status"), inspect.get("exitCode")))
        # NOTE: 需要taskgroup状态为finish并且exitCode为0，才认为任务执行成功
        status_set = set(status_list)
        # 如果状态记录中只有一个finish状态, 并且是正常退出，则认为命令执行成功
        if len(status_set) == 1 and list(status_set)[0] == constants.TASK_NORMAL_STATUS:
            sdk.log.info(u"命令执行成功！")
            break


        # 设置间隔，默认为10s
        time.sleep(INTERVAL)

    exit(0)
