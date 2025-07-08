# OpenMessaging Benchmark clients

Deploying OpenMessaging Benchmark client.

## Standard OpenMessaging Benchmark tool

```
sudo docker pull acueva/client_ben:latest
sudo docker run -d acueva/client_ben:latest
sudo docker exec -it <CONTAINER ID> /bin/bash
sudo docker cp <CONTAINER ID>:/app/results ~/dell/results/
sudo docker stop <CONTAINER ID>
sudo docker rm <CONTAINER ID>
```

## Sconified OpenMessaging Benchmark tool

Install the Sconified OpenMessaging Benchmark tool:
```
sudo docker login registry.scontain.com
sudo docker pull registry.scontain.com/amiguel/neardatapublic/pravega:client_ben
```

Execute the image:
```
sudo docker run --device=/dev/sgx_enclave -d registry.scontain.com/amiguel/neardatapublic/pravega:client_ben
```

Enter the image:
```
sudo docker ps -a
sudo docker exec -it <CONTAINER ID> /bin/bash
```

Finishing setup:
```
mv openmessaging-benchmark-0.0.1-SNAPSHOT/* omb/
rm -fr openmessaging-benchmark-0.0.1-SNAPSHOT openmessaging-benchmark-0.0.1-SNAPSHOT-bin.tar.gz
apk add python3 py3-pip
pip install pyyaml
```

Before running the test check the test_case.csv and run.sh files. The CSV file have the configuration of the test cases that are going to be run. Then start the benchmarking by running:
```
./run.sh > output.txt &
```

Finally, to stop and delete the contianer and copy the results to the host machine, in the host machine execute:
```
sudo docker cp <CONTAINER ID>:/app/results ~/
sudo docker stop <CONTAINER ID>
sudo docker rm <CONTAINER ID>
```

