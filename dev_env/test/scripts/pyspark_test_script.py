import os, getpass
from pyspark.sql.types import (StructField, StructType, StringType, IntegerType)
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("ex1").getOrCreate()
data_dir = os.path.join('/home', getpass.getuser(), 'data')

## From tuples array
data = [(i, 'foo') for i in range(1000)]
columns = ['id', 'txt']
# Infer schema
df = spark.createDataFrame(data, columns)
df.show(10)

# From CSV File
file_name = 'AAPL.csv'
df = spark.read.csv(os.path.join(data_dir, file_name), header=True, inferSchema=True)
print('From CSV: appl_stock')
df.show(10)
