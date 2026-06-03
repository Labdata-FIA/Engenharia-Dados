from pyspark.sql import SparkSession
import requests

spark = SparkSession.builder.appName('INGESTION').enableHiveSupport().getOrCreate()

r = requests.get('https://random-data-api.com/api/v2/users?size=100')
req = spark.read.json(spark.sparkContext.parallelize(r.json()))

req = req.select( \
 'email' \
,'first_name' \
,'last_name' \
,'gender' \
,'id' \
,'username' \
         )

req.repartition(1).write.parquet('s3a://camada-bronze/api/user',mode='append')
