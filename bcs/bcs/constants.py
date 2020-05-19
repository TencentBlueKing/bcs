# -*- coding: utf-8 -*-

MESOS_DEPLOYMENT_RESOURCE = "Deployment"
MESOS_APPLICATION_RESOURCE = "Application"

POLLING_TIMEOUT = 3600
POLLING_COMMAND_TIMEOUT = 1800
# 时间间隔，默认为10s
INTERVAL = 5
# 轮训等待时间， 默认为10s
WAIT_POLLING_TIME = 10

# 应用正常状态
NORMAL_STATUS = "running"
ABNORMAL_STATUS = "unnormal"

# 任务正常状态
TASK_NORMAL_STATUS = ("finish", 0)
TASK_FAILED_STATUS = "failed"
TASK_FINISH_STATUS = "finish"


# 资源类型转换
MESOS_RESOURCE_KIND_MAP = {
    "Deployment": "deployment",
    "Application": "application"
}

# 删除应用操作类型，便于标识应用已经被删除
DELETE_OPER = "delete"
