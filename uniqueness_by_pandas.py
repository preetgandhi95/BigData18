import sys
import pandas as pd
import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql.functions import *
import json
spark = SparkSession.builder.appName("Python Spark SQL basic example").config("spark.some.config.option", "some-value").getOrCreate()
from pyspark.sql import Row
sc = spark.sparkContext
threshold = 
input_list = 
for i in input_list : 
    data_path = i
    base = os.path.basename(data_path)
    file_name = os.path.splitext(base)[0]
    df = pd.read_csv(data_path)

    u = []
    for x in df:
        u.append({'key':x, 'u_index': float("{0:.2f}".format(len(df[x].unique())/len(df[x]))), 'dataset': file_name})

    uniqueness = pd.DataFrame.from_dict(u)
    uniqueness = uniqueness[uniqueness['u_index']>=threshold]
    uniqueness.to_csv('{0}_output.csv'.format(file_name),index = False)
