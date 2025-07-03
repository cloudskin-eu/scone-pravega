# Deploying Pravega

Deploying Pravega and Sconified Pravega using docker compose.

## Sconified Pravega

Deploying:
```
docker compose --env-file .env -f ./docker-compose-sgx.yml up -d
```

Check logs:
```
docker compose logs -f
```

Undeploy:
```
docker-compose -f ./docker-compose-sgx.yml down
```

