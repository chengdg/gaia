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

## 如何集成到Ningx？ ##
1. 在hosts文件中添加如下域名
```
127.0.0.1 api.zeus.com
```
```
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