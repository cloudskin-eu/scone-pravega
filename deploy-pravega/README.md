# Deploying Pravega

Deploying Pravega and Sconified Pravega using docker compose.

## Prepare

Before deploying Pravega is important to define the variable HOST\_IP (172.16.3.10 in this example) and create the a folder for persistent volume.
```
export HOST_IP=172.16.3.10
sudo mkdir /pravega-data/
sudo chmod -R 777 /pravega-data/
```

In case nfs server was not installed, it needs to be installed and the folder should be added to the exports file:
```
sudo apt install nfs-kernel-server
sudo echo "/pravega-data/ 127.0.0.1(rw,sync,no_subtree_check,no_root_squash)" >> /etc/exports
sudo exportfs -ra
sudo systemctl restart nfs-kernel-server
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
docker compose --env-file .env -f ./docker-compose-sgx.yml up -d
```

Check logs:
```
docker compose -f ./docker-compose-sgx.yml logs -f
```

Undeploy:
```
docker-compose -f ./docker-compose-sgx.yml down
```

