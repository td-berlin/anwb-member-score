"""
Usage:
  parallel_data_prep.py <file_path>
  parallel_data_prep.py (-h | --help)
  parallel_data_prep.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.

Arguments:
  <file_path>   Path to the input Parquet file.
"""

import pyspark.sql.functions as F
from docopt import docopt
from pyspark.sql import SparkSession
from pyspark.sql.types import *


def transform_to_rfm(file_path: str) -> None:
    spark = (
        SparkSession.builder.appName("TransformToRFM")
        .config("spark.sql.legacy.parquet.nanosAsLong", "true")
        .getOrCreate()
    )
    res_schema = StructType(
        [
            StructField("id", IntegerType(), True),
            StructField("date", DateType(), True),
            StructField("cds_bought", IntegerType(), True),
            StructField("spent", FloatType(), True),
        ]
    )
    data_df = (
        spark.read.format("parquet")
        .option("inferSchema", "false")
        .schema(res_schema)
        .load(file_path)
        .cache()
    )
    print(data_df.count())
    analysis_date = data_df.agg(F.max("date")).collect()[0][0]

    rfm = data_df.groupBy("id").agg(
        F.datediff(F.max("date"), F.min("date")).alias("recency"),
        F.datediff(F.lit(analysis_date), F.min("date")).alias("T"),
        (F.count("id") - 1).alias("frequency"),
        F.mean("spent").alias("monetary_value"),
    )
    rfm = rfm.filter(F.col("frequency") > 0)
    rfm = rfm.withColumnRenamed("id", "customer_id")
    rfm.write.mode("overwrite").parquet("data/rfm_data/rfm_df.parquet")
    spark.stop()


if __name__ == "__main__":
    arguments = docopt(__doc__, version="Transform RFM 1.0")
    file_path = arguments["<file_path>"]
    transform_to_rfm(file_path)
    print("Data Transformed")
