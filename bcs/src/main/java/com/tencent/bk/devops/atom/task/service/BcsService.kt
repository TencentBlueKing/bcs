package com.tencent.bk.devops.atom.task.service

import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import com.fasterxml.jackson.module.kotlin.readValue
import com.tencent.bk.devops.atom.task.BcsContainerAtom
import com.tencent.bk.devops.atom.task.pojo.BcsContainerParam
import com.tencent.bk.devops.atom.task.pojo.TaskResult
import com.tencent.bk.devops.atom.task.pojo.enum.BcsCategory
import com.tencent.bk.devops.atom.task.utils.OkhttpUtils
import okhttp3.MediaType
import okhttp3.Request
import okhttp3.RequestBody
import org.slf4j.LoggerFactory

class BcsService {
	private val JSON = MediaType.parse("application/json;charset=utf-8")

	fun reCreateInstance(
			accessToken: String,
			category: BcsCategory,
			appidStr: String,
			projectId: String,
			instIdList: String
	): Pair<Int, String> {
		val url = configService.getBcsHost() + "cc_app_ids/$appidStr/projects/$projectId/instances/batch_recreate/?access_token=$accessToken&category=${category.getValue()}"
		logger.info("Recreate instance, request url: $url")
		val requestData = mapOf("inst_id_list" to listOf(instIdList))
		val requestBody = ObjectMapper().writeValueAsString(requestData)
		logger.info("Recreate instance, request body: $requestBody")
		val request = Request.Builder()
				.url(url)
				.post(RequestBody.create(JSON, requestBody))
				.build()
		OkhttpUtils.doHttp(request).use { response ->
			val data = response.body()!!.string()
			logger.info("Recreate instance, response: $data")
			if (!response.isSuccessful) {
				throw RuntimeException("Recreate instance, response: $data")
			}
			val responseData: Map<String, Any> = jacksonObjectMapper().readValue(data)
			val code = responseData["code"] as Int
			var message = ""
			if (responseData["message"] != null) message = responseData["message"].toString()
			return Pair(code, message)
		}
	}

	fun deleteInstance(
			accessToken: String,
			category: BcsCategory,
			appidStr: String,
			projectId: String,
			instIdList: String
	): Pair<Int, String> {
		val url =
				configService.getBcsHost() + "cc_app_ids/$appidStr/projects/$projectId/instances/batch_delete/?access_token=$accessToken&category=${category.getValue()}"
		logger.info("delete instance, request url: $url")
		val requestData = mapOf("inst_id_list" to listOf(instIdList))
		val requestBody = ObjectMapper().writeValueAsString(requestData)
		logger.info("delete instance, request body: $requestBody")
		val request = Request.Builder()
				.url(url)
				.delete(RequestBody.create(JSON, requestBody))
				.build()
		OkhttpUtils.doHttp(request).use { response ->
			val data = response.body()!!.string()
			logger.info("delete instance, response: $data")
			if (!response.isSuccessful) {
				throw java.lang.RuntimeException("delete instance, response: $data")
			}
			val responseData: Map<String, Any> = jacksonObjectMapper().readValue(data)
			val code = responseData["code"] as Int
			var message = ""
			if (responseData["message"] != null) message = responseData["message"].toString()
			return Pair(code, message)
		}
	}

	fun scaleInstance(
			accessToken: String,
			category: BcsCategory,
			appidStr: String,
			projectId: String,
			instIdList: String,
			instNum: Int
	): Pair<Int, String> {
		val url =
				configService.getBcsHost() + "cc_app_ids/$appidStr/projects/$projectId/instances/batch_scale/?access_token=$accessToken&category=${category.getValue()}&instance_num=$instNum"
		logger.info("Scale instance, request url: $url")

		val requestData = mapOf("inst_id_list" to listOf(instIdList))
		val requestBody = ObjectMapper().writeValueAsString(requestData)
		logger.info("Scale instance, request body: $requestBody")

		val request = Request.Builder()
				.url(url)
				.put(RequestBody.create(JSON, requestBody))
				.build()
		OkhttpUtils.doHttp(request).use { response ->
			val data = response.body()!!.string()
			logger.info("Scale instance, response: $data")
			if (!response.isSuccessful) {
				throw java.lang.RuntimeException(data)
			}
			val responseData: Map<String, Any> = jacksonObjectMapper().readValue(data)
			val code = responseData["code"] as Int
			var message = ""
			if (responseData["message"] != null) message = responseData["message"].toString()
			return Pair(code, message)
		}
	}

	fun updateInstance(
			accessToken: String,
			category: BcsCategory,
			appidStr: String,
			projectId: String,
			versionId: Int,
			instNum: Int,
			instIdList: String,
			instVar: Map<String, Map<String, String>>
	): Pair<Int, String> {
		val url =
				configService.getBcsHost() + "cc_app_ids/$appidStr/projects/$projectId/instances/batch_update/?access_token=$accessToken&category=${category.getValue()}&version_id=$versionId&instance_num=$instNum"
		logger.info("Update instance, request url: $url")
		val requestData = mapOf(
				"inst_id_list" to listOf(instIdList),
				"inst_variables" to instVar
		)
		val requestBody = ObjectMapper().writeValueAsString(requestData)
		logger.info("Update instance, request body: $requestBody")
		val request = Request.Builder()
				.url(url)
				.put(RequestBody.create(JSON, requestBody))
				.build()
		OkhttpUtils.doHttp(request).use { response ->
			val data = response.body()!!.string()
			logger.info("Update instance, response: $data")
			if (!response.isSuccessful) {
				throw RuntimeException("Update instance, response: $data")
			}
			val responseData: Map<String, Any> = jacksonObjectMapper().readValue(data)
			val code = responseData["code"] as Int
			var message = ""
			if (responseData["message"] != null) message = responseData["message"].toString()
			return Pair(code, message)
		}
	}


	fun getInstanceStatus(accessToken: String, appidStr: String, projectId: String, instanceId: String): TaskResult {
		val url =
				configService.getBcsHost() + "cc_app_ids/$appidStr/projects/$projectId/instances/$instanceId/status/?access_token=$accessToken"
		BcsContainerAtom.logger.info("Get instance status, request url: $url")
		val request = Request.Builder()
				.url(url)
				.get()
				.build()
		OkhttpUtils.doHttp(request).use { response ->
			val data = response.body()!!.string()
			BcsContainerAtom.logger.info("Get instance status, response: $data")
			if (!response.isSuccessful) {
				throw RuntimeException("Get instance status, response: $data")
			}

			val responseData: Map<String, Any> = jacksonObjectMapper().readValue(data)
			val code = responseData["code"] as Int
			if (0 != code) {
				val message = responseData["message"].toString()
				return TaskResult(true, false, message)
			}
			val statusMap = responseData["data"] as Map<String, Any>
			if (null == statusMap["status"]) {
				return TaskResult(false, false, "")
			}
			val status = statusMap["status"] as String
			return when {
				"running".equals(status, false) -> TaskResult(true, true, "running")
				"unnormal".equals(status, false) -> TaskResult(true, false, "unnormal")
				else -> TaskResult(false, false, "")
			}
		}
	}

	fun getInstVersionIdByName(
			accessToken: String,
			appIdStr: String,
			projectId: String,
			instId: String,
			instVersionName: String
	): Int {
		val url = configService.getBcsHost() + "cc_app_ids/$appIdStr/projects/$projectId/instances/$instId/versions/?access_token=$accessToken"
		logger.info("Get instVersionId, request url: $url")
		val request = Request.Builder()
				.url(url)
				.get()
				.build()
		OkhttpUtils.doHttp(request).use { response ->
			val data = response.body()!!.string()
			logger.info("Get instVersionId, response: $data")
			if (!response.isSuccessful) {
				throw RuntimeException("Get instVersionId, response: $data")
			}
			val responseData: Map<String, Any> = jacksonObjectMapper().readValue(data)
			val code = responseData["code"] as Int
			if (code != 0) {
				val message = responseData["code"] as String
				logger.error("Get instVersionId failed, message : $message")
				throw RuntimeException("Get instVersionId failed, response: $data")
			}

			val responseDataData: List<Map<String, Any>> = responseData["data"] as List<Map<String, Any>>
			val instVersionObjs = responseDataData.filter { (it["name"] as String).equals(instVersionName, true) }
			if (instVersionObjs.isEmpty()) {
				logger.error("Get instVersionId failed , instVersionName is mismatching. instVersionName : $instVersionName")
				throw RuntimeException("Get instVersionId failed , instVersionName is mismatching. instVersionName : $instVersionName")
			}
			val instVersionObj = instVersionObjs[0]
			return instVersionObj["id"] as Int
		}
	}


	fun createInstance(
			category: BcsCategory,
			projectId: String,
			param: BcsContainerParam
	) {

		val timeout = param.timeout
		if (param.namespaceVar == null) {
			BcsContainerAtom.logger.error("namespaceVar is not init ")
			throw java.lang.RuntimeException("namespaceVar is not init ")
		}
		val variableInfo = param.namespaceVar!!

		if (param.templateName.isNullOrBlank()) {
			BcsContainerAtom.logger.error("instanceEntity is not init ")
			throw java.lang.RuntimeException("instanceEntity is not init ")
		}

		val category = category
		val appIdStr = param.ccAppId
		val clusterId = param.clusterId
		val templateName = param.templateName
		val showVersionName = param.showVersionName
		val instanceEntityObj = mapOf(
				category to listOf(
						mapOf("name" to templateName)
				)
		)

		val token = param.accessToken!!
		val url = BcsContainerAtom.configService.getBcsHost() + "cc_app_ids/$appIdStr/projects/$projectId/instances/?access_token=$token"
		BcsContainerAtom.logger.info("Create instance, request url: $url")

		val clusterNsInfo = mutableMapOf<String, MutableMap<String, String>>()
		variableInfo.forEach { it ->
			val namespace = it.namespace
			val map: MutableMap<String, String> = clusterNsInfo.computeIfAbsent(namespace) { mutableMapOf() }
			val key = it.varKey
			val value = it.varValue
			map[key] = value
		}

		val requestData = mapOf(
				"cluster_ns_info" to mapOf(clusterId to clusterNsInfo),
				"show_version_name" to showVersionName,
				"instance_entity" to instanceEntityObj
		)

		val requestBody = ObjectMapper().writeValueAsString(requestData)
		BcsContainerAtom.logger.info("Create instance, request body: $requestBody")
		val request = Request.Builder()
				.url(url)
				.post(RequestBody.create(JSON, requestBody))
				.build()
		OkhttpUtils.doHttp(request).use { response ->
			val data = response.body()!!.string()
			BcsContainerAtom.logger.info("Create instance, response: $data")
			if (!response.isSuccessful) {
				BcsContainerAtom.logger.error("Create instance failed, msg: $data")
				throw java.lang.RuntimeException("Create instance failed, msg: $data")
			}
			val responseData: Map<String, Any> = jacksonObjectMapper().readValue(data)
			val code = responseData["code"] as Int
			if (code != 0) {
				val message = responseData["message"].toString()
				BcsContainerAtom.logger.error("Create instance failed, msg:$message")
				throw java.lang.RuntimeException("Create instance failed, msg: $data")
			}
			val instData = responseData["data"] as Map<String, Any>
			val instIdList = instData["inst_id_list"] as List<Int>

			Thread.sleep(5 * 1000)

			instIdList.forEach {
				val appResult = waitForRunning(
						accessToken = token,
						appidStr = appIdStr,
						projectId = projectId,
						instanceId = it.toString(),
						timeout = timeout.toLong()
				)
				if (!appResult.first) {
					BcsContainerAtom.logger.error("BCS operation failed:${appResult.second}")
					throw java.lang.RuntimeException("BCS operation failed:${appResult.second}")
				}
			}
			BcsContainerAtom.logger.info("BCS operation success!")
		}
	}

	private fun waitForRunning(
			accessToken: String,
			appidStr: String,
			projectId: String,
			instanceId: String,
			timeout: Long
	): Pair<Boolean, String> {
		logger.info("waiting for bcsApp running, timeout setting: ${timeout}min")
		val startTime = System.currentTimeMillis()
		loop@ while (true) {
			if (System.currentTimeMillis() - startTime > timeout * 60 * 1000) {
				logger.error("waiting for bcsApp running timeout")
				return Pair(false, "Waiting for bcs app running timeout")
			}

			val (isFinish, success, msg) = getInstanceStatus(
					accessToken = accessToken,
					appidStr = appidStr,
					projectId = projectId,
					instanceId = instanceId
			)
			return when {
				!isFinish -> {
					Thread.sleep(5 * 1000)
					continue@loop
				}
				!success -> {
					logger.error("Waiting for bcs app running failed, msg: $msg")
					Pair(false, "Waiting for bcs app running failed, msg: $msg")
				}
				else -> Pair(true, "Success!")
			}
		}
	}

	companion object {
		val logger = LoggerFactory.getLogger(BcsContainerAtom::class.java)
		val configService = ConfigService()
	}
}