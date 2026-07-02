import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count

print("=" * 60)
print("DUBLIN BUS RELIABILITY BATCH PROCESSOR")
print("=" * 60)

spark = SparkSession.builder \
    .appName("Bus Reliability Batch Processing") \
    .getOrCreate()

print("\nReading processed JSON...")

df = spark.read.option("multiline", "true").json(
    "data/processed/processed_trip_updates.json"
)

print("\nSchema")
df.printSchema()

print("\nTotal Records :", df.count())

print("\nCalculating Route Statistics...")

result = df.groupBy("route_id").agg(
    avg("reliability_score").alias("average_score"),
    count("*").alias("total_trips")
)

print("\nResults")
result.show(20, False)

print("\nSaving Output...")

os.makedirs("data/batch-layer", exist_ok=True)

pdf = result.toPandas()

with open("data/batch-layer/batch_output.json", "w") as f:
    for _, row in pdf.iterrows():
        f.write(row.to_json())
        f.write("\n")

print("\nBatch Output saved successfully!")
print("\nBatch processing completed successfully!")

spark.stop()