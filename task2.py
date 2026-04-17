from pyspark.sql import SparkSession
from pyspark.sql.functions import col, substring, avg, round as spark_round

# Start Spark session
spark = SparkSession.builder \
    .appName("GSOD Task 2 - Average Annual Temperature") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Load CSV 
paths = [
    "data/2020/*",
    "data/2021/*",
    "data/2022/*"
]

df = spark.read.csv(paths, header=True, inferSchema=True)

print("\nOriginal Schema")
df.printSchema()

df_temp = df.select("STATION", "DATE", "TEMP")

print("\nSelected Columns Preview")
df_temp.show(5, truncate=False)

# Extract YEAR from DATE
df_temp = df_temp.withColumn("YEAR", substring(col("DATE").cast("string"), 1, 4).cast("int"))

# Remove missing temp values
df_temp_clean = df_temp.filter(
    col("TEMP").isNotNull() & (col("TEMP") != 9999.9)
)

print("\nCleaned Data Preview")
df_temp_clean.show(5, truncate=False)

# Average annual temp per station
df_avg = df_temp_clean.groupBy("STATION", "YEAR") \
    .agg(spark_round(avg("TEMP"), 2).alias("average_temperature")) \
    .orderBy("STATION", "YEAR")

print("\nAverage Annual Temperature by Station")
df_avg.show(50, truncate=False)

# Output count
output_count = df_avg.count()
print(f"\nTotal aggregated rows: {output_count}")

# Save output 
df_avg.coalesce(1).write.mode("overwrite").option("header", True).csv("output/task2_avg_temp")

print("\nOutput saved to: output/task2_avg_temp")

# Stop Spark
spark.stop()