# Databricks notebook source
spark

# COMMAND ----------

# MAGIC %md
# MAGIC # Instruções do Exercício
# MAGIC Este notebook tem a responsabilidade em fornecer as instruções necessárias para criação das camadas:
# MAGIC - landing
# MAGIC - raw
# MAGIC - bronze
# MAGIC - silver
# MAGIC
# MAGIC Utilizar neste exercício:
# MAGIC - Estratégia de solução
# MAGIC   - Spark Stateless
# MAGIC     - spark.read
# MAGIC     - ... DataFrame.write
# MAGIC     - foreachBatch (quando necessário)
# MAGIC   - Spark Stateful
# MAGIC     - spark.readStream
# MAGIC     - ... DataFrame.writeStream
# MAGIC     - checkpoint
# MAGIC     - foreachBatch (quando necessário)
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Principais variáveis

# COMMAND ----------


# dados de armazenamento
aluno = 'rafael_negrao_001'
banco_de_dados = "exemploapidb"
tabela = "contato_eventos"

# dados para acessar o kafka
brokers = "35.170.45.4:9094"
topic = "mysql.exemplodb.contato_entity"
groupId = f"consumer-landing-{tabela}-{aluno}-01"


print(
f'''
aluno = {aluno}
banco_de_dados = {banco_de_dados}
tabela = {tabela}

brokers = {brokers}
topic = {topic}
groupId = {groupId}
'''
)


# COMMAND ----------

# MAGIC %md
# MAGIC #### Definicao da localizacao do sistema de armazenamento

# COMMAND ----------

warehouse_path = "/Volumes/workspace/default/laboratorio-spark/"

localizacao_base_landing = f'{warehouse_path}/fialabdata-engenharia-deltalake/landing/{banco_de_dados}_{aluno}'
localizacao_base_landing_checkpoint = f'{localizacao_base_landing}/_checkpoint'

localizacao_base_raw = f'{warehouse_path}/fialabdata-engenharia-deltalake/raw/{banco_de_dados}_{aluno}'
localizacao_base_raw_tabela = f'{localizacao_base_raw}/{tabela}'
localizacao_base_raw_tabela_checkpoint = f'{localizacao_base_raw_tabela}/_checkpoint'

localizacao_base_bronze = f'{warehouse_path}/fialabdata-engenharia-deltalake/bronze/{banco_de_dados}_{aluno}'
localizacao_base_bronze_tabela = f'{localizacao_base_bronze}/{tabela}'
localizacao_base_bronze_tabela_checkpoint = f'{localizacao_base_bronze_tabela}/_checkpoint'

localizacao_base_silver = f'{warehouse_path}/fialabdata-engenharia-deltalake/silver/{banco_de_dados}_{aluno}'
localizacao_base_silver_tabela = f'{localizacao_base_silver}/{tabela}'
localizacao_base_silver_tabela_checkpoint = f'{localizacao_base_silver_tabela}/_checkpoint'

print(
f'''

warehouse_path = {warehouse_path}

localizacao_base_landing = {localizacao_base_landing}
localizacao_base_landing_checkpoint = {localizacao_base_landing_checkpoint}

localizacao_base_raw = {localizacao_base_raw}
localizacao_base_raw_tabela = {localizacao_base_raw_tabela}
localizacao_base_raw_tabela_checkpoint = {localizacao_base_raw_tabela_checkpoint}

localizacao_base_bronze = {localizacao_base_bronze}
localizacao_base_bronze_tabela = {localizacao_base_bronze_tabela}
localizacao_base_bronze_tabela_checkpoint = {localizacao_base_bronze_tabela_checkpoint}

localizacao_base_silver = {localizacao_base_silver}
localizacao_base_silver_tabela = {localizacao_base_silver_tabela}
localizacao_base_silver_tabela_checkpoint = {localizacao_base_silver_tabela_checkpoint}
'''
)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- limpeza
# MAGIC -- drop table raw_exemploapidb.contato_eventos;
# MAGIC -- drop database raw_exemploapidb;
# MAGIC -- drop table bronze_exemploapidb.contato_eventos;
# MAGIC -- drop database bronze_exemploapidb;
# MAGIC -- drop database silver_exemploapidb;
# MAGIC -- drop database silver_exemploapidb.contato_eventos;

# COMMAND ----------

# limpeza
dbutils.fs.rm(localizacao_base_landing, True)
dbutils.fs.rm(localizacao_base_raw, True)
dbutils.fs.rm(localizacao_base_bronze, True)
dbutils.fs.rm(localizacao_base_silver, True)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Visão geral das camadas
# MAGIC
# MAGIC ![Camadas Data Lake](https://raw.githubusercontent.com/rafael-negrao/laboratorio-databricks/main/imagens/camadas-datalake.png)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Camada LANDING

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, StringType, LongType, ArrayType, BooleanType
from pyspark.sql.functions import from_json, col, when, lit, from_utc_timestamp, row_number, desc, to_timestamp

# COMMAND ----------

# MAGIC %md
# MAGIC ### Definição do Schema de Leitura

# COMMAND ----------

schema_value = StructType([
    StructField("payload", StructType([
        StructField("after", StructType([
            StructField("id", LongType(), True),
            StructField("email", StringType(), True),
            StructField("nome", StringType(), True),
            StructField("telefone", StringType(), True),
            StructField("data_criacao", LongType(), True),
            StructField("data_atualizacao", LongType(), True)]), True),
        StructField("before", StructType([
            StructField("id", LongType(), True),
            StructField("email", StringType(), True),
            StructField("nome", StringType(), True),
            StructField("telefone", StringType(), True),
            StructField("data_criacao", LongType(), True),
            StructField("data_atualizacao", LongType(), True)]), True),
        StructField("op", StringType(), True),
        StructField("source", StructType([
            StructField("connector", StringType(), True),
            StructField("db", StringType(), True),
            StructField("file", StringType(), True),
            StructField("gtid", StringType(), True),
            StructField("name", StringType(), True),
            StructField("pos", LongType(), True),
            StructField("query", StringType(), True),
            StructField("row", LongType(), True),
            StructField("server_id", LongType(), True),
            StructField("snapshot", StringType(), True),
            StructField("table", StringType(), True),
            StructField("thread", StringType(), True),
            StructField("ts_ms", LongType(), True),
            StructField("version", StringType(), True)]), True),
        StructField("transaction", StringType(), True),
        StructField("ts_ms", LongType(), True)]), True),
    StructField("schema", StructType([
        StructField("fields", ArrayType(StructType([
            StructField("field", StringType(), True),
            StructField("fields", ArrayType(
                StructType([
                    StructField("default", StringType(), True),
                    StructField("field", StringType(), True),
                    StructField("name", StringType(), True),
                    StructField("optional", BooleanType(), True),
                    StructField("parameters", StructType([StructField("allowed", StringType(), True)]), True),
                    StructField("type", StringType(), True),
                    StructField("version", LongType(), True)]), True), True),
            StructField("name", StringType(), True),
            StructField("optional", BooleanType(), True),
            StructField("type", StringType(), True)]), True), True),
        StructField("name", StringType(), True),
        StructField("optional", BooleanType(), True),
        StructField("type", StringType(), True)]), True)])

schema_key = StructType([
    StructField("payload", StructType([
        StructField("id", LongType(), True)]), True),
    StructField("schema", StructType([
        StructField("fields", ArrayType(StructType([
            StructField("field", StringType(), True),
            StructField("optional", BooleanType(), True),
            StructField("type", StringType(), True)]), True), True),
        StructField("name", StringType(), True),
        StructField("optional", BooleanType(), True),
        StructField("type", StringType(), True)]), True)])

# COMMAND ----------

# MAGIC %md
# MAGIC ### Leitura dos dados

# COMMAND ----------

is_stream_mode = False

# COMMAND ----------

print(f"is_stream_mode = {is_stream_mode}")
if is_stream_mode:
  df_kafka_stream = (
    spark 
      .readStream
      .format("kafka") 
      .option("kafka.bootstrap.servers", brokers) 
      .option("subscribe", topic) 
      .option("group.id", groupId)
      .option("startingOffsets", "earliest") 
      .load())
else:
  df_kafka_stream = (
    spark
      .read
      .format("kafka") 
      .option("kafka.bootstrap.servers", brokers) 
      .option("subscribe", topic) 
      .option("group.id", groupId)
      .option("startingOffsets", "earliest") 
      .load())

# COMMAND ----------

# MAGIC %md
# MAGIC ### Transformação dos dados

# COMMAND ----------

df_estagio_01 = (
  df_kafka_stream
    .withColumn("key", col("key").cast("string"))
    .withColumn("value", col("value").cast("string"))
    .withColumn("key_struct", from_json(col("key"), schema_key))
    .withColumn("value_struct", from_json(col("value"), schema_value))
    .withColumn("date", from_utc_timestamp((col("value_struct.payload.ts_ms") / lit(1000)).cast("timestamp"), "Brazil/East").cast("date"))
    .withColumn("date", when(col("date").isNull(), col("timestamp").cast("date")).otherwise(col("date")))
)

# COMMAND ----------

if not is_stream_mode:
  display(df_estagio_01)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Gravação dos dados

# COMMAND ----------

if is_stream_mode:
  query = (
    df_estagio_01
      .select('date', 'value')
      .writeStream
      .format('json')
      .outputMode('append')
      .option('checkpointLocation', localizacao_base_landing_checkpoint)
      .start(localizacao_base_landing)
  )
  query.awaitTermination()
else:
  (
    df_estagio_01
      .select('date', 'value')
      .write
      .format('json')
      .mode('append')
      .partitionBy('date')
      .save(localizacao_base_landing)
  )

# COMMAND ----------

display(dbutils.fs.ls(localizacao_base_landing))
display(dbutils.fs.ls(f'{localizacao_base_landing}/date=2025-01-06'))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Camada RAW

# COMMAND ----------

# MAGIC %md
# MAGIC Responsabilidades desta camada:
# MAGIC - O particionamento será por data que o dado foi criado ou alterado.
# MAGIC - O dado precisa ser armazendado sem transformações

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### Criação das estruturas
# MAGIC ---
# MAGIC - database: 
# MAGIC   - database name: **raw_exemploapidb**
# MAGIC   - location: **utilizar a variável localizacao_base_raw**
# MAGIC - tabela
# MAGIC   - table name: **contato_eventos**
# MAGIC   - location: **utilizar a variável localizacao_base_raw_tabela**
# MAGIC
# MAGIC Os detalhes do schema para criação da tabela está no trecho **Gravação dos dados**

# COMMAND ----------

# MAGIC %md
# MAGIC ### Arquivo Origem de Dados
# MAGIC Sobre o arquivo origem de dados:
# MAGIC - Localização: **/user/hive/warehouse/fialabdata-engenharia-deltalake/landing/contato_eventos**
# MAGIC - Formato: **json**

# COMMAND ----------

print(f'''localizacao_base_raw = {localizacao_base_raw}''')

# COMMAND ----------

display(
spark.sql(f"""
CREATE DATABASE IF NOT EXISTS raw_exemploapidb
LOCATION '{localizacao_base_raw}'
""")
)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Leitura dos dados

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC Para carregar arquivos no modo stream e ter inferência automática
# MAGIC https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/schema.html

# COMMAND ----------

from pyspark.sql import functions as F


df_raw_stage_01 = spark.read.json(localizacao_base_landing)
display(df_raw_stage_01)

# COMMAND ----------

df_raw_stage_02 = (
  df_raw_stage_01
    .withColumn('value_json', F.col('value'))
)
display(df_raw_stage_02)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Transformação dos dados
# MAGIC

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, StringType, LongType, ArrayType, BooleanType

df_raw_stage_03 = (
  df_raw_stage_02
    .withColumn('value_struct', F.from_json(F.col('value_json'), schema_value))
    .withColumn('transaction_date', from_utc_timestamp(
      (col("value_struct.payload.ts_ms") / lit(1000)).cast("timestamp"), "Brazil/East").cast("date"))
    .withColumn('raw_date', F.current_date())
)

display(df_raw_stage_03)

# COMMAND ----------

df_raw_stage_04 = (
  df_raw_stage_03
    .select('transaction_date', 'raw_date', 'value')
)
display(df_raw_stage_04)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Gravação dos dados

# COMMAND ----------

# MAGIC %md
# MAGIC **Schema**
# MAGIC
# MAGIC |Column|Type|Obs.|
# MAGIC |---|---|--|
# MAGIC |transaction_date|date|Utilizar o campo dateTime contido na mensagem
# MAGIC |raw_date|date|Utilizar a função F.current_date()
# MAGIC |value|string (base64)|

# COMMAND ----------

print(f'localizacao_base_raw_tabela = {localizacao_base_raw_tabela}')

# COMMAND ----------

from delta.tables import *

delta_table = (
  DeltaTable.createIfNotExists(spark)
    .tableName('raw_exemploapidb.contato_eventos')
    .location(localizacao_base_raw_tabela)
    .partitionedBy('raw_date')
    .addColumns(df_raw_stage_04.schema)
    .execute() # buid
)

display(delta_table.detail())

# COMMAND ----------

# MAGIC %sql
# MAGIC desc extended raw_exemploapidb.contato_eventos

# COMMAND ----------

from pyspark.sql import DataFrame
def foreachBatchRaw(batchDF: DataFrame, batchId: int):
  (
    batchDF
      .write
      .format('delta')
      .mode('append')
      .partitionBy('raw_date')
      .saveAsTable('raw_exemploapidb.contato_eventos')
  )

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC Como ficaria no modo stream
# MAGIC
# MAGIC ```python
# MAGIC query = (
# MAGIC     df_raw_stage_04
# MAGIC       .writeStream
# MAGIC       .outputMode("append")
# MAGIC       .foreachBatch(foreachBatchRaw)
# MAGIC       .start()
# MAGIC )
# MAGIC query.awaitTermination()
# MAGIC ```

# COMMAND ----------


foreachBatchRaw(df_raw_stage_04, 0)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from raw_exemploapidb.contato_eventos

# COMMAND ----------

# MAGIC %md
# MAGIC ## Camada BRONZE

# COMMAND ----------

# MAGIC %md
# MAGIC Responsabilidades desta camada:
# MAGIC - O particionamento será por data que o dado foi criado ou alterado.
# MAGIC - Modo de escrita: append
# MAGIC - Aplicar o schema ao dado

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### Criação das estruturas
# MAGIC ---
# MAGIC - database: 
# MAGIC   - database name: **raw_exemploapidb**
# MAGIC   - location: **utilizar a variável localizacao_base_bronze**
# MAGIC - tabela
# MAGIC   - table name: **contato_eventos**
# MAGIC   - location: **utilizar a variável localizacao_base_bronze_tabela**
# MAGIC
# MAGIC Os detalhes do schema para criação da tabela está no trecho Gravação dos dados

# COMMAND ----------

print(f'localizacao_base_bronze = {localizacao_base_bronze}')

# COMMAND ----------

display(
spark.sql(f"""
CREATE DATABASE IF NOT EXISTS bronze_exemploapidb
LOCATION '{localizacao_base_bronze}'
""")
)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Leitura dos dados
# MAGIC Utilizar o que foi persistido na camada **bronze**
# MAGIC
# MAGIC Documentação de referência no modo stream para delta: https://docs.databricks.com/pt/structured-streaming/delta-lake.html#stream-a-delta-lake-change-data-capture-cdc-feed

# COMMAND ----------

# leitura no modo stream
print(f"is_stream_mode = {is_stream_mode}")
if is_stream_mode:
  df_bronze_stage_01 = spark.readStream.table("raw_exemploapidb.contato_eventos")
else:
  df_bronze_stage_01 = spark.table('raw_exemploapidb.contato_eventos')
  display(df_bronze_stage_01)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Transformação dos dados

# COMMAND ----------

df_bronze_stage_02 = (
  df_bronze_stage_01
    .withColumn('value_json', F.col('value'))
    .withColumn('value_struct', F.from_json(F.col('value_json'), schema_value))
    .withColumn("transaction_date", from_utc_timestamp((col("value_struct.payload.ts_ms") / lit(1000)).cast("timestamp"), "Brazil/East").cast("date"))
    .withColumn('bronze_date', F.current_date())
)
if not is_stream_mode:
  display(df_bronze_stage_02)

# COMMAND ----------

df_bronze_stage_03 = (
  df_bronze_stage_02
    .select(
      F.col('transaction_date'),
      F.col('raw_date'),
      F.col('bronze_date'),
      F.col('value_struct.*'),
    )
)

if not is_stream_mode:
  display(df_bronze_stage_03)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Gravação dos dados

# COMMAND ----------

print(f'localizacao_base_bronze_tabela = {localizacao_base_bronze_tabela}')

# COMMAND ----------

from delta.tables import *

delta_table = (
  DeltaTable.createIfNotExists(spark)
    .tableName('bronze_exemploapidb.contato_eventos')
    .location(localizacao_base_bronze_tabela)
    .partitionedBy('bronze_date')
    .addColumns(df_bronze_stage_03.schema)
    .execute()
)

display(delta_table.detail())

# COMMAND ----------

def foreachBatchBronze(batchDF: DataFrame, batchId: int):
  (
    batchDF
      .write
      .format('delta')
      .mode('append')
      .partitionBy('bronze_date')
      .saveAsTable('bronze_exemploapidb.contato_eventos')
  )

# COMMAND ----------

if is_stream_mode:
  query = (
    df_bronze_stage_03
      .writeStream
      .format("console")
      .outputMode("append")
      .option("checkpointLocation", localizacao_base_bronze_tabela_checkpoint)
      .foreachBatch(foreachBatchBronze)
      .start()
  )
  query.awaitTermination()
else:
  foreachBatchBronze(df_bronze_stage_03, 0)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from bronze_exemploapidb.contato_eventos

# COMMAND ----------

# MAGIC %md
# MAGIC ## Camada SILVER

# COMMAND ----------

# MAGIC %md
# MAGIC Responsabilidades desta camada:
# MAGIC - O particionamento será por data que o dado foi criado ou alterado.
# MAGIC - Ter dado mais próximo possível do universo transacional

# COMMAND ----------

# MAGIC %md
# MAGIC ### Criação das estruturas
# MAGIC ---
# MAGIC - database: 
# MAGIC   - database name: **silver_exemploapidb**
# MAGIC   - location: **utilizar a variável localizacao_base_silver**
# MAGIC - tabela
# MAGIC   - table name: **contato_eventos**
# MAGIC   - location: **utilizar a variável localizacao_base_silver_tabela**

# COMMAND ----------

# MAGIC %md
# MAGIC Intruções para o merge:
# MAGIC - **payload.op**
# MAGIC   - **r**: read event, primeiro carregamento da tabela
# MAGIC   - **c**: create event
# MAGIC   - **u**: update event
# MAGIC   - **d**: delete event
# MAGIC - **id**: identificador único do contato
# MAGIC   - **payload.after.id**: quando aplicado para os eventos: r, c, u
# MAGIC   - **payload.before.id**: quando o evento for delete
# MAGIC
# MAGIC Os detalhes do schema para criação da tabela está no trecho Gravação dos dados

# COMMAND ----------

print(f'localizacao_base_silver = {localizacao_base_silver}')

# COMMAND ----------

display(
spark.sql(f"""
CREATE DATABASE IF NOT EXISTS silver_exemploapidb
LOCATION '{localizacao_base_silver}'
""")
)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Leitura dos dados
# MAGIC
# MAGIC Utilizar o que foi persistido na camada **raw**

# COMMAND ----------

print(f"is_stream_mode = {is_stream_mode}")
if is_stream_mode:
  df_silver_stage_01 = spark.readStream.table('bronze_exemploapidb.contato_eventos')
else:
  df_silver_stage_01 = spark.table('bronze_exemploapidb.contato_eventos')
  display(df_silver_stage_01)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Transformação dos dados

# COMMAND ----------

df_op = spark.createDataFrame([
  {'op': 'r', 'op_rank': 0},
  {'op': 'c', 'op_rank': 1},
  {'op': 'u', 'op_rank': 2},
  {'op': 'd', 'op_rank': 3},
])

if not is_stream_mode:
  display(df_op)

# COMMAND ----------

df_silver_stage_01.printSchema()

# COMMAND ----------

if not is_stream_mode:
  print("debug")
  display(
    df_silver_stage_01
      .alias('target')
      .join(df_op.alias('source'), F.col('target.payload.op') == F.col('source.op'), 'inner')
      .withColumn('silver_date', F.current_date()))

# COMMAND ----------

df_silver_stage_02 = (
  df_silver_stage_01
    .withColumn('op', F.col('payload.op'))
    .join(df_op, ['op'], 'inner') # join entre uma tabela estática com stream
    .withColumn('silver_date', F.current_date())
)
if not is_stream_mode:
  display(df_silver_stage_02)

# COMMAND ----------

df_silver_stage_03 = (
  df_silver_stage_02
    .withColumn('columns', F.when(F.col("payload.after").isNull(), F.col("payload.before")).otherwise(F.col("payload.after")))
    .withColumn('silver_date', F.from_utc_timestamp((F.col("payload.ts_ms") / F.lit(1000)).cast("timestamp"), "Brazil/East").cast('date'))
    .withColumn('ts_ms', F.from_utc_timestamp((F.col("payload.ts_ms") / F.lit(1000)).cast("timestamp"), "Brazil/East"))
    .select(
      F.col('transaction_date'),
      F.col('raw_date'),
      F.col('bronze_date'),
      F.col('silver_date'),
      F.col('ts_ms'),
      F.col('op'),
      F.col('op_rank'),
      F.col('columns.*'),
    )
    
)
if not is_stream_mode:
  display(df_silver_stage_03)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Gravação dos dados

# COMMAND ----------

print(f'localizacao_base_silver_tabela = {localizacao_base_silver_tabela}')

# COMMAND ----------

print('colunas: {}'.format([c for c in df_silver_stage_03.columns if 'op_rank' not in c]))

# COMMAND ----------

from delta.tables import *

delta_table = (
  DeltaTable.createIfNotExists(spark)
    .tableName('silver_exemploapidb.contato_eventos')
    .location(localizacao_base_silver_tabela)
    .addColumns(
      df_silver_stage_03
        .select([c for c in df_silver_stage_03.columns if 'op_rank' not in c])
        .schema
    )
    .execute()
)

if not is_stream_mode:
  display(delta_table.detail())

# COMMAND ----------

from pyspark.sql import Window
def build_rank(dataframe, key_columns, order_by):
  return (
    dataframe
      .select(
        F.col("*"), 
        F.row_number().over(Window.partitionBy(key_columns).orderBy(order_by)).alias("rank")
      )
      .filter(F.col("rank") == "1")
      .drop("rank")
    )

# COMMAND ----------

# debug
def debug():
  df_silver_stage_04 = (
    build_rank(df_silver_stage_03, ['id'], [F.col('ts_ms').desc(), F.col('op_rank').desc()])
    .drop('op_rank')
  )
  display(
    df_silver_stage_04
      .dropDuplicates()
      .orderBy('id', 'ts_ms')    
  )

# COMMAND ----------

debug()

# COMMAND ----------

def foreachBatchSilver(dataframe: DataFrame, batchId: int):
  df_silver_stage_04 = (
    build_rank(dataframe, ['id'], [F.col('ts_ms').desc(), F.col('op_rank').desc()])
    .drop('op_rank')
  )
  delta_table_silver_contato = DeltaTable.forName(spark, 'silver_exemploapidb.contato_eventos')
  (
    delta_table_silver_contato
    .alias('target')
    .merge(
      df_silver_stage_04.alias('source'),
      'target.id = source.id'
    )
    .whenMatchedDelete(f"source.op = 'd'") # remocao fisica
    .whenMatchedUpdateAll(f"source.op = 'u' and source.ts_ms >= target.ts_ms")
    .whenNotMatchedInsertAll(f"source.op <> 'd'")
    .execute()
  )

# COMMAND ----------

if is_stream_mode:
  query = (
    df_silver_stage_03
      .writeStream
      .format("console")
      .outputMode("append")
      .option("checkpointLocation", localizacao_base_silver_tabela_checkpoint)
      .foreachBatch(foreachBatchSilver)
      .start()
  )
  query.awaitTermination()
else:
  foreachBatchSilver(df_silver_stage_03, 0)

# COMMAND ----------

display(spark.table('silver_exemploapidb.contato_eventos'))

# COMMAND ----------

`[INFO]: FIM DO NOTEBOOK`
