import sys
from pyspark.sql import Row
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("Python Spark SQL basic example").config("spark.some.config.option", "some-value").getOrCreate()
sc = spark.sparkContext
from csv import reader
import pandas as pd
import numpy as np
base = os.path.basename(sys.argv[1])
file_name = os.path.splitext(base)[0]
output = []
lines = sc.textFile(sys.argv[1], 1).mapPartitions(lambda x: reader(x))
column_count = len(lines.take(1)[0])
total_rows =lines.map(lambda line:('line',1)).reduceByKey(lambda x,y: x+y)
total_rows_count = total_rows.take(1)[0][1]
for i in range(column_count):
	column_name = lines.take(1)[0][i]
	unique_values = lines.map(lambda line:(line[i],1)).reduceByKey(lambda x,y: x+y).map(lambda x: ('unique',1)).reduceByKey(lambda x,y: x+y)
	unique_values_count = unique_values.take(1)[0][1]
	output.append({'column_name':column_name, 'uniqueness':unique_values_count/total_rows_count})

output_df = pd.DataFrame.from_dict(output)
output_df.to_csv({0}_output.csv)
