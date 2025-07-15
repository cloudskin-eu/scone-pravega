# Deploying Pravega

Deploying Pravega and Sconified Pravega using docker compose.

## Prepare

For the persist volume is necessary to have the nfs-kernel-server service in the machine:
```
sudo apt install nfs-kernel-server
```

Then, it is necessary to create a folder for storing the Pravega data. In our case we will use the external device "sdb", so create a folder for stoing the data:
```
sudo mkdir /mnt/sdb/pravega-data/
sudo chmod -R 777 /mnt/sdb/pravega-data/
```

Once the folder is created we need to configure the nfs server. Add manually at the end of the file "/etc/exports" the following line:
```
/mnt/sdb/pravega-data/ 127.0.0.1(rw,sync,no_subtree_check,no_root_squash)
```

And restart the service:
```
sudo exportfs -ra
sudo systemctl restart nfs-kernel-server
```

Finally, it is neccessary to set the variable HOST\_IP to the machine IP (172.16.3.10 in this case):
```
export HOST_IP=172.16.3.10
```

## Standard Pravega

Deploying standard Pravega:
```
docker compose -f ./docker-compose-std.yml up -d
```

Check logs:
```
docker compose -f ./docker-compose-std.yml logs -f
```

Undeploy:
```
docker-compose -f ./docker-compose-std.yml down
```

## Sconified Pravega

Deploying:
```
docker compose -f ./docker-compose-sgx.yml up -d
```

Check logs:
```
docker compose -f ./docker-compose-sgx.yml logs -f
```

Undeploy:
```
docker-compose -f ./docker-compose-sgx.yml down
```

## Cleaning Data

Once the benchmark were executed, we recommend to delete all to avoid full hard disk:
```
sudo rm -rf /mnt/sdb/pravega-data/*
```

