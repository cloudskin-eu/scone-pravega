#!/bin/bash

BASE_IMAGE="registry.scontain.com:5050/ardhipoetra/cloudskin-images/java:ubuntu20.04-scone5.10.0-rc.1"

if ! docker inspect $BASE_IMAGE >/dev/null 2>&1; then
    echo "$BASE_IMAGE not found in local, try pulling from registry"
    if ! docker pull "$BASE_IMAGE" >/dev/null 2>&1; then
        echo "Cannot pull image from registry - bailed out"
        exit 1
    fi
fi

PRAVEGA_VERSION=0.13

echo "---- Pulling Pravega ----"
rm -rf pravega/ && git clone --single-branch -b r${PRAVEGA_VERSION} https://github.com/pravega/pravega

# pravega-changes
echo "---- Applying Pravega Changes ----"
cp pravega-changes/docker-pravega/Dockerfile pravega/docker/pravega/Dockerfile
cp -rf pravega-changes/docker-pravega/scripts pravega/docker/pravega/

pushd pravega/docker/pravega
docker build --no-cache --build-arg BASE_IMAGE=${BASE_IMAGE}\
             --build-arg PRAVEGA_VERSION=${PRAVEGA_VERSION}\
            -t pravega_s:${PRAVEGA_VERSION}.0 .
popd

# pravega-bookkeeper
echo "---- Applying Pravega-Bookkeeper Changes ----"
cp pravega-changes/docker-bookkeeper/Dockerfile pravega/docker/bookkeeper/Dockerfile

pushd pravega/docker/bookkeeper
docker build --build-arg BASE_IMAGE=${BASE_IMAGE} --no-cache -t pravega_s:bk .
popd

# compose
echo "---- Applying Pravega-compose Changes ----"
cp pravega-changes/docker-compose/docker-compose-nfs.yml pravega/docker/compose/docker-compose-nfs.yml

# add soft link to docker-compose.yml for easier debug
ln -s pravega/docker/compose/docker-compose-nfs.yml docker-compose-nfs.yml

cat > .env <<EOF
# PRAVEGA_BK_IMAGE=pravega_s:bk
PRAVEGA_IMAGE=pravega_s:${PRAVEGA_VERSION}.0
EOF

# copy SCONE configuration to compose directory
cp pravega-changes/docker-compose/sgx-musl-*.conf pravega/docker/compose/

echo "Done"