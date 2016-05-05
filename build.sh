#!/bin/bash

set -ex

BRANCH=${BUILDKITE_COMMIT:-"develop"}

TAG=${BRANCH:0:7}

docker build -t edyn/route53-update .
docker tag edyn/route53-update edyn/route53-update:"$TAG"

docker push edyn/route53-update:"$TAG"
