import os, getpass
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("ex1").getOrCreate()
df = spark.read.csv('AAPL.csv', header=True, inferSchema=True)
print('From CSV: appl_stock')
df.show(10)
