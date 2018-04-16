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

data_path = sys.argv[1]
with open(data_path, encoding='utf-8') as data_file:
    data = json.loads(data_file.read())
col =[]
r = data['meta']['view']['columns']
for i in range(0,len(r)):
    col.append(r[i]['name'])
d = data['data']
df = pd.DataFrame(d,columns=col)

a = []
b = []
c = []
for x in df:
# all the columns that have unique values and do not contain null
    if (len(df[x].unique())==len(df[x]) and df[x].isnull().any() == False):
        a.append(x)
# columns that are unique disregarding unique values
    if (len(df[x].unique())==len(df[x])):
        b.append(x)
# % of unique values (if very low can still be considered candidate keys)
    c.append([x, float("{0:.2f}".format(len(df[x].unique())/len(df[x])))])
keys = sc.parallelize(a)
keys.saveAsTextFile('keys.txt')
dirty_keys = sc.parallelize(b)
dirty_keys.saveAsTextFile('dirty_keys.txt')
how_unique = sc.parallelize(c)
how_unique.saveAsTextFile('how_unique.txt')
