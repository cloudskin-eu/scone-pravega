# Deploying Pravega

Deploying Pravega and Sconified Pravega using docker compose.

## Standard Pravega

```
docker compose --env-file .env -f ./docker-compose-std.yml up -d
docker compose -f ./docker-compose-std.yml logs -f
docker-compose -f ./docker-compose-std.yml down
```

## Sconified Pravega

In this folder run the following commands.

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

