# OpenMessaging Benchmark clients

Deploying OpenMessaging Benchmark client.

## Standard OpenMessaging Benchmark tool

First, download the docker image from DockerHub:
```
sudo docker pull acueva/client_ben:latest
```

Then start the container using the image:
```
sudo docker run -d acueva/client_ben:latest
```

You can validate it and get the container id by running:
```
sudo docker ps
```

Once you have the container id it is easy to the enter the container and run the test cases:
```
sudo docker exec -it <CONTAINER ID> /bin/bash
./run.sh > output.txt &
```

Finally, copy the results out of the container and stop it:
```
sudo docker cp <CONTAINER ID>:/app/results ~/
sudo docker stop <CONTAINER ID>
sudo docker rm <CONTAINER ID>
```

## Sconified OpenMessaging Benchmark tool

In case you want to use the Sconified OpenMessaging benchmark version, it is necessary to login into the Scotain registry and download the image:
```
sudo docker login registry.scontain.com
sudo docker pull registry.scontain.com/amiguel/neardatapublic/pravega:client_ben
```

Once the image was downloaded it can be executed using:
```
sudo docker run --device=/dev/sgx_enclave -d registry.scontain.com/amiguel/neardatapublic/pravega:client_ben
```

This image was not updated, so before executing the test cases take a look to the files, and execute:
```
mv openmessaging-benchmark-0.0.1-SNAPSHOT/* omb/
rm -fr openmessaging-benchmark-0.0.1-SNAPSHOT openmessaging-benchmark-0.0.1-SNAPSHOT-bin.tar.gz
apk add python3 py3-pip
pip install pyyaml
```

After executing those commands and edit the files the process is the same as the Standard OpenMessaging benchmakr version.

