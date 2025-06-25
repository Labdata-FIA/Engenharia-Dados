# Lab Armazenamento Distribuido


## Disclaimer
> **As configurações dos Laboratórios é puramente para fins de desenvolvimento local e estudos**


## Pré-requisitos?
* Docker
* Docker-Compose


Este laboratório tem como objetivo praticar comandos HDFS utilizando um cluster Hadoop simulado com Docker. A estrutura de diretórios segue a arquitetura em camadas do modelo **Medalhão (Bronze, Silver, Gold)**, com exemplo de particionamento por ano, mês e dia.

## 📦 Estrutura de diretórios HDFS

A estrutura a ser criada no HDFS será a seguinte:

```

├── bronze/
│   └── ano=2025/mes=06/dia=19/
├── silver/
│   └── ano=2025/mes=06/dia=19/
└── gold/
    └── ano=2025/mes=06/dia=19/
```

---

* > http://localhost:9864/
* > http://localhost:9870/

```bash
docker container rm $(docker ps -a -q) -f
docker volume prune

docker compose up -d datanode namenode minio

docker exec -it namenode bash

```


### 🔍 Verificar modo seguro (Safe Mode)

```bash
hdfs dfsadmin -safemode get
```

### Se o retorno for `Safe mode is OFF` então não está, pode pular o proximo comando.

### 🚫 Sair do modo seguro manualmente

```bash
hdfs dfsadmin -safemode leave
```

## 🚀 Comandos iniciaiss

### Criar diretórios no HDFS

```bash
hdfs dfs -mkdir -p /bronze/ano=2025/mes=06/dia=19
hdfs dfs -mkdir -p /silver/ano=2025/mes=06/dia=19
hdfs dfs -mkdir -p /gold/ano=2025/mes=06/dia=19
```


---

## 📂 Exercícios práticos

### 1. Envio de arquivos para a camada Bronze

```bash
echo "cliente_id,nome" > /util/clientes.csv
echo "1,Fernando" >> /util/clientes.csv
cat  /util/clientes.csv

```

### 1.1 Enviando o arquivo `clientes.csv` para o HDFS

```bash
hdfs dfs -put /util/clientes.csv /bronze/ano=2025/mes=06/dia=19/
```

### 2. Visualização dos dados

```bash
hdfs dfs -ls /bronze/ano=2025/mes=06/dia=19
hdfs dfs -cat /bronze/ano=2025/mes=06/dia=19/clientes.csv
```


### 3. Simular transformação para Silver

```bash
hdfs dfs -cp /bronze/ano=2025/mes=06/dia=19/clientes.csv \
          /silver/ano=2025/mes=06/dia=19/

hdfs dfs -ls /silver/ano=2025/mes=06/dia=19/

```

### 4. Simular tratamento final para Gold

```bash
hdfs dfs -cp /silver/ano=2025/mes=06/dia=19/clientes.csv \
          /gold/ano=2025/mes=06/dia=19/

hdfs dfs -ls /gold/ano=2025/mes=06/dia=19/

```

### 5. Buscando os dados, mas antes apague o arquivo `clientes.csv` da pasta util dentro do seu computador o maquina virtual
```bash
 hdfs dfs -get /bronze/ano=2025/mes=06/dia=19/clientes.csv ./util/

```


## 🧹 Limpeza

Para remover um diretório e todo seu conteúdo:

```bash
hdfs dfs -rm -r /bronze
```


### Acesso o endereço abaixo para que tenha uma visão do Haddop
> http://localhost:9870/


### Acessando os diretórios
![HFDS](/content/hdfs-00.png)


### 📦 Verificar blocos de um arquivo

```bash
hdfs fsck /bronze/ano=2025/mes=06/dia=19/clientes.csv -files -blocks -locations
```

Mostra a integridade do arquivo, onde os blocos estão localizados e sua replicação.

### 📊 Ver uso de espaço no HDFS

```bash
hdfs dfs -du -h /
```


---

## ⚙️ Scripts úteis para administradores

### 📌 Script para listar todos os arquivos e blocos

```bash
hdfs dfs -ls -R / | awk '{print $8}' | while read file; do
  echo "Arquivo: $file"
  hdfs fsck $file -files -blocks -locations
done
```

### 📌 Script para checar status de replicação

```bash
hdfs fsck / -blocks -locations -files | grep -i 'Under replicated'
```


## Agora é com voce! Crie a mesma estrutura de armazenamento com o MiniO

> http://localhost:9001/login

* Usuário: admin
* Senha: minioadmin

