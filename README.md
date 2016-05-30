**python-service-base —— python service的codebase**

# 如何使用

安装peewee：
```
pip install -U "peewee==2.6.4"
```

安装插件：
```
pip install git+https://git2.weizzz.com:84/microservice/eaglet.git
```

生成API文档：
```
swagger-codegen generate -i openapi.json -l html -o html
```
