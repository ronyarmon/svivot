import pyspark
from pyspark.sql.functions import mean, min, max, stddev
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from pyspark.sql import SparkSession, SQLContext, DataFrame

spark = SparkSession.builder.appName("ex1").getOrCreate()
sqlContext = SQLContext(sparkContext=spark.sparkContext, sparkSession=spark)

data = [(i, 'foo') for i in range(1000)]
columns = ['id', 'txt']
# specify schema
schema = StructType([StructField("id", IntegerType(), True), StructField("txt", StringType(), True)])
df1 = sqlContext.createDataFrame(data, schema) # Uses the schema specified
print(df1.printSchema())
df1.show(5)