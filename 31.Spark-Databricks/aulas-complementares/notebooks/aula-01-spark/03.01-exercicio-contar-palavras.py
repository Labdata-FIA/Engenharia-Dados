# Databricks notebook source
# MAGIC
# MAGIC %md
# MAGIC
# MAGIC ### Exercício de Contagem de Palavras
# MAGIC
# MAGIC Neste exercício, vamos processar um arquivo de texto para contar quantas vezes cada palavra aparece no documento. A contagem de palavras é um exemplo comum de manipulação de grandes volumes de texto usando o Spark.
# MAGIC
# MAGIC #### Arquivo Utilizado: `contar-palavras.txt`
# MAGIC O arquivo contém informações sobre o projeto Apache Spark, e vamos usar seu conteúdo para contar as palavras.
# MAGIC
# MAGIC > path: https://raw.githubusercontent.com/rafael-negrao/laboratorio-spark/main/dados/contar-palavras.txt
# MAGIC ---
# MAGIC
# MAGIC ### Passos do Exercício:
# MAGIC
# MAGIC 1. **Carregar o arquivo de texto**: Ler o arquivo que contém múltiplas linhas de texto.
# MAGIC 2. **Quebrar o texto em palavras**: Dividir as linhas de texto em palavras individuais.
# MAGIC 3. **Normalizar o texto**: Converter todas as palavras para minúsculas e remover espaços em branco.
# MAGIC 4. **Contar a ocorrência de cada palavra**: Calcular quantas vezes cada palavra aparece no texto.
# MAGIC 5. **Exibir o resultado**: Mostrar a contagem de palavras ordenada pela frequência.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### Preview do Arquivo de Texto:
# MAGIC Aqui está um exemplo do conteúdo do arquivo `contar-palavras.txt` que será processado:
# MAGIC
# MAGIC ```
# MAGIC Spark is a unified analytics engine for large-scale data processing. It provides
# MAGIC high-level APIs in Scala, Java, Python, and R, and an optimized engine that
# MAGIC supports general computation graphs for data analysis...
# MAGIC ```
# MAGIC
# MAGIC ### **Resultado Esperado**:
# MAGIC As palavras mais frequentes serão exibidas junto com suas contagens. Por exemplo:
# MAGIC ```
# MAGIC | palavra  | count |
# MAGIC |----------|-------|
# MAGIC | spark    | 15    |
# MAGIC | for      | 10    |
# MAGIC | data     | 8     |
# MAGIC | and      | 7     |
# MAGIC | the      | 6     |
# MAGIC ...
# MAGIC ```
# MAGIC
# MAGIC

# COMMAND ----------

spark

# COMMAND ----------

# MAGIC %sh
# MAGIC wget https://raw.githubusercontent.com/rafael-negrao/laboratorio-spark/main/dados/contar-palavras.txt -O /tmp/contar-palavras.txt

# COMMAND ----------

dbutils.fs.mv("file:/tmp/contar-palavras.txt", "dbfs:/tmp/contar-palavras.txt")

# COMMAND ----------



# COMMAND ----------



# COMMAND ----------



# COMMAND ----------



# COMMAND ----------


