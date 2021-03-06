#!/bin/sh

DATE="$(date "+%Y%m%d%H%M")"
SERVICE_NAME="build-container-image"
docker build -t ${SERVICE_NAME}:${DATE} .
docker tag ${SERVICE_NAME}:${DATE} ${SERVICE_NAME}:latest
