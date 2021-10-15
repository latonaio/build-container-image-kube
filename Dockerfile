# FROM gcr.io/kaniko-project/executor:v0.12.0 AS kaniko
FROM thedoh/arm64-kaniko-executor:v0.19.0 as kaniko

FROM l4t:latest

ENV DOCKER_CONFIG /kaniko/.docker

RUN mkdir /kaniko
COPY --from=kaniko /kaniko /kaniko

# Definition of a Device & Service
ENV POSITION=Runtime \
    SERVICE=build-container-image \
    AION_HOME=/var/lib/aion

RUN mkdir ${AION_HOME}
WORKDIR ${AION_HOME}
# Setup Directoties
RUN mkdir -p \
    $POSITION/$SERVICE
WORKDIR ${AION_HOME}/$POSITION/$SERVICE/
ADD . .
RUN mv ./config.json /kaniko/.docker/
# RUN pip3 install setuptools --upgrade
RUN python3 setup.py install
CMD ["python3", "-m", "build_image"]
# CMD ["/bin/sh", "-c", "while :; do sleep 10; done"]
