from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, year as spark_year, avg, stddev, min as spark_min,
    max as spark_max, count
)
import os

spark = SparkSession.builder \
    .appName("Task4-DataPrep") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Load raw GSOD data (same as task2) 
# Reads all CSVs recursively from data/2020/, data/2021/, data/2022/
data_path = "data/*/*"
df = spark.read.option("recursiveFileLookup", "true") \
               .csv(data_path, header=True, inferSchema=True)

# Filter valid temps (GSOD uses 9999.9 as missing)
df = df.filter((col("TEMP").isNotNull()) & (col("TEMP") < 9999.0))
df = df.withColumn("YEAR", spark_year(col("DATE")))

#  Aggregate: avg, std dev, min, max, record count per station per year 
stats = df.groupBy("STATION", "YEAR").agg(
    avg("TEMP").alias("avg_temp"),
    stddev("TEMP").alias("std_temp"),
    spark_min("TEMP").alias("min_temp"),
    spark_max("TEMP").alias("max_temp"),
    count("TEMP").alias("record_count")
)

# Attach station metadata (NAME, LAT, LON) and take first occurrence
meta = df.groupBy("STATION").agg(
    avg("LATITUDE").alias("latitude"),
    avg("LONGITUDE").alias("longitude")
)

# NAME can vary slightly, just grab the first one
from pyspark.sql.functions import first
meta_name = df.groupBy("STATION").agg(first("NAME", ignorenulls=True).alias("name"))
meta = meta.join(meta_name, on="STATION", how="left")

result = stats.join(meta, on="STATION", how="left")
result = result.orderBy("STATION", "YEAR")

# Save as single CSV 
out_path = "output/task4_climate_stats"
result.coalesce(1).write.csv(out_path, header=True, mode="overwrite")

print(f"\nData saved to {out_path}")
print(f"   Total rows: {result.count()}")
result.show(10, truncate=False)

spark.stop()