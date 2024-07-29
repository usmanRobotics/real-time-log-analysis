from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_extract, col, when, window, count, to_timestamp

spark = SparkSession.builder.appName("RealTimeLogAnalysis").getOrCreate()

log_file_path = "/app/logs/web_server_logs.csv"

schema = "IP STRING, Time STRING, Method STRING, URL STRING, Protocol STRING, Status STRING, UserAgent STRING"

logs = spark.readStream.schema(schema).csv(log_file_path)

# Extract required fields using regular expressions
logs = logs.withColumn('IP', regexp_extract('value', r'^(\S+)', 1)) \
    .withColumn('Time', regexp_extract('value', r'\[(.*?)\]', 1)) \
    .withColumn('Method', regexp_extract('value', r'\"(\S+)', 1)) \
    .withColumn('URL', regexp_extract('value', r'\"(?:\S+)\s(\S+)\s', 1)) \
    .withColumn('Status', regexp_extract('value', r'\s(\d{3})\s', 1)) \
    .withColumn('UserAgent', regexp_extract('value', r'\"[^\"]*\"[^\"]*\"(.*)\"$', 1))

#======
logs = logs.withColumn('Time', to_timestamp('Time', 'dd/MMM/yyyy:HH:mm:ss Z')) \
    .withColumn('Status', col('Status').cast('integer')) \
    .withColumn('Error', when(col('Status') >= 400, 1).otherwise(0))

aggregated_logs = logs.groupBy(window(col("Time"), "1 minute")) \
    .agg(count("IP").alias("TotalRequests"), 
         count(when(col("Error") == 1, True)).alias("TotalErrors"))

aggregated_logs = aggregated_logs.withColumn("ErrorRate", col("TotalErrors") / col("TotalRequests"))

query = aggregated_logs.writeStream.outputMode("complete").format("console").start()

query.awaitTermination()
