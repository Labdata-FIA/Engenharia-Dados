# Databricks notebook source
# MAGIC %md
# MAGIC ## Spark Streaming - Watermarking
# MAGIC
# MAGIC Documentação de referência: https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#handling-late-data-and-watermarking

# COMMAND ----------

spark

# COMMAND ----------

# MAGIC %md
# MAGIC ### Criar processo de streaming

# COMMAND ----------


# Ler os dados da fonte de taxa (rate source) - Gerando 1 linha por segundo
df = (
  spark
    .readStream
    .format("rate")
    .option("rowsPerSecond", 1)
    .load()
)

# COMMAND ----------

# MAGIC %md
# MAGIC Apresentando o comportamento do format: `rate` 

# COMMAND ----------

display(df)
# display(df, checkpointLocation="/Volumes/workspace/default/laboratorio-spark/exercicio.04.02/_checkpoint")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Aplicando processo de transformação 

# COMMAND ----------

import pyspark.sql.functions as F

# Simular eventos atrasados ao subtrair um intervalo aleatório do timestamp
df_atrasado = (
    df.withColumn("numero", F.floor(F.rand() * F.lit("3")))
      .withColumn(
        "timestamp_atrasado", 
        F.when(F.col("numero") == 0, F.col("timestamp") - F.expr("INTERVAL 1 MINUTE"))
         .when(F.col("numero") == 1, F.col("timestamp") - F.expr("INTERVAL 2 MINUTES"))
         .otherwise(F.col("timestamp") - F.expr("INTERVAL 3 MINUTES"))
    )
)

# Renomear a coluna 'value' para 'vendas'
df_atrasado = (
    df_atrasado
#        .withColumnRenamed("value", "vendas")
        .withColumn("vendas", F.lit("1"))
)

# Adicionar uma marcação para eventos atrasados (mas aceitos pelo watermark)
df_atrasado = df_atrasado.withColumn(
    "atrasado",
    F.when(F.col("timestamp_atrasado") < F.current_timestamp(), "Sim").otherwise("Não")
)

# Configurar o Watermark para processar eventos atrasados até 2 minutos
df_agrupado = (
    df_atrasado
        .withWatermark("timestamp_atrasado", "2 minutes")
        .groupBy(F.window("timestamp_atrasado", "1 minute"), "atrasado")
        .agg(F.sum("vendas").alias("total_vendas"))
)

# COMMAND ----------

# Exibir os resultados no console
query = (
    df_agrupado.writeStream
        .outputMode("append")
        .format("console")
        .start()
)
query.awaitTermination()

# COMMAND ----------

# display(df_agrupado)
display(df, checkpointLocation="/Volumes/workspace/default/laboratorio-spark/exercicio.04.02/_checkpoint")

# COMMAND ----------


