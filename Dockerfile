FROM reg.weizom.com/wzbase/django16:1.0
MAINTAINER victor "gaoliqi@weizoom.com"

RUN pip install -U \
   git+https://git2.weizzz.com:84/microservice/eaglet.git \
   git+https://git2.weizzz.com:84/microservice/mns_python_sdk.git \
   && rm -rf ~/.pip ~/.cache

RUN mkdir -p /service
ADD . /service
WORKDIR /service
#VOLUME ["/service"]

ENTRYPOINT ["/usr/local/bin/dumb-init", "/bin/bash", "/service/start_service.sh"]
