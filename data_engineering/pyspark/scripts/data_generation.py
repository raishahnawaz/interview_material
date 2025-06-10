#Sample Python Code to Create Parquet and ORC Files
import pandas as pd
import pyarrow as pa
import pyarrow.orc as orc

# Sample data
data = {
    "id": [1, 2, 3],
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35]
}
df = pd.DataFrame(data)

# Save as Parquet
df.to_parquet("sample_data.parquet", index=False)

# Save as ORC
table = pa.Table.from_pandas(df)
with pa.OSFile("sample_data.orc", 'wb') as sink:
    with orc.ORCWriter(sink) as writer:
        writer.write(table)

# Parquet/ORC files are binary formats, hence not human-readable
from pyspark.sql import SparkSession

# Create or get a Spark session
spark = SparkSession.builder \
    .appName("Read Parquet and ORC") \
    .getOrCreate()

# Read and show Parquet file
df_parquet = spark.read.parquet("sample_data.parquet")
df_parquet.show()

# Read and show ORC file
df_orc = spark.read.orc("sample_data.orc")
df_orc.show()

