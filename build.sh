#!/bin/bash

set -ex

BRANCH=${BUILDKITE_COMMIT:-"develop"}

TAG=${BRANCH:0:7}

docker build -t edyn/logstash .
docker tag edyn/logstash edyn/docker-logstash:"$TAG"

docker push edyn/docker-logstash:"$TAG"
