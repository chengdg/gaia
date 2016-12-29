FROM reg.weizom.com/wzbase/python27:1.0
MAINTAINER gaia-team

EXPOSE 8003
ADD ./dist /service
WORKDIR /service

RUN pip install -U \
    git+https://git2.weizzz.com:84/microservice/dingtalk-sso.git \
    git+https://git2.weizzz.com:84/microservice/mns_python_sdk.git \
    git+https://git2.weizzz.com:84/microservice/wcas-sso.git \
    git+https://git2.weizzz.com:84/microservice/servicecli.git \
  && rm -rf ~/.pip ~/.cache

ENTRYPOINT ["/usr/local/bin/dumb-init", "/bin/bash", "start_service.sh"]
