#
# Copyright Pravega Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#
# Note: This file contains source code copied from the Apache BookKeeper
#       project (http://bookkeeper.apache.org). Specifically, it contains
#       source code copied from file `Dockerfile`, revisions `a14c8bf` and
#       `a00f60d`:
# - github.com/apache/bookkeeper/blob/branch-4.7/docker/Dockerfile
# - github.com/apache/bookkeeper/blob/branch-4.9/docker/Dockerfile
#
ARG BASE_IMAGE=registry.scontain.com:5050/ardhipoetra/cloudskin-images/java:ubuntu20.04-scone5.10.0-rc.1

FROM ${BASE_IMAGE}

ARG BK_VERSION=4.14.1
ARG DISTRO_NAME=bookkeeper-all-${BK_VERSION}-bin


RUN set -x \
    && apt update && apt install -y iproute2 wget gpg python2 \
    && ln -s  /usr/bin/python2 /usr/bin/python \
    && cd /opt \
    && wget -q "https://archive.apache.org/dist/bookkeeper/bookkeeper-${BK_VERSION}/${DISTRO_NAME}.tar.gz" \
    && wget -q "https://archive.apache.org/dist/bookkeeper/bookkeeper-${BK_VERSION}/${DISTRO_NAME}.tar.gz.asc" \
    && wget -q "https://archive.apache.org/dist/bookkeeper/bookkeeper-${BK_VERSION}/${DISTRO_NAME}.tar.gz.sha512" \
    && sha512sum -c ${DISTRO_NAME}.tar.gz.sha512 \
    && wget https://dist.apache.org/repos/dist/release/bookkeeper/KEYS \
    && gpg --import KEYS \
    && gpg --batch --verify "$DISTRO_NAME.tar.gz.asc" "$DISTRO_NAME.tar.gz" \
    && tar -xzf "$DISTRO_NAME.tar.gz" \
    && mkdir -p /opt/bookkeeper \
    && cp -r bookkeeper-all-${BK_VERSION}/* /opt/bookkeeper/ \
    && rm -rf "bookkeeper-all-${BK_VERSION}" "$DISTRO_NAME.tar.gz" "$DISTRO_NAME.tar.gz.asc" "$DISTRO_NAME.tar.gz.sha512"

# install zookeeper shell (this doesn't need to be sconified)
# bookkeeper script requires python2, but kazoo only support python2.7 until version 2.7.0
RUN wget -q https://bootstrap.pypa.io/pip/2.7/get-pip.py \
    && python --version \
    && python get-pip.py \
    && pip install kazoo==2.7.0 zk-shell \
    && rm -rf get-pip.py

WORKDIR /opt/bookkeeper

RUN wget "https://github.com/apache/bookkeeper/archive/refs/tags/release-${BK_VERSION}.tar.gz" \
    && tar xf release-${BK_VERSION}.tar.gz \
    && cp -r bookkeeper-release-${BK_VERSION}/docker/scripts/ /opt/bookkeeper/ \
    && chmod +x -R /opt/bookkeeper/scripts/ 

# bookkeeper requires procfs-mounts
# as per 02012025, we use scone 5.10, which has procfs support. These lines are not necessary anymore.
# only uncomment these lines if you don't have access to the base image.
#
# COPY --from=registry.scontain.com:5050/amiguel/neardatapublic/sconelibs:procfs /opt/scone/lib/libc.scone-x86_64.so.1  /opt/scone/lib/libc.scone-x86_64.so.1.procfs
# COPY --from=registry.scontain.com:5050/amiguel/neardatapublic/sconelibs:procfs /opt/scone/lib/ld-scone-x86_64.so.1    /opt/scone/lib/ld-scone-x86_64.so.1.procfs
# RUN mv -vf /opt/scone/lib/libc.scone-x86_64.so.1  /opt/scone/lib/libc.scone-x86_64.so.1.orig \
#     && mv -vf /opt/scone/lib/ld-scone-x86_64.so.1    /opt/scone/lib/ld-scone-x86_64.so.1.orig \
#     && cp -pvf /opt/scone/lib/libc.scone-x86_64.so.1.procfs /opt/scone/lib/libc.scone-x86_64.so.1 \
#     && cp -pvf /opt/scone/lib/ld-scone-x86_64.so.1.procfs   /opt/scone/lib/ld-scone-x86_64.so.1 \
#     && ln -svf /opt/scone/lib/libc.scone-x86_64.so.1.procfs  /lib/libc.scone-x86_64.so.1 \
#     && ln -svf /opt/scone/lib/ld-scone-x86_64.so.1.procfs    /lib/ld-scone-x86_64.so
# 


COPY entrypoint.sh /opt/bookkeeper/scripts/pravega_entrypoint.sh

# For backwards compatibility with older operator versions
COPY entrypoint.sh /opt/bookkeeper/entrypoint.sh

RUN chmod +x -R /opt/bookkeeper/scripts/

ENTRYPOINT [ "/bin/bash", "/opt/bookkeeper/scripts/pravega_entrypoint.sh" ]
CMD ["bookie"]

HEALTHCHECK --interval=10s --timeout=60s CMD /bin/bash /opt/bookkeeper/scripts/healthcheck.sh
