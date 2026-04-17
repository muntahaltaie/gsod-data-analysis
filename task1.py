from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, isnull, when, count

# Start Spark session
spark = SparkSession.builder \
    .appName("GSOD Task 1") \
    .getOrCreate()

# Read CSV  
paths = [
    "data/2020/*.csv",
    "data/2021/*.csv",
    "data/2022/*.csv"
]

df = spark.read.csv(paths, header=True, inferSchema=True)

print("\nFirst 5 Rows")
df.show(5, truncate=False)

# Print schema
print("\nSchema")
df.printSchema()

# Create YEAR column
df = df.withColumn("YEAR", year(col("DATE")))

# Count total records
total_records = df.count()
print(f"\nTotal records: {total_records}")

# Count unique stations
unique_stations = df.select("STATION").distinct().count()
print(f"Unique stations: {unique_stations}")

# Show years covered
print("\nYears Covered")
df.select("YEAR").distinct().orderBy("YEAR").show()


# Missing temp values
missing_temp_count = df.filter(
    (col("TEMP") == 9999.9) | col("TEMP").isNull()
).count()

print(f"Missing/invalid TEMP values: {missing_temp_count}")


# Missing precp. values
missing_prcp_count = df.filter(
    isnull(col("PRCP")) | (col("PRCP") == 99.99)
).count()

print(f"Missing/invalid PRCP values: {missing_prcp_count}")

# Summary stats
print("\nSummary Statistics")
df.select("TEMP", "MAX", "MIN", "PRCP").describe().show()

# Counts rows per year
print("\nRecord Count per Year")
df.groupBy("YEAR").count().orderBy("YEAR").show()

# Stops Spark
spark.stop()