FROM reg.weizom.com/wzbase/python27:1.0
MAINTAINER gaia-team

EXPOSE 8003
ADD . /service
WORKDIR /service

ENTRYPOINT ["/usr/local/bin/dumb-init", "/bin/bash", "start_service.sh"]
