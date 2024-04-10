import pyspark
from pyspark.sql import SparkSession, SQLContext, DataFrame
spark = SparkSession.builder.appName("ex1").getOrCreate()
textFile = spark.read.text('age_salary.txt')
print(textFile.count())
print(textFile.first())
textFile.filter(textFile.value.contains('shira')).show()