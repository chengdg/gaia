FROM reg.weizzz.com:5000/wz/python27:1.0
MAINTAINER gaia-team

EXPOSE 8003
ADD . /service
WORKDIR /service
VOLUME ["/service"]

ENTRYPOINT ["/usr/local/bin/dumb-init", "/bin/bash", "start_service.sh"]