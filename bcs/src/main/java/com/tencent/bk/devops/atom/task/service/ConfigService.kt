package com.tencent.bk.devops.atom.task.service

import com.tencent.bk.devops.atom.task.BcsContainerAtom
import com.tencent.bk.devops.atom.task.constant.BCS_HOST
import com.tencent.bk.devops.atom.task.constant.PROJECT_URL
import com.tencent.bk.devops.atom.task.pojo.BcsContainerParam
import java.lang.RuntimeException

class ConfigService {

	private var bcsHost : String = ""
	private var projectHost : String = ""

	fun checkConfigValue(param: BcsContainerParam) : Boolean {
		if(getConfigValue(PROJECT_URL, param).isNullOrEmpty()) {
			throw RuntimeException("私有配置${PROJECT_URL}为空")
		}
		projectHost = getConfigValue(PROJECT_URL, param)!!

		if(getConfigValue(BCS_HOST,param).isNullOrEmpty()) {
			throw RuntimeException("私有配置${BCS_HOST}为空")
		}
		bcsHost = getConfigValue(BCS_HOST, param)!!

		return true
	}

	private fun getConfigValue(key: String, param: BcsContainerParam): String? {
		val configMap = param.bkSensitiveConfInfo
		if(configMap == null){
			BcsContainerAtom.logger.warn("插件私有配置为空，请补充配置")
		}
		if(configMap.containsKey(key)){
			return configMap[key]
		}
		return null
	}

	fun getBcsHost(): String {
		return bcsHost
	}

}