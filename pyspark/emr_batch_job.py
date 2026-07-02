from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg

spark = SparkSession.builder \
    .appName("Bus Reliability Batch Processing") \
    .getOrCreate()

# Read JSON files from S3
df = spark.read.json("s3://bus-reliability-data-vg/")

print("=" * 60)
print("TOTAL RECORDS")
print("=" * 60)
print(df.count())

# Reliability statistics
summary = (
    df.groupBy("reliability")
      .agg(
          count("*").alias("total_trips"),
          avg("number_of_stop_updates").alias("avg_stop_updates")
      )
)

summary.show()

# Save processed results back to S3
summary.write.mode("overwrite").json(
    "s3://bus-reliability-data-vg/batch-output/"
)

print("Batch processing completed successfully.")

spark.stop()