import findspark
import pyspark
from pyspark.sql import SQLContext
import pandas as pd
def csv_to_spark(csvfile):
    # Pass in the SparkContext object `sc`
    sc = pyspark.SparkContext()
    sqlCtx = SQLContext(sc)
    df = sqlCtx.read.csv(csvfile)
    # Register the DataFrame df as a table.
    df.registerTempTable(csvfile)

def spark_to_pickle(df): 
    df = df.toPandas()
    df.to_pickle('df_course_final.pkl')