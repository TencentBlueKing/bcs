package com.tencent.bk.devops.atom.task

import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import com.fasterxml.jackson.module.kotlin.readValue
import com.tencent.bk.devops.atom.AtomContext
import com.tencent.bk.devops.atom.common.Status
import com.tencent.bk.devops.atom.spi.AtomService
import com.tencent.bk.devops.atom.spi.TaskAtom
import com.tencent.bk.devops.atom.task.pojo.BcsContainerParam
import com.tencent.bk.devops.atom.task.pojo.enum.BcsCategory
import com.tencent.bk.devops.atom.task.pojo.enum.BcsOperation
import com.tencent.bk.devops.atom.task.service.BcsService
import com.tencent.bk.devops.atom.task.service.ConfigService
import com.tencent.bk.devops.plugin.utils.OkhttpUtils
import okhttp3.Request
import org.slf4j.LoggerFactory
import java.lang.Exception
import java.lang.RuntimeException

@AtomService(paramClass = BcsContainerParam::class)
class BcsContainerAtom : TaskAtom<BcsContainerParam> {

	override fun execute(atomContext: AtomContext<BcsContainerParam>) {
		val param = atomContext.param
		val atomResult = atomContext.result
		if (!checkParam(param)) {
			atomResult.status = Status.error
			return
		}
		configService.checkConfigValue(param)

		val projectId = param.projectId
		val opType = BcsCategory.parse(param.opType)
		val bcsOperation = BcsOperation.parse(param.category)
		try {
			if (bcsOperation == BcsOperation.CREATE) {
				bcsService.createInstance(opType!!, projectId, param)
			} else {
				doBcsOperation(param, bcsOperation!!, projectId)
			}
		} catch (ex: Exception) {
			logger.error("atom execute fail, failMsg:${ex.message}")
			atomResult.status = Status.error
		}
	}

	private fun doBcsOperation(param: BcsContainerParam, opType: BcsCategory, projectId: String) {
		// 公共的参数校验
		if (param.bcsAppInstName.isNullOrBlank()) {
			logger.error("bcsAppInstName is not init")
			throw RuntimeException("bcsAppInstName is not init")
		}
		if (param.namespace.isNullOrBlank()) {
			logger.error("namespace is not init")
			throw RuntimeException("namespace is not init")
		}
		val accessToken = param.accessToken!!
		val appIdStr = param.ccAppId
		val category = BcsCategory.parse(param.category)
		val namespace = param.namespace
		val bcsAppInstName = param.bcsAppInstName
		val bcsAppInstId = getBcsAppInstIdByName(accessToken = accessToken, appidStr = appIdStr, projectId = projectId, category = category!!, bcsAppInstName = bcsAppInstName, namespace = namespace)
		val timeout = param.timeout
		val instVarList = param.instVar ?: listOf()

		val varMap = mutableMapOf<String, String>()
		instVarList.forEach {
			varMap[it.key] = it.value
		}
		val instVar = mutableMapOf<String, Map<String, String>>()
		instVar[bcsAppInstId] = varMap


		lateinit var result: Pair<Int, String>
		when (opType) {
			BcsOperation.RECREATE -> {
				logger.info("BCS opType is reCreate, instanceId : $bcsAppInstId")
				result = bcsService.reCreateInstance(accessToken = accessToken, category = category, appidStr = appIdStr, projectId = projectId, instIdList = bcsAppInstId)
			}
			BcsOperation.SCALE -> {
				if (param.bcsInstNum.isNullOrBlank()) {
					logger.error("bcsInstNum is not init")
					throw RuntimeException("bcsInstNum is not init")
				}
				val instNum = param.bcsInstNum?.toInt() ?: 0
				logger.info("BCS opType is scale, instanceId : $bcsAppInstId and instanceNum: $instNum")
				result = bcsService.scaleInstance(accessToken = accessToken, category = category, appidStr = appIdStr, projectId = projectId, instIdList = bcsAppInstId, instNum = instNum)
			}
			BcsOperation.ROLLINGUPDATE -> {
				if (param.instVersionName.isNullOrBlank()) {
					logger.error("instVersionName is not init")
					throw RuntimeException("instVersionName is not init")
				}
				val instVersionName = param.instVersionName
				val versionId = bcsService.getInstVersionIdByName(
						accessToken = accessToken,
						appIdStr = appIdStr,
						projectId = projectId,
						instId = bcsAppInstId,
						instVersionName = instVersionName
				)
				result = if (param.bcsInstNum.isNullOrBlank()) {
					logger.error("bcsInstNum is not init")
					throw RuntimeException("bcsInstNum is not init")
				} else {
					val instNum = param.bcsInstNum?.toInt() ?: 0
					logger.info("BCS opType is batch update, instanceId : $bcsAppInstId")
					bcsService.updateInstance(accessToken = accessToken, category = category!!, appidStr = appIdStr, projectId = projectId, versionId = versionId, instNum = instNum, instIdList = bcsAppInstId, instVar = instVar)
				}
			}
			BcsOperation.DELETE -> {
				logger.error("BCS opType is delete")
				result = bcsService.deleteInstance(
						accessToken = accessToken,
						category = category,
						appidStr = appIdStr,
						projectId = projectId,
						instIdList = bcsAppInstId
				)
			}
		}

		if (result.first != 0) {
			logger.error("BCS operate failed msg: ${result.second}")
			throw RuntimeException("BCS operation failed")
		}

		Thread.sleep(5 * 1000)

		if (opType != BcsOperation.DELETE) {
			val appResult = waitForRunning(accessToken, appIdStr, projectId, bcsAppInstId, timeout.toLong())
			if (!appResult.first) {
				logger.info("BCS operation failed:${appResult.second}")
				throw RuntimeException("BCS operation failed")
			}
		}
		logger.info("BCS operation success!")
	}

	private fun getBcsAppInstIdByName(
			accessToken: String,
			appidStr: String,
			projectId: String,
			category: BcsCategory,
			bcsAppInstName: String,
			namespace: String
	): String {
		val url =
				configService.getBcsHost() + "cc_app_ids/$appidStr/projects/$projectId/instance/detail/?access_token=$accessToken&category=${category.getValue()}&name=$bcsAppInstName&namespace=$namespace"
		logger.info("Get bcsAppInstId, request url: $url")

		val request = Request.Builder()
				.url(url)
				.get()
				.build()

		lateinit var dataMap: Map<String, Any>
		OkhttpUtils.doHttp(request).use { response ->
			val data = response.body()!!.string()
			logger.info("Get bcsAppInstId by bcsAppInstName, response: $data")
			if (!response.isSuccessful) {
				logger.error("Get bcsAppInstId by bcsAppInstName($bcsAppInstName) failed, msg:$data")
				throw RuntimeException("Get bcsAppInstId faild, response: $data")
			}

			val responseData: Map<String, Any> = jacksonObjectMapper().readValue(data)
			val code = responseData["code"] as Int
			if (0 != code) {
				val message = responseData["message"].toString()
				logger.error("Get bcsAppInstId by bcsAppInstName($bcsAppInstName) failed, msg:$message")
				throw RuntimeException("Get bcsAppInstId faild, response: $data")
			}
			dataMap = responseData["data"] as Map<String, Any>
			if (dataMap["id"] == null || dataMap["id"] == "") {
				logger.error("Get bcsAppInstId by bcsAppInstName($bcsAppInstName) failed, msg:$data")
				throw RuntimeException("Get bcsAppInstId by bcsAppInstName($bcsAppInstName) failed, response:$data")
			}
		}
		return dataMap["id"].toString()
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

			val (isFinish, success, msg) = bcsService.getInstanceStatus(
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

	private fun checkParam(bcsContainerParam: BcsContainerParam): Boolean {
		if (bcsContainerParam.opType.isBlank()) {
			logger.error("opType is not init")
			return false
		}
		if (bcsContainerParam.category.isNullOrBlank()) {
			logger.error("category is not init")
			return false
		}
		if (bcsContainerParam.accessToken.isNullOrBlank()) {
			logger.error("accessToken is not init")
			return false
		}
		return true
	}

	companion object {
		val logger = LoggerFactory.getLogger(BcsContainerAtom::class.java)
		val bcsService = BcsService()
		val configService = ConfigService()
	}
}