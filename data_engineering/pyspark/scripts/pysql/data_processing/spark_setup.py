## 1. PySpark Fundamentals

### Basic Setup and Configuration
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf


def create_spark_session(app_name="PySpark_Interview_Prep"):
    """
    Create optimized Spark session for interview scenarios
    """
    conf = SparkConf() \
        .setAppName(app_name) \
        .set("spark.sql.adaptive.enabled", "true") \
        .set("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .set("spark.sql.adaptive.skewJoin.enabled", "true") \
        .set("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
        .set("spark.sql.execution.arrow.pyspark.enabled", "true")

    spark = SparkSession.builder.config(conf=conf).getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    return spark


# Usage example
spark = create_spark_session()
print(f"Spark Version: {spark.version}")
print(f"Available cores: {spark.sparkContext.defaultParallelism}")


### RDD Fundamentals
# rdd_operations.py
from pyspark import SparkContext


def rdd_examples(spark):
    """
    Comprehensive RDD operations for interviews
    """
    sc = spark.sparkContext

    # Creating RDDs
    numbers_rdd = sc.parallelize([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    text_rdd = sc.textFile("sample_data/input.txt")

    # Transformations (Lazy)
    even_numbers = numbers_rdd.filter(lambda x: x % 2 == 0)
    squared_numbers = numbers_rdd.map(lambda x: x ** 2)
    word_counts = text_rdd.flatMap(lambda line: line.split()) \
        .map(lambda word: (word.lower(), 1)) \
        .reduceByKey(lambda a, b: a + b)

    # Actions (Eager)
    total_sum = numbers_rdd.reduce(lambda a, b: a + b)
    first_five = numbers_rdd.take(5)
    collected_data = even_numbers.collect()

    # Advanced operations
    paired_rdd = numbers_rdd.map(lambda x: (x % 3, x))
    grouped_data = paired_rdd.groupByKey().mapValues(list)

    return {
        'sum': total_sum,
        'first_five': first_five,
        'even_numbers': collected_data,
        'word_counts': word_counts.take(10),
        'grouped': grouped_data.collect()
    }