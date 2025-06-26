# scone-pravega
Benchmarks for Sconified Pravega server images

## Status
The status could be seen in the table below.

| Pravega component  | Status |
| ------------- | ------------- |
| Controller  | sconified |
| Segment store | sconified |
| Zookeeper | sconified by existing image (registry.scontain.com:5050/sconecuratedimages/apps:zookeeper-3-alpine-scone5.9) |
| Bookkeeper | sconified, but fragile |
| HDFS | native |
| Java client | untested |
| Java benchmark | sconified by Robert |
| Rust client | untested |

## Build pravega

At this moment, we don't actually need to modify any pravega components. What needs to be changed is only some of the parameters and build process.

The script [prepare_pravega.sh](./prepare_pravega.sh) is there to help you build the images based on the latest release in Github. (Currently 0.13)

Prerequisites : 
- You need to have access to the BASE_IMAGE in [prepare_pravega.sh](./prepare_pravega.sh)
- Right now it's `registry.scontain.com:5050/ardhipoetra/cloudskin-images/java:ubuntu20.04-scone5.10.0-rc.1`: java-compatible ubuntu-based scone runtime.

Build process : 
- execute [prepare_pravega.sh](./prepare_pravega.sh)
- This will build the necessary images (pravega and bookkeeper):
    - `pravega_s:<version>.0` for pravega, and
    - `pravega_s:bk` for bookkeeper
- At the end, it will generate the .env file which should be consumed by docker-compose to spawn them.

## Deploy pravega 

Apparently, you need to clear some leftover data, so do this beforehand: 
`sudo rm -rf pravega/docker/compose/data/`

Then, in this directory, invoke `docker compose --env-file .env -f pravega/docker/compose/docker-compose-nfs.yml up --force-recreate`

Change `.env` file to switch image to use.

**Important** : it's very important to also remove the containers before subsequent run! Somehow many things break if this is not being done. One can simply use `docker-compose -f pravega/docker/compose/docker-compose-nfs.yml down`.

All in all, I recommend the following command to copy-paste : 
```
sudo rm -rf pravega/docker/compose/data/ \
&& docker compose --env-file .env -f pravega/docker/compose/docker-compose-nfs.yml up --force-recreate \
&& docker-compose -f pravega/docker/compose/docker-compose-nfs.yml down
```

## Test the deployment

Important points to follow : 

- First, take note the controller's IP. Invoke this command : 
```
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' compose-controller-1
```

- Assuming pravega components is deployed by a compose, we need to connect our _runner_ to it. For example, with `docker` wants to connect to the default docker compose, you would need to add `--network=compose_default`

- Then, inside the runner container, change the IP address of the controller.

### Test example

Here, we can try using the image [acueva/pravega-rust-benchmark](https://hub.docker.com/r/acueva/pravega-rust-benchmark). Since it needs a yaml config file, I provide a small example in [config-rust-benchmark.yaml](./config-rust-benchmark.yaml). Suppose the controller' IP is `172.18.0.5`, then the yaml file will be : 

```
name: CONFIG_EXAMPLE
address: "172.18.0.5:9090"
payload_file: "/benchmark/payload-100b.data"
message_num: 50
producer_rate: 10
```

Then, we can run the example by doing this : 
```
docker run --rm --network=compose_default --entrypoint=/benchmark/pravega-rust-benchmark -v `pwd`:/data/:ro acueva/pravega-rust-benchmark /data/config-rust-benchmark.yaml
```

Then the output will look like : 
```
Connecting to Pravega 172.18.0.5:9090
Init Environment
         Scope scope1750942431 created
         Stream stream1750942431 created
Starting WarmUp
Starting Benchmark
         + Messages Sent 10
         - Messages Read 10
         + Messages Sent 20
         - Messages Read 20
         + Messages Sent 30
         - Messages Read 30
         + Messages Sent 40
         - Messages Read 40
         + Messages Sent 50
         - Messages Read 50
         - No more data to read
Benchmark finished
```