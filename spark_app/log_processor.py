from pyspark.sql import SparkSession
from pyspark.sql.functions import window, col

spark = SparkSession.builder.appName("LogProcessor").getOrCreate()

schema = "ip STRING, identifier STRING, user STRING, timestamp STRING, method STRING, url STRING, protocol STRING, status INT, size STRING, referrer STRING, user_agent STRING"

logs = spark.readStream.schema(schema).csv("/app/logs")

logs = logs.withColumn("timestamp", col("timestamp").cast("timestamp"))

# Grouping by times interval and status codes
windowed_counts = logs.groupBy(
    window(logs.timestamp, "1 minute"),
    logs.status
).count()

# Output results to console
query = windowed_counts.writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query.awaitTermination()
