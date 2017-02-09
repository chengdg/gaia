**python-service-base —— python service的codebase**

# 如何使用

安装peewee：
```
pip install -U "peewee==2.6.4"
```

安装Python包：
```
pip install \
  six \
  falcon
```

安装插件：
```
pip install -U git+https://git2.weizzz.com:84/microservice/eaglet.git
```

生成API文档：
```
npm install -g bootprint
npm install -g bootprint-swagger
node ./swagger
bootprint swagger swagger/openapi.json html
```
然后打开 html/index.html 即可看到API文档。

## 如何集成到Ningx？ ##
1. 在hosts文件中添加如下域名
```
127.0.0.1 api.zeus.com
127.0.0.1 db.zeus.com
```
2. 编辑Nginx的`nginx.conf`文件，添加如下配置

```
server {
    listen       80;
    server_name  api.zeus.com;

    #charset koi8-r;

    #access_log  logs/api_weapp.access.log  main;
    location /static {
        root D:/weapp/workspace/zeus/; #换成自己的目录
    }
    
    location / {
        proxy_pass http://127.0.0.1:8002;
    }
    
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   html;
    }
}
```

## 基本规范
- get请求中bool值统一使用字符串"true","false"。
- 发送复杂的数据，使用必须先json序列化
- 显式声明参数
  - api层返回结果
  - api层调用静态方法时的字典
  
MNS消息使用指南:https://git2.weizzz.com:84/weizoom/new_zeus/wikis/mns-guide

## 数据初始化

1. 在weapp执行rebuild重建数据库
2. 在gaia执行`behave -kt @full_init` 或者`behave -kt @full_init_jobs_self`(如果需要使用jobs账号作为自营)

## BDD
1. 在weapp执行rebuild重建数据库
2. 启动bdd_server，即`sh start_bdd_server.sh`：
    - weapp bdd_server
    - apiserver bdd_server
    - weizoom_card bdd_server
3. 启动项目，即`sh start_service.sh`
    - card_apiserver
    - gaia