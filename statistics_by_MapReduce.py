import os
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
total_rows =lines.map(lambda line:('line',1)).reduceByKey(lambda x,y: x+y)
total_rows_count = total_rows.take(1)[0][1]
column_list = np.array(sys.argv[2])
for i in range(column_list):
    column_name = lines.take(1)[0][i]
    sum = lines.map(lambda line:(column_name, line[i])).reduceByKey(lambda x,y: x+y)
    mean = sum.take(1)[0][1]/total_rows_count

    std_parts = lines.map(lambda line:(column_name, (line[i]-mean)**2)).reduceByKey(lambda x,y: x+y)
    std = (std_parts.take(1)[0][1]/(total_rows_count-1))**0.5
    output.append({'column_name': column_name, 'mean': mean, 'std': std})

output_df = pd.DataFrame.from_dict(output)
output_df.to_csv('{0}_statistics_output.csv'.format(file_name), index = False)
