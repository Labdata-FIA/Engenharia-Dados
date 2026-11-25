<div align="center">

# ⚡ Como instalar um Cluster do Apache Spark no Docker Desktop utilizando Compose

![Apache Spark](https://img.shields.io/badge/Apache%20Spark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![Python](https://img.shields.io/badge/PySpark-3776AB?style=for-the-badge&logo=python&logoColor=white)
![VS Code](https://img.shields.io/badge/VS%20Code-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white)

</div>

---

## 📑 Sumário

- [📖 Sobre o Apache Spark](#-sobre-o-apache-spark)
- [🏗️ Infraestrutura](#️-infraestrutura)
- [🐳 Passo 1 — Criando o `docker-compose.yml`](#-passo-1--criando-o-docker-composeyml)
- [▶️ Passo 2 — Subindo os containers](#️-passo-2--subindo-os-containers)
- [🧩 Passo 3 — Configurando o VS Code](#-passo-3--configurando-o-vs-code)
- [⚙️ Passo 4 — Criando o `spark-default.conf`](#️-passo-4--criando-o-spark-defaultconf)
- [🔄 Passo 5 — Reiniciando o cluster](#-passo-5--reiniciando-o-cluster)
- [🧪 Passo 6 — Testando o container](#-passo-6--testando-o-container)
- [🎉 Conclusão](#-conclusão)
- [📚 Aulas do Módulo](#-aulas-do-módulo)

---

## 📖 Sobre o Apache Spark

O **Apache Spark** é um mecanismo analítico unificado para processamento de dados em larga escala. Ele fornece APIs de alto nível em **Java, Scala, Python e R**, além de um mecanismo otimizado que suporta gráficos de execução gerais. Ele também suporta um amplo conjunto de ferramentas de alto nível, incluindo **Spark SQL** para SQL e processamento de dados estruturados, **API Pandas no Spark** para cargas de trabalho Pandas, **MLlib** para aprendizado de máquina, **GraphX** para processamento de gráficos e **Structured Streaming** para computação incremental e processamento de fluxo.

---

## 🏗️ Infraestrutura

No docker, o Apache Spark terá a seguinte infra-estrutura:

<!-- 📸 Imagem: arquitetura do cluster Spark no Docker -->

---

## 🐳 Passo 1 — Criando o `docker-compose.yml`

Para montarmos um cenário próximo a esse, iremos usar o arquivo compose;

Crie uma pasta (preferencialmente dentro da onde o seu docker já abre o terminal) e edite o `docker-compose.yml` com o conteúdo abaixo e salve o arquivo

```yaml
services:
  spark-master:
    image: apache/spark:latest
    container_name: spark-master
    hostname: spark-master
    command: bash -c "/opt/spark/bin/spark-class org.apache.spark.deploy.master.Master"
    ports:
      - "7077:7077"   # Porta para comunicação com workers
      - "8080:8080"   # UI do Spark Master
    environment:
      - SPARK_HOME=/opt/spark
    networks:
      - spark-net

  spark-worker-1:
    image: apache/spark:latest
    container_name: spark-worker-1
    hostname: spark-worker-1
    command: bash -c "/opt/spark/bin/spark-class org.apache.spark.deploy.worker.Worker spark://spark-master:7077"
    depends_on:
      - spark-master
    ports:
      - "8081:8081"   # UI do Spark Worker 1
    environment:
      - SPARK_HOME=/opt/spark
    networks:
      - spark-net

  spark-worker-2:
    image: apache/spark:latest
    container_name: spark-worker-2
    hostname: spark-worker-2
    command: bash -c "/opt/spark/bin/spark-class org.apache.spark.deploy.worker.Worker spark://spark-master:7077"
    depends_on:
      - spark-master
    ports:
      - "8082:8081"  # Worker 2 exposto na porta 8082
    environment:
      - SPARK_HOME=/opt/spark
    networks:
      - spark-net


#Parte 2 - Adicionando o Jupyter + Spark
  jupyter:
    image: jupyter/all-spark-notebook:latest
    container_name: jupyter
    hostname: jupyter
    ports:
      - "8888:8888"
    environment:
      - SPARK_HOME=/usr/local/spark
    volumes:
      - ./notebooks:/home/jovyan/work
      - ./notebooks:/conf/spark-defaults.conf:/usr/local/spark/conf/spark-defaults.conf
    depends_on:
      - spark-master
    networks:
      - spark-net


networks:
  spark-net:
    driver: bridge
```

> [!NOTE]
> **Observação:** O arquivo desse `docker-compose.yml` pode ser encontrado em:
> 🔗 https://github.com/datalibtec/spark/blob/main/docker-compose.yml

---

## ▶️ Passo 2 — Subindo os containers

Dentro da pasta que foi salvo o arquivo, digite:

```bash
docker-compose up -d
```

> [!TIP]
> Serão baixadas as imagens do Apache Spark. Os arquivos são grandes, a qual pode demorar um pouco dependendo da conexão de sua internet.

E os containers também subirão:

<!-- 📸 Imagem: containers subindo no terminal -->

Clique em **Containers** e veja que está sendo executado todo o cluster configurado:

<!-- 📸 Imagem: aba Containers do Docker Desktop -->

Acesse via browser, o **[localhost:8080](http://localhost:8080)** e veja que o serviço está sendo executado.

<!-- 📸 Imagem: Spark Master UI -->

---

## 🧩 Passo 3 — Configurando o VS Code

Vamos ter que configurar o arquivo

No **VS Code**, instale as extensões **Dev Containers** e **Containers Tools**, ambos da Microsoft:

<!-- 📸 Imagem: extensão Dev Containers -->

<!-- 📸 Imagem: extensão Container Tools -->

1. Clique em cima da extensão instalada em **Dev-Containers**, selecione o **spark jupyter**.

   <!-- 📸 Imagem: selecionando o container jupyter -->

2. Clique em **Explorer** do VS Code e depois em **"Open Folder"**

   <!-- 📸 Imagem: Open Folder -->

3. Clique na barra de comandos do VS Code, deixe a pasta como está e clique em **OK**

> [!NOTE]
> Perceba que agora no Explorer, voce está enxergando a estrutura de pastas que está dentro do container.

---

## ⚙️ Passo 4 — Criando o `spark-default.conf`

Dentro da pasta `notebooks`, crie uma pasta chamada `conf` e um novo arquivo chamado `spark-default.conf`

<!-- 📸 Imagem: estrutura notebooks/conf/spark-default.conf -->

> [!NOTE]
> O arquivo `spark-default.conf` pode ser baixado em:
> 🔗 https://github.com/datalibtec/spark/blob/main/SPK%20001%20-%20spark-defaults.conf

Coloque esse conteúdo no arquivo:

```properties
spark.master                    spark://spark-master:7077
spark.submit.deployMode         client
spark.driver.host               jupyter
spark.driver.bindAddress        0.0.0.0
spark.ui.enabled                true
```

---

## 🔄 Passo 5 — Reiniciando o cluster

Será necessário fazer a releitura do arquivo novamente, para a crediação do cluster:

Digite o comando no prompt do docker

```bash
docker-compose restart
```

---

## 🧪 Passo 6 — Testando o container

Teste o container com os seguintes passos:

**1.** Ainda no prompt do docker, será necessário entrar no bash do container jupyter. Digite o seguinte comando:

```bash
docker exec -it jupyter bash
```

**2.** Entre na pasta `work` dentr do container jupyter:

```bash
cd work
```

**3.** Precisamos do endereço com o token para acessar via browser do localhost. Digite o comando:

```bash
jupyter server list
```

**4.** Copie o endereco http e cole no endereço do browser. Ele irá dar erro.

> [!IMPORTANT]
> Substitua no endereço somente o `jupyter` por `localhost` e entre dentro da pasta `work`. Clique em **Python 3 (ipyKernel)**

<!-- 📸 Imagem: Jupyter — novo notebook Python 3 -->

**5.** Dê o nome do arquivo de **`SimpleTest`**

> [!NOTE]
> O arquivo SimpleTest pode ser baixado em:
> 🔗 https://github.com/datalibtec/spark/blob/main/SPK%20001%20-%20SimpleTest.ipynb

**6.** Digite o código que está descrito e salve o arquivo

```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
spark.range(1000).show()
```

**7.** Execute o arquivo e o resultado irá aparecer:

<!-- 📸 Imagem: resultado do spark.range(1000).show() -->

> [!TIP]
> ✅ Esse é o primeiro arquivo e quer dizer que o **pyspark** está utilizando o **Spark**.

---

## 🎉 Conclusão

Agora que temos a base da infra estruturada pronta, conseguimos iniciar os estudos em Spark de forma mais profunda. 🚀

---

## 📚 Aulas do Módulo

Clique na aula para acessar a pasta com os materiais:

| Aula | Tema | Materiais |
|:---:|---|---|
| **01** | 🚀 [Introdução ao Apache Spark](./01-introducao) | 📓 Introdução ao Apache Spark<br>📓 PySpark Spark SQL<br>📄 Como instalar um Cluster do Apache Spark no Docker Desktop utilizando Compose |
| **02** | 💻 [Spark Local](./02-spark-local) | 📓 Apache Spark: Caso de Uso Fictício de Vendas |
| **03** | 📦 [Spark Batch](./03-spark-batch) | 📓 Apache Spark - Pipeline de Engenharia de Dados em Batch |
| **04** | 🏛️ [Ingestão no Lakehouse](./04-spark-ingestao-lakehouse) | 📓 Data Lakehouse - Medallion - Sales Performance<br>📓 Data Lakehouse - Medallion - Sales Performance (Sem Delta) |
| **05** | 🌊 [Spark Structured Streaming](./05-spark-structured-streaming) | 📓 Structured Streaming + Delta Lake - Sales Performance<br>📓 Structured Streaming - Sales Performance (Sem Delta) |
| **06** | 🧱 [LAB Databricks](./06-spark-lab-databricks) | 📓 Apache Spark + SQL - LAB Databricks Free Edition - DRE Consolidado |

<div align="center">

**[⬆️ Voltar ao topo](#-como-instalar-um-cluster-do-apache-spark-no-docker-desktop-utilizando-compose)**

</div>
