from pyspark.sql import SparkSession
from pyspark.sql.functions import col, date_format, to_date

spark = SparkSession.builder.appName("customs_log").getOrCreate()

customs_data = (
    spark.read.options(header=True, inferSchema=True, sep="\t")
    .csv("hdfs://localhost:9000/user/max/input/customs_data.csv")
    .withColumn("month", date_format(to_date(col("month"), "MM/yyyy"), "yyyy/MM"))
)

code_category = spark.read.options(header=True, inferSchema=True, sep="\t").csv(
    "hdfs://localhost:9000/user/max/output/part-00000"
)

df = customs_data.join(code_category, on="code", how="inner").select(
    col("month"),
    col("country"),
    col("direction"),
    col("code"),
    col("category"),
    col("measure"),
    col("value"),
    col("netto"),
    col("quantity"),
    col("region"),
    col("district"),
)

# Very slow 1.5 hours vs 15 minutes with partitionBy
# mmyyyy = [row["month"] for row in df.select("month").distinct().collect()]
#
# for my in mmyyyy:
#     m, y = my.split("/")
#     df[col("month") == my].write.mode("overwrite").parquet(
#         f"hdfs://localhost:9000/user/max/partners/{y}/{m}/"
#     )

df.repartition("month").write.partitionBy("month").mode("overwrite").parquet(
    "hdfs://localhost:9000/user/max/partners/"
)

# Renaming directories
sc = spark.sparkContext

monthes = [row["month"] for row in df.select("month").distinct().collect()]
years = {i.split("/")[0] for i in monthes}

hadoop_conf = sc._jsc.hadoopConfiguration()
file_system = sc._jvm.org.apache.hadoop.fs.FileSystem.get(hadoop_conf)

BASE_PATH = "/user/max/partners/"
for year in years:
    year_dir = sc._jvm.org.apache.hadoop.fs.Path(BASE_PATH + year)
    file_system.mkdirs(year_dir)
for ym in monthes:
    y, m = ym.split("/")
    old_path = sc._jvm.org.apache.hadoop.fs.Path(
        f"/user/max/partners/month={y}%2F{m}/"
    )
    new_path = sc._jvm.org.apache.hadoop.fs.Path(f"/user/max/partners/{y}/{m}/")
    if file_system.rename(old_path, new_path):
        print(f"Directory '{old_path}' successfully renamed to '{new_path}'.")
    else:
        print(f"Failed to rename directory '{old_path}' to '{new_path}'.")
