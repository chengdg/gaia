#!/bin/bash
cd docker
ls .. | grep -v "docker" | xargs -n1 -i cp -rf ../{} .
NAME=test_gaia:1.0
docker build --rm -t $NAME .
cd ..