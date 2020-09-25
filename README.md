# BCS 插件

通过插件完成应用的生命周期管理。

## MESOS

集群为Mesos类型的应用管理。

支持功能:
- create: 部署实例
- recreate
- scale
- rollingupdate
- delete
- signal
- command

## 安装插件

1. 下载源码

2. 打包文件

```
# 假设下载后的目录为 a

cd a/bcs

# 生成包: bcs-1.0.0.tar.gz
python setup.py sdist
```

3. 创建一个目录，包含bcs-1.0.0.tar.gz和task.json，然后打包生成.zip的文件

4. 打开`蓝盾`APP，选择`研发商店`，点击`工作台`，点击`新增插件`，输入相应的信息

5. 回到插件列表页，选择`上架`，然后上传前面步骤生成的zip包，进行插件的安装

6. 点击插件名称，选择 `设置` -> `私有设置`, 新增如下配置:
   - APIGW_HOST: APIGW对应的host
   - APP_CODE: 插件访问apigw时的应用编码
   - APP_SECRET: 插件访问apigw时的应用TOKEN
   - IAM_HOST: IAM对应的HOST


## 注意
1. 申请网关: bcs-api, paas-cd, bcs-cc的资源的权限
2. 权限中心升级后，需要在bcs saas对应的db: `bk_bcs_app`, table: `projects_functioncontroller`中添加func_code: `APP_CODE_SKIP_AUTH`, wlist: app_code，这里app_code为上面在`私有设置`中添加的APP_CODE
