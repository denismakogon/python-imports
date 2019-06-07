#!/usr/bin/env bash

set -xe

docker run --rm -ti \
    --cpu-quota=10000 \
    --cpu-period=100000 \
    --cpu-shares=128 \
    --memory=128m \
    --kernel-memory=128m \
    --memory-swap=128m \
    -v $PWD:/code \
    -e PYTHONPROFILEIMPORTTIME=1 \
    --entrypoint /bin/bash \
    python:3.7-slim-stretch
