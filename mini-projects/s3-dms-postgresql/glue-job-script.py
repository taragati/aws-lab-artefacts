import sys
from awsglue.context import GlueContext
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import SparkSession

# Initialize
args = getResolvedOptions(sys.argv, [])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# 📥 Read CSV from S3
df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load("s3://your-bucket/path/to/file.csv")

# Optionally show schema
df.printSchema()

# 🛢️ Write to Postgres
df.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://<your-rds-endpoint>:5432/<your-db>") \
    .option("dbtable", "your_table_name") \
    .option("user", "your_db_user") \
    .option("password", "your_db_password") \
    .option("driver", "org.postgresql.Driver") \
    .mode("append") \
    .save()