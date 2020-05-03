package com.tencent.bk.devops.atom.task.pojo

import com.tencent.bk.devops.atom.pojo.AtomBaseParam

class BcsContainerParam : AtomBaseParam() {
	val ccAppId: String = ""
	val projectId: String = ""
	/* 操作类型(包括：create,recreate,scale,rollingupdate,delete), required = true) */
	val opType: String = ""
	// 其他操作参数
	/* 对象类型(DaemonSet/Job/Deployment/StatefulSet), required = true) */
	val category: String? = ""
	/* 页面accessToken, required = false) */
	val accessToken: String? = ""
	/* 超时时间(minutes),默认8分钟, required = false) */
	val timeout: Int = 8

	// 创建类参数
	/* 集群ID, required = false) */
	val clusterId: String? = ""

	/* 模板名称, required = false) */
	val templateName: String? = ""
	/* 模板集版本名称, required = false) */
	val versionName: String? = ""
	/* 展示版本名称", required = false*/
	val showVersionName: String?= ""

	/* 模板集", required = false*/
	val musterId: String? = ""

	/* 命名空间变量, required = false) */
	val namespaceVar: List<BcsNamespaceVar>? = emptyList()

	// 滚动发布类参数
	/* 应用程序名称, required = false) */
	val bcsAppInstName: String? = ""
	/* 应用实例名称, required = false) */
	val bcsInstName: String? = ""
	/* 命名空间, required = false) */
	val namespace: String? = ""
	/* 应用实例个数, required = false) */
	val bcsInstNum: String? = "1"
	/* 应用实例版本名称, required = false) */
	val instVersionName: String? = ""
//
//	// 命令参数
//	@ApiModelProperty("环境变量", required = false)
//	val env: List<KeyValue>?,
//	@ApiModelProperty("命令， 例如 ps", required = false)
//	val command: String?,
//	@ApiModelProperty("命令参数， 例如 -a", required = false)
//	val commandParam: String?,
//	@ApiModelProperty("用户，默认为root", required = false)
//	val username: String?,
//	@ApiModelProperty("工作目录", required = false)
//	val workDir: String?,
//	@ApiModelProperty("特权，默认是false", required = false)
//	val privileged: Boolean = false,
//	@ApiModelProperty("任务信息保存时间, 默认为 24607 m", required = false)
//	val reserveTime: String?,
//
	// 公共参数
	/* 命名空间以及变量, required = false) */
	val instVar: List<KeyValue>? = null
}