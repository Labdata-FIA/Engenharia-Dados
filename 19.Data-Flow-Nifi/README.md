
# LAB Mongodb Kafka e Nifi

---
## Disclaimer
> **Esta configuração é puramente para fins de desenvolvimento local e estudos**
> 

---

# Nifi

## Subindo o ambiente docker com NIFI

> [!IMPORTANT]
> Observe o docker compose, o serviço do NIFI


```bash
 docker compose up -d nifi  docker compose up -d nifi minio
```

> https://localhost:9443/nifi/#/login


|Usuário|Senha|
|------------------|--------------|
|admin|fia@2024@ladata@laboratorio|

https://random-data-api.com/api/v2/users?size=10

## Criando o Process Group

Process Group (Grupo de Processos) é um agrupador lógico que organiza um conjunto de processadores e outros componentes do fluxo de dados

![Lab](/content/nifi0.png)


## Criando o Process 

Os Processors são os principais componentes do Apache NiFi responsáveis por manipular, transformar e mover dados dentro de um fluxo. Cada Processor tem uma função específica, como ler arquivos, fazer requisições HTTP, converter formatos, filtrar registros, gravar em banco de dados, entre outras.

### Criando nosso primeiro GetFile

Crie um Process do tipo GetFile 

![Lab](/content/nifi2-0.png)


### Configurando nosso GetFile

|Property|Value|
|------------------|--------------|
|Input Directory|/files|
|File Filter|.*\.csv$|


> [!IMPORTANT]
> Configura os dados da aba Scheduling

![Lab](/content/nifi3-0.png)




### Parameter Context

No Apache NiFi, Contexto de Parâmetros é um recurso que permite centralizar e gerenciar configurações reutilizáveis dentro de um fluxo de dados. Ele possibilita definir valores parametrizáveis para processadores, permitindo maior flexibilidade e facilidade na manutenção dos fluxos.

![Lab](/content/nifi2.png)


### Os principais benefícios incluem:
* ✅ Reutilização – Um único conjunto de parâmetros pode ser aplicado a vários componentes.
* ✅ Segurança – Parâmetros sensíveis, como credenciais, podem ser protegidos.
* ✅ Facilidade de Alteração – Ajustes podem ser feitos sem modificar diretamente os fluxos.



![Lab](/content/nifi3.png)

![Lab](/content/nifi4.png)

![Lab](/content/nifi-parameter.png)

![Lab](/content/nifi-parameter-2.png)

|Name|Value|
|------------------|--------------|
|DirectoryCSV|/files|
|RecordReader|CSVReader|
|RecordWriter|JsonRecordSetWriter|
|EndPoint-Minio|http://minio:9000|


![Lab](/content/nifi5.png)


Para atribuir um Contexto de Parâmetro a um Grupo de Processos, clique em Configurar, na Paleta de Operação ou no menu de contexto do Grupo de Processos.

![Lab](/content/nifi6.png)

### Como usar ??

Edita o GetFile
|Property|Value|
|------------------|--------------|
|Input Directory|#{DirectoryCSV}|

![Lab](/content/nifi-edit-getfile.png)


## Fazendo a ingestão com Mnio, mas antes...


### Configurando MinIO

Acesso para o MinIO http://localhost:9001/login

* Senha : admin
* password: minioadmin


### Configurando o MinIO

> [!IMPORTANT]
> Crie a camada Raw caso não tenha ainda


![MinIO](../content/minio-04.png)
![MinIO](../content/minio-05.png)
![MinIO](../content/minio-06.png)


![MinIO](../content/minio-07.png)


## Controller Services
No Apache NiFi, os Controller Services são componentes compartilháveis que fornecem funcionalidades comuns a vários processadores dentro de um fluxo de dados. Eles permitem centralizar configurações e melhorar a eficiência do processamento.

Exemplos de Controller Services:
* 🔹 DBCPConnectionPool – Gerencia conexões com bancos de dados.
* 🔹 SSLContextService – Configura SSL/TLS para comunicação segura.
* 🔹 AvroSchemaRegistry – Define esquemas de dados Avro para validação.

![Lab](/content/nifi7.png)


### Criando Controller Services `AWSCredentialsProviderControllerService` para autenticação 

![Lab](/content/nifi22-0.png)

![Lab](/content/nifi22.png)


|Property|Value|
|------------------|--------------|
|Access Key ID|cursolab|
|Secret Access Key|cursolab|


![Lab](/content/nifi22-2.png)

### Criando o Process `PutS3Object`


|Property|Value|
|------------------|--------------|
|Bucket|raw|
|AWS Credentials Provider Service|AWSCredentialsProviderControllerService|
|Object Key|${filename}|
|Endpoint Override URL|#{EndPoint-Minio}|

![Lab](/content/nifi22-4.png)

Na pasta 19.Data-Flow-Nifi\util tem o a arquivo usuarios.csv, copie e cole para a pasta file


![Lab](/content/nifi22-5.png)