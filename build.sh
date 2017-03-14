#!/bin/bash

NAME=reg.weizom.com/weizoom/gaia:latest
VERSION=$(date +%Y%m%d%H%M)
TIMESTAMP_TAG=reg.weizom.com/weizoom/gaia:$VERSION

docker images --format="{{.Repository}}:{{.Tag}}" | grep gaia | xargs docker rmi
docker build --no-cache --rm -t ${NAME} -t ${TIMESTAMP_TAG} .

docker push ${NAME} 
docker push ${TIMESTAMP_TAG}
