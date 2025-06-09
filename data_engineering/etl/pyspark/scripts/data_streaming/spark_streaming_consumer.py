from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType, IntegerType

# Create Spark session
spark = SparkSession.builder \
    .appName("KafkaEventConsumer") \
    .master("local[*]") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Define schema for the JSON data
schema = StructType() \
    .add("user_id", IntegerType()) \
    .add("event", StringType()) \
    .add("timestamp", DoubleType())

# Read stream from Kafka topic 'user-events'
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "user-events") \
    .option("startingOffsets", "earliest") \
    .load()

# Convert Kafka value bytes to JSON
json_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Output to console
query = json_df.writeStream \
    .format("console") \
    .option("truncate", False) \
    .start()

query.awaitTermination()
