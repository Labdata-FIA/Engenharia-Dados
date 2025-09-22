# Lab Pipeline Integrado


## Disclaimer
> **As configurações dos Laboratórios é puramente para fins de desenvolvimento local e estudos**


## Pré-requisitos?
* Docker
* Docker-Compose

# Iniciando o ambiente

```sh
docker compose up -d spark minio kafka-broker zookeeper
```


> http://localhost:8889/

> http://localhost:9001/

### No minio crie os buckets para as camadas (bronze, silver e gold) e access e secrets keys (, datalake)



```sh
docker exec -it kafka-broker /bin/bash

kafka-topics --bootstrap-server localhost:9092 --list 

kafka-console-consumer --bootstrap-server localhost:9092 --topic bronze-user --from-beginning

```

