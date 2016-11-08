#!/bin/bash

# function printUsage() {
# 	echo "Usage: bash build_image.sh [option] ..."
# 	echo "Available options:"
# 	echo "  --test: build image for test"
# 	echo "  --deploy: build image for deploy"
# 	echo "  --push: push image to image repository"
# }

# function parseArgs() {
# 	for arg in $*; do
# 		if [ "$arg" == "--test" ]; then
# 			IS_BUILD_TEST_IMAGE=true
# 		elif [ "$arg" == "--deploy" ]; then
# 			IS_BUILD_DEPLOY_IMAGE=true
# 		elif [ "$arg" == "--push" ]; then
# 			SHOULD_PUSH_IMAGE=true
# 		else
# 			echo "[ERROR]: unknown arg: $arg"
# 			echo ""
# 			printUsage
# 			exit 1
# 		fi
# 	done

# 	if ${IS_BUILD_DEPLOY_IMAGE} && ${IS_BUILD_TEST_IMAGE}; then
# 		echo "[ERROR]: you can not build 'test image' and 'deploy image' at the same time !"
# 		exit 1
# 	fi

# 	if ! ${IS_BUILD_TEST_IMAGE} && ! ${IS_BUILD_DEPLOY_IMAGE}; then
# 		echo "[ERROR]: you must specify a build target using '--test' or '--deploy'"
# 		exit 1
# 	fi

# }

# if [ $# == 0 ]; then
# 	printUsage
# 	exit 1
# fi

# # check arguments
# IS_BUILD_TEST_IMAGE=false
# IS_BUILD_DEPLOY_IMAGE=false
# SHOULD_PUSH_IMAGE=false

# parseArgs $*

python <<END
import servicecli
args = '$*'.split(' ')
if (len(args) == 1) and (len(args[0]) == 0):
	args = ['build_image.sh']
else:
	args.insert(0, 'build_image.sh')
servicecli.build_image(*args)
END

# build image
#cd docker
#ls .. | grep -v "docker" | xargs -n1 -i cp -rf ../{} .

#if ${IS_BUILD_TEST_IMAGE}; then
#elif ${}
#fi

#cd docker
#ls .. | grep -v "docker" | xargs -n1 -i cp -rf ../{} .
#NAME=test_gaia:1.0
#docker build --rm -t $NAME .
#cd ..