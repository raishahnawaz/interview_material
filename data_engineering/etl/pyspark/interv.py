# PySpark Interview Preparation - Complete Guide

## Project Structure
```
pyspark - interview - prep /
├── README.md
├── requirements.txt
├── docker /
│   ├── Dockerfile
│   └── docker - compose.yml
├── scripts /
│   ├── data_processing /
│   ├── transformations /
│   ├── performance /
│   └── advanced /
├── deployment /
│   ├── aws /
│   ├── gcp /
│   └── azure /
└── sample_data /
```





## 2. DataFrame Operations

### DataFrame Creation and Basic Operations
```python
# dataframe_basics.py
from pyspark.sql import DataFrame
from pyspark.sql.types import *
from pyspark.sql.functions import *


def dataframe_operations(spark):
    """
    Essential DataFrame operations for interviews
    """
    # Define schema
    schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("age", IntegerType(), True),
        StructField("salary", DoubleType(), True),
        StructField("department", StringType(), True),
        StructField("join_date", DateType(), True)
    ])

    # Sample data
    data = [
        (1, "John Doe", 30, 50000.0, "Engineering", "2020-01-15"),
        (2, "Jane Smith", 25, 45000.0, "Marketing", "2021-03-20"),
        (3, "Bob Johnson", 35, 60000.0, "Engineering", "2019-06-10"),
        (4, "Alice Williams", 28, 48000.0, "HR", "2020-11-05"),
        (5, "Charlie Brown", 32, 55000.0, "Engineering", "2018-09-30")
    ]

    # Create DataFrame
    df = spark.createDataFrame(data, schema)

    # Basic operations
    df.show()
    df.printSchema()
    df.describe().show()

    # Column operations
    df_with_bonus = df.withColumn("bonus", col("salary") * 0.1)
    df_renamed = df.withColumnRenamed("name", "employee_name")
    df_filtered = df.filter(col("age") > 30)
    df_selected = df.select("name", "department", "salary")

    # Aggregations
    dept_stats = df.groupBy("department") \
        .agg(
        count("*").alias("employee_count"),
        avg("salary").alias("avg_salary"),
        max("salary").alias("max_salary"),
        min("age").alias("min_age")
    )

    return df, df_with_bonus, dept_stats


```

### Advanced DataFrame Transformations
```python
# advanced_dataframe.py
from pyspark.sql.window import Window


def advanced_dataframe_operations(spark):
    """
    Advanced DataFrame operations commonly asked in interviews
    """
    # Window functions
    df = spark.table("employees")  # Assuming table exists

    # Ranking functions
    window_spec = Window.partitionBy("department").orderBy(desc("salary"))
    df_with_rank = df.withColumn("rank", rank().over(window_spec)) \
        .withColumn("dense_rank", dense_rank().over(window_spec)) \
        .withColumn("row_number", row_number().over(window_spec))

    # Lag/Lead functions
    df_with_lag = df_with_rank.withColumn(
        "prev_salary",
        lag("salary", 1).over(window_spec)
    ).withColumn(
        "next_salary",
        lead("salary", 1).over(window_spec)
    )

    # Cumulative operations
    df_cumulative = df_with_lag.withColumn(
        "running_total",
        sum("salary").over(Window.partitionBy("department")
                           .orderBy("join_date")
                           .rowsBetween(Window.unboundedPreceding, Window.currentRow))
    )

    # Pivot operations
    pivot_df = df.groupBy("department").pivot("year").sum("salary")

    return df_with_rank, df_cumulative, pivot_df


```

---

## 3. SQL Operations

### Complex SQL Queries
```python


# sql_operations.py

def sql_query_examples(spark):
    """
    Common SQL patterns asked in PySpark interviews
    """
    # Register temporary view
    df.createOrReplaceTempView("employees")

    # Complex joins
    join_query = """
    SELECT e1.name as employee, e2.name as manager, e1.salary
    FROM employees e1
    LEFT JOIN employees e2 ON e1.manager_id = e2.id
    WHERE e1.salary > (
        SELECT AVG(salary) 
        FROM employees e3 
        WHERE e3.department = e1.department
    )
    """

    # Window functions in SQL
    window_query = """
    SELECT 
        name,
        department,
        salary,
        RANK() OVER (PARTITION BY department ORDER BY salary DESC) as salary_rank,
        LAG(salary) OVER (PARTITION BY department ORDER BY join_date) as prev_salary,
        salary - LAG(salary) OVER (PARTITION BY department ORDER BY join_date) as salary_diff
    FROM employees
    """

    # CTEs and complex aggregations
    cte_query = """
    WITH dept_stats AS (
        SELECT 
            department,
            AVG(salary) as avg_salary,
            COUNT(*) as emp_count
        FROM employees
        GROUP BY department
    ),
    high_performers AS (
        SELECT e.*, ds.avg_salary
        FROM employees e
        INNER JOIN dept_stats ds ON e.department = ds.department
        WHERE e.salary > ds.avg_salary * 1.2
    )
    SELECT * FROM high_performers
    ORDER BY department, salary DESC
    """

    results = {
        'joins': spark.sql(join_query),
        'windows': spark.sql(window_query),
        'cte': spark.sql(cte_query)
    }

    return results


```

---

## 4. Performance Optimization

### Partitioning and Bucketing
```python


# performance_optimization.py

def partitioning_examples(spark):
    """
    Partitioning strategies for optimal performance
    """
    df = spark.table("large_dataset")

    # Check current partitioning
    print(f"Current partitions: {df.rdd.getNumPartitions()}")

    # Repartitioning strategies
    # Hash partitioning
    df_repartitioned = df.repartition(200, "department")

    # Range partitioning (for ordered data)
    df_range_partitioned = df.repartitionByRange(100, "salary")

    # Coalesce for reducing partitions
    df_coalesced = df.coalesce(50)

    # Custom partitioning
    def custom_partitioner(key):
        if key == "Engineering":
            return 0
        elif key == "Marketing":
            return 1
        else:
            return 2

    # Bucketing for joins
    df.write \
        .option("path", "output/bucketed_data") \
        .bucketBy(10, "department") \
        .sortBy("salary") \
        .saveAsTable("bucketed_employees")

    return df_repartitioned, df_coalesced


def caching_strategies(spark):
    """
    Efficient caching strategies
    """
    df = spark.table("large_dataset")

    # Different storage levels
    from pyspark import StorageLevel

    # Memory only (default)
    df.cache()  # Same as df.persist(StorageLevel.MEMORY_ONLY)

    # Memory and disk
    df.persist(StorageLevel.MEMORY_AND_DISK)

    # Serialized caching for memory efficiency
    df.persist(StorageLevel.MEMORY_ONLY_SER)

    # Off-heap storage
    df.persist(StorageLevel.OFF_HEAP)

    # Check if cached
    print(f"Is cached: {df.is_cached}")

    # Unpersist when done
    df.unpersist()

    return df


```

### Join Optimization
```python


# join_optimization.py

def join_optimization_techniques(spark):
    """
    Join optimization strategies for interviews
    """
    large_df = spark.table("large_table")
    small_df = spark.table("small_table")

    # Broadcast join for small tables
    from pyspark.sql.functions import broadcast

    broadcast_join = large_df.join(
        broadcast(small_df),
        "join_key",
        "inner"
    )

    # Bucket join (both tables bucketed on join key)
    bucket_join = spark.sql("""
        SELECT /*+ BUCKET */ l.*, s.*
        FROM large_bucketed l
        JOIN small_bucketed s ON l.key = s.key
    """)

    # Sort-Merge join optimization
    # Pre-sort data by join keys
    large_sorted = large_df.sort("join_key")
    small_sorted = small_df.sort("join_key")

    sort_merge_join = large_sorted.join(small_sorted, "join_key")

    # Salted join for skewed data
    def salted_join(large_df, small_df, join_key, salt_range=100):
        # Add salt to both dataframes
        large_salted = large_df.withColumn(
            "salt",
            (rand() * salt_range).cast("int")
        ).withColumn(
            "salted_key",
            concat(col(join_key), lit("_"), col("salt"))
        )

        small_exploded = small_df.withColumn(
            "salt",
            explode(array([lit(i) for i in range(salt_range)]))
        ).withColumn(
            "salted_key",
            concat(col(join_key), lit("_"), col("salt"))
        )

        return large_salted.join(small_exploded, "salted_key").drop("salt", "salted_key")

    return broadcast_join, sort_merge_join


```

---

## 5. Streaming Processing

### Structured Streaming
```python
# streaming_processing.py
from pyspark.sql.streaming import StreamingQuery


def streaming_examples(spark):
    """
    Structured Streaming examples for real-time processing
    """
    # Read from Kafka
    kafka_stream = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "input-topic") \
        .load()

    # Parse JSON data
    parsed_stream = kafka_stream.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")

    # Windowed aggregations
    windowed_counts = parsed_stream \
        .withWatermark("timestamp", "10 minutes") \
        .groupBy(
        window(col("timestamp"), "5 minutes", "1 minute"),
        col("category")
    ) \
        .count()

    # Output to multiple sinks
    console_query = windowed_counts.writeStream \
        .outputMode("update") \
        .format("console") \
        .trigger(processingTime="30 seconds") \
        .start()

    kafka_output = windowed_counts.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("topic", "output-topic") \
        .option("checkpointLocation", "checkpoint/kafka-output") \
        .start()

    return console_query, kafka_output


def stateful_streaming(spark):
    """
    Stateful operations in streaming
    """

    # Arbitrary stateful operations
    def update_state(key, values, state):
        # Custom state logic
        current_count = state.get() or 0
        new_count = current_count + len(values)
        state.update(new_count)
        return new_count

    stateful_stream = parsed_stream \
        .groupByKey(lambda x: x.key) \
        .mapGroupsWithState(
        update_state,
        outputMode="update",
        timeoutConf=GroupStateTimeout.ProcessingTimeTimeout
    )

    return stateful_stream


```

---

## 6. Data Sources and Formats

### File Format Operations
```python


# data_sources.py

def file_format_operations(spark):
    """
    Working with different file formats
    """
    # Parquet operations
    parquet_df = spark.read.parquet("data/employees.parquet")
    parquet_df.write \
        .mode("overwrite") \
        .option("compression", "snappy") \
        .partitionBy("department") \
        .parquet("output/partitioned_employees")

    # Delta Lake operations
    delta_df = spark.read.format("delta").load("data/delta-table")
    delta_df.write \
        .format("delta") \
        .mode("overwrite") \
        .option("overwriteSchema", "true") \
        .save("output/delta-employees")

    # JSON operations with schema inference
    json_df = spark.read \
        .option("multiline", "true") \
        .option("inferSchema", "true") \
        .json("data/employees.json")

    # CSV with custom options
    csv_df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .option("dateFormat", "yyyy-MM-dd") \
        .option("timestampFormat", "yyyy-MM-dd HH:mm:ss") \
        .csv("data/employees.csv")

    # Avro format
    avro_df = spark.read.format("avro").load("data/employees.avro")

    return parquet_df, delta_df, json_df


def database_operations(spark):
    """
    Database connectivity examples
    """
    # JDBC connections
    jdbc_df = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://localhost:5432/company") \
        .option("dbtable", "employees") \
        .option("user", "username") \
        .option("password", "password") \
        .option("driver", "org.postgresql.Driver") \
        .load()

    # Optimized JDBC reads
    partitioned_jdbc = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://localhost:5432/company") \
        .option("dbtable", "employees") \
        .option("partitionColumn", "id") \
        .option("lowerBound", "1") \
        .option("upperBound", "100000") \
        .option("numPartitions", "10") \
        .load()

    return jdbc_df, partitioned_jdbc


```

---

## 7. UDFs and Custom Functions

### User Defined Functions
```python
# udfs_and_custom_functions.py
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType, IntegerType
import re


def udf_examples(spark):
    """
    User-defined function examples
    """

    # Simple UDF
    def categorize_age(age):
        if age < 25:
            return "Young"
        elif age < 40:
            return "Middle"
        else:
            return "Senior"

    age_category_udf = udf(categorize_age, StringType())

    # Complex UDF with regex
    def extract_domain(email):
        if email:
            match = re.search(r'@([^.]+\.[^.]+)', email)
            return match.group(1) if match else "unknown"
        return "unknown"

    domain_udf = udf(extract_domain, StringType())

    # Vectorized UDF (Pandas UDF)
    from pyspark.sql.functions import pandas_udf
    import pandas as pd

    @pandas_udf(returnType=StringType())
    def vectorized_categorize_age(ages: pd.Series) -> pd.Series:
        return ages.apply(lambda age:
                          "Young" if age < 25 else
                          "Middle" if age < 40 else
                          "Senior"
                          )

    # Usage
    df = spark.table("employees")
    df_with_categories = df.withColumn("age_category", age_category_udf("age")) \
        .withColumn("email_domain", domain_udf("email")) \
        .withColumn("age_cat_vectorized", vectorized_categorize_age("age"))

    return df_with_categories


def custom_aggregation_functions(spark):
    """
    Custom aggregation functions using UDAF
    """
    from pyspark.sql.functions import UserDefinedAggregateFunction
    from pyspark.sql.types import DoubleType, StructType, StructField, LongType

    class GeometricMean(UserDefinedAggregateFunction):
        def inputSchema(self):
            return StructType([StructField("value", DoubleType())])

        def bufferSchema(self):
            return StructType([
                StructField("product", DoubleType()),
                StructField("count", LongType())
            ])

        def dataType(self):
            return DoubleType()

        def deterministic(self):
            return True

        def initialize(self, buffer):
            buffer[0] = 1.0  # product
            buffer[1] = 0  # count

        def update(self, buffer, input):
            if input[0] is not None:
                buffer[0] *= input[0]
                buffer[1] += 1

        def merge(self, buffer1, buffer2):
            buffer1[0] *= buffer2[0]
            buffer1[1] += buffer2[1]

        def evaluate(self, buffer):
            if buffer[1] == 0:
                return None
            return buffer[0] ** (1.0 / buffer[1])

    geometric_mean = GeometricMean()

    # Usage
    df = spark.table("sales")
    result = df.select(geometric_mean("price").alias("geometric_mean_price"))

    return result


```

---

## 8. Testing and Debugging

### Unit Testing Framework
```python
# testing_framework.py
import unittest
from pyspark.sql import SparkSession
from pyspark.sql.types import *


class PySparkTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spark = SparkSession.builder \
            .appName("PySparkTesting") \
            .master("local[2]") \
            .getOrCreate()
        cls.spark.sparkContext.setLogLevel("ERROR")

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

    def test_data_transformation(self):
        # Sample test data
        data = [(1, "John", 30), (2, "Jane", 25), (3, "Bob", 35)]
        schema = StructType([
            StructField("id", IntegerType(), True),
            StructField("name", StringType(), True),
            StructField("age", IntegerType(), True)
        ])

        df = self.spark.createDataFrame(data, schema)

        # Test transformation
        result_df = df.filter(col("age") > 25)
        result_count = result_df.count()

        self.assertEqual(result_count, 2)

        # Test data quality
        self.assertIsNone(result_df.filter(col("name").isNull()).first())

    def test_aggregation_logic(self):
        # Test custom aggregation logic
        data = [("A", 10), ("B", 20), ("A", 15), ("B", 25)]
        df = self.spark.createDataFrame(data, ["category", "value"])

        result = df.groupBy("category").sum("value").collect()
        result_dict = {row.category: row['sum(value)'] for row in result}

        expected = {"A": 25, "B": 45}
        self.assertEqual(result_dict, expected)


def debugging_techniques(spark):
    """
    Common debugging techniques for PySpark
    """
    df = spark.table("large_dataset")

    # Explain query plan
    df.explain(True)  # Extended explain

    # Sample data for debugging
    sample_df = df.sample(0.01, seed=42)

    # Check data skew
    partition_counts = df.rdd.mapPartitions(lambda x: [sum(1 for _ in x)]).collect()
    print(f"Partition distribution: {partition_counts}")

    # Monitor Spark UI programmatically
    sc = spark.sparkContext
    print(f"Application ID: {sc.applicationId}")
    print(f"Spark UI URL: {sc.uiWebUrl}")

    return sample_df, partition_counts


```

---

## 9. Cloud Deployment Scripts

### AWS EMR Deployment
```python


# aws_deployment.py

def create_emr_cluster():
    """
    AWS EMR cluster creation script
    """
    import boto3

    emr_client = boto3.client('emr', region_name='us-west-2')

    cluster_config = {
        'Name': 'PySpark-Interview-Cluster',
        'ReleaseLabel': 'emr-6.13.0',
        'Applications': [
            {'Name': 'Spark'},
            {'Name': 'Hadoop'},
            {'Name': 'Hive'}
        ],
        'Instances': {
            'InstanceGroups': [
                {
                    'Name': 'Master',
                    'Market': 'ON_DEMAND',
                    'InstanceRole': 'MASTER',
                    'InstanceType': 'm5.xlarge',
                    'InstanceCount': 1
                },
                {
                    'Name': 'Workers',
                    'Market': 'SPOT',
                    'InstanceRole': 'CORE',
                    'InstanceType': 'm5.xlarge',
                    'InstanceCount': 2,
                    'BidPrice': '0.20'
                }
            ],
            'Ec2KeyName': 'your-key-pair',
            'KeepJobFlowAliveWhenNoSteps': True,
            'TerminationProtected': False,
            'Ec2SubnetId': 'subnet-xxxxxxxx'
        },
        'ServiceRole': 'EMR_DefaultRole',
        'JobFlowRole': 'EMR_EC2_DefaultRole',
        'BootstrapActions': [
            {
                'Name': 'Install Additional Packages',
                'ScriptBootstrapAction': {
                    'Path': 's3://your-bucket/bootstrap-script.sh'
                }
            }
        ],
        'Configurations': [
            {
                'Classification': 'spark-defaults',
                'Properties': {
                    'spark.sql.adaptive.enabled': 'true',
                    'spark.sql.adaptive.coalescePartitions.enabled': 'true',
                    'spark.sql.adaptive.skewJoin.enabled': 'true'
                }
            }
        ]
    }

    response = emr_client.run_job_flow(**cluster_config)
    return response['JobFlowId']


# Spark job submission
def submit_spark_job(cluster_id, s3_script_path):
    """
    Submit PySpark job to EMR cluster
    """
    emr_client = boto3.client('emr', region_name='us-west-2')

    step_config = {
        'Name': 'PySpark Data Processing',
        'ActionOnFailure': 'CONTINUE',
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': [
                'spark-submit',
                '--deploy-mode', 'cluster',
                '--master', 'yarn',
                '--conf', 'spark.sql.adaptive.enabled=true',
                s3_script_path
            ]
        }
    }

    response = emr_client.add_job_flow_steps(
        JobFlowId=cluster_id,
        Steps=[step_config]
    )

    return response['StepIds'][0]


```

### GCP Dataproc Deployment
```python


# gcp_deployment.py

def create_dataproc_cluster():
    """
    GCP Dataproc cluster creation
    """
    from google.cloud import dataproc_v1

    client = dataproc_v1.ClusterControllerClient()
    project_id = "your-project-id"
    region = "us-central1"
    cluster_name = "pyspark-interview-cluster"

    cluster_config = {
        "project_id": project_id,
        "cluster_name": cluster_name,
        "config": {
            "master_config": {
                "num_instances": 1,
                "machine_type_uri": "n1-standard-4",
                "disk_config": {"boot_disk_type": "pd-standard", "boot_disk_size_gb": 100}
            },
            "worker_config": {
                "num_instances": 2,
                "machine_type_uri": "n1-standard-4",
                "disk_config": {"boot_disk_type": "pd-standard", "boot_disk_size_gb": 100},
                "preemptibility": dataproc_v1.Instance.Preemptibility.PREEMPTIBLE
            },
            "software_config": {
                "image_version": "2.0-debian10",
                "properties": {
                    "spark:spark.sql.adaptive.enabled": "true",
                    "spark:spark.sql.adaptive.coalescePartitions.enabled": "true"
                }
            },
            "initialization_actions": [
                {
                    "executable_file": "gs://your-bucket/init-script.sh",
                    "execution_timeout": {"seconds": 300}
                }
            ]
        }
    }

    operation = client.create_cluster(
        request={
            "project_id": project_id,
            "region": region,
            "cluster": cluster_config
        }
    )

    return operation.result()


def submit_dataproc_job(project_id, region, cluster_name, gcs_script_path):
    """
    Submit PySpark job to Dataproc
    """
    from google.cloud import dataproc_v1

    job_client = dataproc_v1.JobControllerClient()

    job = {
        "placement": {"cluster_name": cluster_name},
        "pyspark_job": {
            "main_python_file_uri": gcs_script_path,
            "properties": {
                "spark.sql.adaptive.enabled": "true",
                "spark.sql.adaptive.coalescePartitions.enabled": "true"
            }
        }
    }

    operation = job_client.submit_job_as_operation(
        request={
            "project_id": project_id,
            "region": region,
            "job": job
        }
    )

    return operation.result()


```

---

## 10. Docker Configuration

### Dockerfile
```dockerfile
# Dockerfile
FROM
openjdk: 8 - jdk - slim

# Install Python and system dependencies
RUN
apt - get
update & & apt - get
install - y \
    python3 \
    python3 - pip \
    python3 - dev \
    wget \
    curl \
    & & rm - rf / var / lib / apt / lists / *

# Set environment variables
ENV
SPARK_VERSION = 3.4
.0
ENV
HADOOP_VERSION = 3
ENV
SPARK_HOME = / opt / spark
ENV
PATH =$PATH:$SPARK_HOME / bin:$SPARK_HOME / sbin
ENV
PYTHONPATH =$SPARK_HOME / python:$SPARK_HOME / python / lib / py4j - 0.10
.9
.5 - src.zip

# Download and install Spark
RUN
wget - O
spark.tgz
"https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" \
& & tar - xzf
spark.tgz - C / opt / \
& & mv / opt / spark -${SPARK_VERSION} - bin - hadoop${HADOOP_VERSION} $SPARK_HOME \
                                                                        & & rm
spark.tgz

# Install Python dependencies
COPY
requirements.txt / tmp / requirements.txt
RUN
pip3
install - r / tmp / requirements.txt

# Create workspace directory
WORKDIR / workspace

# Copy project files
COPY. / workspace /

# Expose Spark UI and Jupyter ports
EXPOSE
4040
8080
8888

# Default command
CMD["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
```

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
spark - master:
build:.
container_name: spark - master
hostname: spark - master
ports:
- "8080:8080"
- "7077:7077"
- "4040:4040"
- "8888:8888"
volumes:
-./ data: / workspace / data
-./ scripts: / workspace / scripts
environment:
- SPARK_MODE = master
- SPARK_MASTER_HOST = spark - master
- SPARK_MASTER_PORT = 7077
command: >
bash - c
"
/ opt / spark / sbin / start - master.sh & &
jupyter
notebook - -ip = 0.0
.0
.0 - -port = 8888 - -no - browser - -allow - root
"

spark - worker - 1:
build:.
container_name: spark - worker - 1
hostname: spark - worker - 1
depends_on:
- spark - master
ports:
- "8081:8081"
volumes:
-./ data: / workspace / data
-./ scripts: / workspace / scripts
environment:
- SPARK_MODE = worker
- SPARK_MASTER_URL = spark: // spark - master: 7077
- SPARK_WORKER_CORES = 2
- SPARK_WORKER_MEMORY = 2
g
command: / opt / spark / sbin / start - worker.sh
spark: // spark - master: 7077

spark - worker - 2:
build:.
container_name: spark - worker - 2
hostname: spark - worker - 2
depends_on:
- spark - master
ports:
- "8082:8081"
volumes:
-./ data: / workspace / data
-./ scripts: / workspace / scripts
environment:
- SPARK_MODE = worker
- SPARK_MASTER_URL = spark: // spark - master: 7077
- SPARK_WORKER_CORES = 2
- SPARK_WORKER_MEMORY = 2
g
command: / opt / spark / sbin / start - worker.sh
spark: // spark - master: 7077

zookeeper:
image: confluentinc / cp - zookeeper:7.4
.0
container_name: zookeeper
ports:
- "2181:2181"
environment:
ZOOKEEPER_CLIENT_PORT: 2181
ZOOKEEPER_TICK_TIME: 2000

kafka:
image: confluentinc / cp - kafka:7.4
.0
container_name: kafka
depends_on:
- zookeeper
ports:
- "9092:9092"
environment:
KAFKA_BROKER_ID: 1
KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
KAFKA_ADVERTISED_LISTENERS: PLAINTEXT: // localhost: 9092
KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
```

---

## 11. Real-World Data Processing Examples

### ETL Pipeline Implementation
```python
# etl_pipeline.py
from pyspark.sql.functions import *
from pyspark.sql.types import *
import logging


class ETLPipeline:
    def __init__(self, spark_session):
        self.spark = spark_session
        self.logger = logging.getLogger(__name__)

    def extract_data(self, source_config):
        """
        Extract data from multiple sources
        """
        extracted_data = {}

        for source_name, config in source_config.items():
            try:
                if config['type'] == 'jdbc':
                    df = self.spark.read \
                        .format("jdbc") \
                        .options(**config['options']) \
                        .load()
                elif config['type'] == 'parquet':
                    df = self.spark.read.parquet(config['path'])
                elif config['type'] == 'json':
                    df = self.spark.read.json(config['path'])
                elif config['type'] == 'kafka':
                    df = self.spark \
                        .readStream \
                        .format("kafka") \
                        .options(**config['options']) \
                        .load()

                extracted_data[source_name] = df
                self.logger.info(f"Successfully extracted data from {source_name}")

            except Exception as e:
                self.logger.error(f"Failed to extract data from {source_name}: {str(e)}")
                raise

        return extracted_data

    def transform_data(self, raw_data):
        """
        Complex data transformations
        """
        # Customer data cleaning and enrichment
        customers_df = raw_data['customers']

        # Data quality checks
        customers_clean = customers_df \
            .filter(col("customer_id").isNotNull()) \
            .filter(col("email").rlike(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})) \
            .withColumn("phone", regexp_replace(col("phone"), r'[ ^\d]', '')) \
            .filter(length(col("phone")) == 10)

        # Feature engineering
        customers_enriched = customers_clean \
            .withColumn("age_group",
                        when(col("age") < 25, "Young")
                        .when(col("age") < 40, "Middle")
                        .otherwise("Senior")
                        ) \
            .withColumn("email_domain",
                        regexp_extract(col("email"), r'@(.+)', 1)
                        ) \
            .withColumn("customer_lifetime_months",
                        months_between(current_date(), col("registration_date"))
                        )

        # Orders data with business logic
        orders_df = raw_data['orders']

        orders_processed = orders_df \
            .withColumn("order_year", year(col("order_date"))) \
            .withColumn("order_month", month(col("order_date"))) \
            .withColumn("order_value_category",
                        when(col("total_amount") < 50, "Low")
                        .when(col("total_amount") < 200, "Medium")
                        .otherwise("High")
                        )

        # Customer behavior analysis
        customer_metrics = orders_processed \
            .groupBy("customer_id") \
            .agg(
            count("order_id").alias("total_orders"),
            sum("total_amount").alias("total_spent"),
            avg("total_amount").alias("avg_order_value"),
            max("order_date").alias("last_order_date"),
            min("order_date").alias("first_order_date")
        ) \
            .withColumn("customer_value_segment",
                        when(col("total_spent") > 1000, "High Value")
                        .when(col("total_spent") > 500, "Medium Value")
                        .otherwise("Low Value")
                        )

        # Join customer data with metrics
        final_customer_view = customers_enriched.join(
            customer_metrics,
            "customer_id",
            "left"
        ).fillna(0, ["total_orders", "total_spent", "avg_order_value"])

        return {
            'customers_enriched': customers_enriched,
            'orders_processed': orders_processed,
            'customer_metrics': customer_metrics,
            'final_customer_view': final_customer_view
        }

    def load_data(self, transformed_data, output_config):
        """
        Load data to various destinations
        """
        for table_name, df in transformed_data.items():
            config = output_config.get(table_name, {})

            try:
                if config.get('format') == 'delta':
                    df.write \
                        .format("delta") \
                        .mode(config.get('mode', 'overwrite')) \
                        .option("mergeSchema", "true") \
                        .save(config['path'])

                elif config.get('format') == 'parquet':
                    df.write \
                        .mode(config.get('mode', 'overwrite')) \
                        .partitionBy(*config.get('partition_by', [])) \
                        .parquet(config['path'])

                elif config.get('format') == 'jdbc':
                    df.write \
                        .format("jdbc") \
                        .mode(config.get('mode', 'overwrite')) \
                        .options(**config['options']) \
                        .save()

                self.logger.info(f"Successfully loaded {table_name}")

            except Exception as e:
                self.logger.error(f"Failed to load {table_name}: {str(e)}")
                raise


# Usage example
def run_etl_pipeline(spark):
    """
    Run complete ETL pipeline
    """
    pipeline = ETLPipeline(spark)

    # Configuration
    source_config = {
        'customers': {
            'type': 'jdbc',
            'options': {
                'url': 'jdbc:postgresql://localhost:5432/ecommerce',
                'dbtable': 'customers',
                'user': 'user',
                'password': 'password'
            }
        },
        'orders': {
            'type': 'parquet',
            'path': 's3a://data-lake/raw/orders/'
        }
    }

    output_config = {
        'final_customer_view': {
            'format': 'delta',
            'path': 's3a://data-lake/processed/customer_360/',
            'mode': 'overwrite'
        },
        'customer_metrics': {
            'format': 'parquet',
            'path': 's3a://data-lake/processed/customer_metrics/',
            'partition_by': ['customer_value_segment'],
            'mode': 'overwrite'
        }
    }

    # Execute pipeline
    raw_data = pipeline.extract_data(source_config)
    transformed_data = pipeline.transform_data(raw_data)
    pipeline.load_data(transformed_data, output_config)

    return transformed_data


```

### Real-time Analytics Pipeline
```python
# realtime_analytics.py
from pyspark.sql.streaming import StreamingQuery
from pyspark.sql.functions import *


def create_realtime_pipeline(spark):
    """
    Real-time analytics pipeline for e-commerce events
    """
    # Define schema for incoming events
    event_schema = StructType([
        StructField("event_id", StringType(), True),
        StructField("user_id", StringType(), True),
        StructField("event_type", StringType(), True),
        StructField("product_id", StringType(), True),
        StructField("category", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("value", DoubleType(), True),
        StructField("session_id", StringType(), True)
    ])

    # Read streaming data from Kafka
    raw_stream = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "user-events") \
        .option("startingOffsets", "latest") \
        .load()

    # Parse JSON events
    parsed_events = raw_stream \
        .select(
        from_json(col("value").cast("string"), event_schema).alias("event")
    ) \
        .select("event.*") \
        .withWatermark("timestamp", "10 minutes")

    # Real-time aggregations

    # 1. Event counts by type in 5-minute windows
    event_counts = parsed_events \
        .groupBy(
        window(col("timestamp"), "5 minutes", "1 minute"),
        col("event_type")
    ) \
        .count() \
        .select(
        col("window.start").alias("window_start"),
        col("window.end").alias("window_end"),
        col("event_type"),
        col("count").alias("event_count")
    )

    # 2. Top products by views in real-time
    product_views = parsed_events \
        .filter(col("event_type") == "product_view") \
        .groupBy(
        window(col("timestamp"), "10 minutes", "2 minutes"),
        col("product_id"),
        col("category")
    ) \
        .count() \
        .select(
        col("window.start").alias("window_start"),
        col("window.end").alias("window_end"),
        col("product_id"),
        col("category"),
        col("count").alias("view_count")
    )

    # 3. User session analysis
    session_metrics = parsed_events \
        .groupBy(
        col("session_id"),
        col("user_id"),
        window(col("timestamp"), "30 minutes")
    ) \
        .agg(
        count("*").alias("events_in_session"),
        countDistinct("product_id").alias("unique_products_viewed"),
        sum(when(col("event_type") == "purchase", col("value")).otherwise(0)).alias("session_revenue"),
        min("timestamp").alias("session_start"),
        max("timestamp").alias("session_end")
    ) \
        .withColumn("session_duration_minutes",
                    (col("session_end").cast("long") - col("session_start").cast("long")) / 60
                    )

    # 4. Anomaly detection for sudden spikes
    anomaly_detection = parsed_events \
        .groupBy(
        window(col("timestamp"), "1 minute"),
        col("event_type")
    ) \
        .count() \
        .withColumn("avg_count_last_hour",
                    avg("count").over(
                        Window.partitionBy("event_type")
                            .orderBy("window")
                            .rowsBetween(-60, -1)
                    )
                    ) \
        .withColumn("is_anomaly",
                    when(col("count") > col("avg_count_last_hour") * 3, True).otherwise(False)
                    ) \
        .filter(col("is_anomaly") == True)

    return {
        'event_counts': event_counts,
        'product_views': product_views,
        'session_metrics': session_metrics,
        'anomaly_detection': anomaly_detection
    }


def setup_streaming_outputs(streams_dict):
    """
    Setup output sinks for streaming queries
    """
    queries = []

    # Console output for debugging
    console_query = streams_dict['event_counts'] \
        .writeStream \
        .outputMode("update") \
        .format("console") \
        .option("truncate", False) \
        .trigger(processingTime="30 seconds") \
        .start()

    # Write to Delta tables for analytics
    delta_query = streams_dict['product_views'] \
        .writeStream \
        .format("delta") \
        .outputMode("append") \
        .option("checkpointLocation", "checkpoint/product-views") \
        .option("path", "delta-tables/product_views_realtime") \
        .trigger(processingTime="1 minute") \
        .start()

    # Kafka output for downstream systems
    kafka_query = streams_dict['session_metrics'] \
        .select(to_json(struct("*")).alias("value")) \
        .writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("topic", "session-metrics") \
        .option("checkpointLocation", "checkpoint/session-metrics") \
        .trigger(processingTime="2 minutes") \
        .start()

    # Alert system for anomalies
    def process_anomalies(df, epoch_id):
        if df.count() > 0:
            # Send alerts (email, Slack, etc.)
            anomalies = df.collect()
            for anomaly in anomalies:
                print(f"ALERT: Anomaly detected in {anomaly.event_type} - Count: {anomaly.count}")

    anomaly_query = streams_dict['anomaly_detection'] \
        .writeStream \
        .foreachBatch(process_anomalies) \
        .trigger(processingTime="30 seconds") \
        .start()

    queries.extend([console_query, delta_query, kafka_query, anomaly_query])
    return queries


```

---

## 12. Advanced Interview Questions & Solutions

### Complex SQL Problems
```python


# advanced_interview_problems.py

def complex_interview_solutions(spark):
    """
    Solutions to advanced PySpark interview problems
    """

    # Problem 1: Find the second highest salary in each department
    def second_highest_salary_per_dept(employees_df):
        window_spec = Window.partitionBy("department").orderBy(desc("salary"))

        result = employees_df \
            .withColumn("rank", dense_rank().over(window_spec)) \
            .filter(col("rank") == 2) \
            .select("department", "name", "salary")

        return result

    # Problem 2: Running total and percentage of total
    def running_totals_and_percentages(sales_df):
        window_running = Window.partitionBy("region") \
            .orderBy("date") \
            .rowsBetween(Window.unboundedPreceding, Window.currentRow)

        window_total = Window.partitionBy("region")

        result = sales_df \
            .withColumn("running_total", sum("amount").over(window_running)) \
            .withColumn("total_sales", sum("amount").over(window_total)) \
            .withColumn("percentage_of_total",
                        (col("running_total") / col("total_sales") * 100).cast("decimal(5,2)"))

        return result

    # Problem 3: Customer churn analysis
    def customer_churn_analysis(transactions_df):
        # Define churn as no transaction in last 90 days
        current_date = lit("2023-12-31")  # Assuming current date

        customer_last_transaction = transactions_df \
            .groupBy("customer_id") \
            .agg(max("transaction_date").alias("last_transaction_date"))

        churn_analysis = customer_last_transaction \
            .withColumn("days_since_last_transaction",
                        datediff(current_date, col("last_transaction_date"))) \
            .withColumn("is_churned",
                        when(col("days_since_last_transaction") > 90, True).otherwise(False)) \
            .withColumn("churn_risk_category",
                        when(col("days_since_last_transaction") > 90, "Churned")
                        .when(col("days_since_last_transaction") > 60, "High Risk")
                        .when(col("days_since_last_transaction") > 30, "Medium Risk")
                        .otherwise("Active"))

        return churn_analysis

    # Problem 4: Hierarchical data processing (employee-manager relationships)
    def process_hierarchical_data(employees_df):
        # Self-join to get manager information
        managers = employees_df.select(
            col("employee_id").alias("manager_id"),
            col("name").alias("manager_name"),
            col("salary").alias("manager_salary")
        )

        # Find employees earning more than their managers
        result = employees_df.alias("emp") \
            .join(managers.alias("mgr"), col("emp.manager_id") == col("mgr.manager_id"), "left") \
            .filter(col("emp.salary") > col("mgr.manager_salary")) \
            .select(
            col("emp.name").alias("employee_name"),
            col("emp.salary").alias("employee_salary"),
            col("mgr.manager_name"),
            col("mgr.manager_salary")
        )

        return result

    # Problem 5: Time series gap filling
    def fill_time_series_gaps(time_series_df):
        # Generate complete date range
        min_date = time_series_df.agg(min("date")).collect()[0][0]
        max_date = time_series_df.agg(max("date")).collect()[0][0]

        # Create complete date range
        date_range = spark.sql(f"""
            SELECT explode(sequence(date'{min_date}', date'{max_date}', interval 1 day)) as date
        """)

        # Get all unique categories
        categories = time_series_df.select("category").distinct()

        # Cross join to create complete grid
        complete_grid = date_range.crossJoin(categories)

        # Left join with actual data and fill gaps
        filled_series = complete_grid \
            .join(time_series_df, ["date", "category"], "left") \
            .withColumn("value",
                        when(col("value").isNull(), 0).otherwise(col("value"))) \
            .orderBy("category", "date")

        return filled_series

    return {
        'second_highest_salary': second_highest_salary_per_dept,
        'running_totals': running_totals_and_percentages,
        'churn_analysis': customer_churn_analysis,
        'hierarchical_processing': process_hierarchical_data,
        'gap_filling': fill_time_series_gaps
    }


# Performance optimization problems
def performance_optimization_problems(spark):
    """
    Performance optimization scenarios for interviews
    """

    # Problem 1: Optimizing skewed joins
    def optimize_skewed_join(large_df, small_df, join_key):
        # Identify skewed keys
        skew_threshold = 1000000  # Adjust based on data

        key_counts = large_df.groupBy(join_key).count()
        skewed_keys = key_counts.filter(col("count") > skew_threshold)

        # Separate skewed and non-skewed data
        skewed_data = large_df.join(skewed_keys.select(join_key), join_key, "inner")
        non_skewed_data = large_df.join(skewed_keys.select(join_key), join_key, "left_anti")

        # Process non-skewed data normally
        normal_join = non_skewed_data.join(broadcast(small_df), join_key, "inner")

        # Process skewed data with salting
        salt_range = 100

        skewed_salted = skewed_data \
            .withColumn("salt", (rand() * salt_range).cast("int")) \
            .withColumn("salted_key", concat(col(join_key), lit("_"), col("salt")))

        small_exploded = small_df \
            .withColumn("salt", explode(array([lit(i) for i in range(salt_range)]))) \
            .withColumn("salted_key", concat(col(join_key), lit("_"), col("salt")))

        skewed_join = skewed_salted.join(small_exploded, "salted_key", "inner") \
            .drop("salt", "salted_key")

        # Union results
        final_result = normal_join.union(skewed_join)

        return final_result

    # Problem 2: Memory-efficient large dataset processing
    def process_large_dataset_efficiently(large_df):
        # Use iterative processing for memory efficiency
        def process_partition(partition_data):
            # Process each partition independently
            processed_data = []
            for batch in partition_data:
                # Apply complex transformations
                processed_batch = batch  # Your processing logic here
                processed_data.append(processed_batch)
            return processed_data

        # Process in batches
        partitioned_df = large_df.repartition(200)  # Adjust partition count

        # Use mapPartitions for memory efficiency
        result = partitioned_df.rdd.mapPartitions(process_partition).toDF()

        return result

    return {
        'skewed_join_optimization': optimize_skewed_join,
        'memory_efficient_processing': process_large_dataset_efficiently
    }


```

---

## 13. Sample Interview Questions with Answers

### Technical Questions & Solutions
```python
# interview_qa.py

"""
COMMON PYSPARK INTERVIEW QUESTIONS AND ANSWERS

Q1: What is the difference between RDD, DataFrame, and Dataset?
A1: 
- RDD: Low-level distributed collection, no schema optimization
- DataFrame: Structured data with schema, Catalyst optimizer
- Dataset: Type-safe version of DataFrame (Scala/Java only, not available in Python)

Q2: Explain lazy evaluation in Spark
A2: Transformations are lazy (not executed immediately), only actions trigger execution.
This allows Spark to optimize the execution plan.

Q3: What are the different types of joins in Spark?
A3: Inner, Left, Right, Full Outer, Left Semi, Left Anti, Cross joins

Q4: How to handle data skew in Spark?
A4: 
- Salting technique for skewed keys
- Broadcast joins for small tables
- Custom partitioning
- Bucketing for repeated joins

Q5: What is the difference between cache() and persist()?
A5: cache() uses default storage level (MEMORY_ONLY), persist() allows specifying storage level

Q6: Explain Spark's execution model
A6: Driver creates DAG, splits into stages and tasks, executed on executors

Q7: How to optimize Spark jobs?
A7:
- Proper partitioning
- Caching frequently used data
- Avoiding shuffles
- Using broadcast joins
- Tuning Spark configuration
"""


def demonstrate_interview_concepts(spark):
    """
    Practical demonstrations of key interview concepts
    """

    # Lazy evaluation demonstration
    def lazy_evaluation_demo():
        rdd1 = spark.sparkContext.parallelize([1, 2, 3, 4, 5])
        rdd2 = rdd1.map(lambda x: x * 2)  # Transformation - lazy
        rdd3 = rdd2.filter(lambda x: x > 5)  # Transformation - lazy

        print("No execution yet - transformations are lazy")

        result = rdd3.collect()  # Action - triggers execution
        print(f"Result: {result}")

        return result

    # Join types demonstration
    def join_types_demo():
        df1 = spark.createDataFrame([(1, "A"), (2, "B"), (3, "C")], ["id", "value1"])
        df2 = spark.createDataFrame([(1, "X"), (2, "Y"), (4, "Z")], ["id", "value2"])

        joins = {
            'inner': df1.join(df2, "id", "inner"),
            'left': df1.join(df2, "id", "left"),
            'right': df1.join(df2, "id", "right"),
            'full': df1.join(df2, "id", "full"),
            'left_semi': df1.join(df2, "id", "left_semi"),
            'left_anti': df1.join(df2, "id", "left_anti")
        }

        for join_type, result_df in joins.items():
            print(f"\n{join_type.upper()} JOIN:")
            result_df.show()

        return joins

    # Caching strategies demonstration
    def caching_demo():
        df = spark.range(1000000).toDF("id")
        df = df.withColumn("squared", col("id") * col("id"))

        # Without caching
        start_time = time.time()
        count1 = df.count()
        sum1 = df.agg(sum("squared")).collect()[0][0]
        time_without_cache = time.time() - start_time

        # With caching
        df.cache()
        start_time = time.time()
        count2 = df.count()  # Triggers caching
        sum2 = df.agg(sum("squared")).collect()[0][0]  # Uses cached data
        time_with_cache = time.time() - start_time

        print(f"Without cache: {time_without_cache:.2f} seconds")
        print(f"With cache: {time_with_cache:.2f} seconds")

        df.unpersist()

        return time_without_cache, time_with_cache

    return {
        'lazy_evaluation': lazy_evaluation_demo(),
        'join_types': join_types_demo(),
        'caching_comparison': caching_demo()
    }


```

---

## 14. Complete Project Setup Instructions

### Setup Instructions
```bash
# setup.sh
# !/bin/bash

# Create project directory structure
mkdir - p
pyspark - interview - prep / {scripts / {data_processing, transformations, performance, advanced},
                              deployment / {aws, gcp, azure}, sample_data, tests, notebooks}

# Create virtual environment
python3 - m
venv
pyspark - env
source
pyspark - env / bin / activate

# Install requirements
pip
install - r
requirements.txt

# Download sample data
curl - o
sample_data / employees.csv
"https://example.com/sample-data/employees.csv"
curl - o
sample_data / orders.json
"https://example.com/sample-data/orders.json"

# Set up Jupyter kernel
python - m
ipykernel
install - -user - -name = pyspark - env - -display - name = "PySpark Environment"

# Create Spark configuration
mkdir - p
~ /.spark / conf
cp
spark - defaults.conf
~ /.spark / conf /

echo
"Setup complete! Run 'source pyspark-env/bin/activate' to activate the environment."
```

### Spark Configuration
```properties
# spark-defaults.conf
spark.sql.adaptive.enabled = true
spark.sql