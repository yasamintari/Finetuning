# Load CSV Training Data into Delta Table
# Run this in a Databricks notebook to create the training data table

import pandas as pd
from pyspark.sql import SparkSession

# Initialize Spark (already available in Databricks notebooks)
# spark = SparkSession.builder.getOrCreate()

# Configuration
catalog = "users"
schema = "yasamin_tari"
table_name = f"{catalog}.{schema}.hedge_fund_training_data"

# Method 1: Load from local CSV file
# If you have training_data.csv in your workspace
csv_path = "/Workspace/Users/{your_email}/training_data.csv"  # Update this path

try:
    # Read CSV with pandas
    df_pandas = pd.read_csv(csv_path)
    
    # Convert to Spark DataFrame
    df_spark = spark.createDataFrame(df_pandas)
    
    # Write to Delta table
    df_spark.write.format("delta").mode("overwrite").saveAsTable(table_name)
    
    print(f"✅ Success! Created Delta table: {table_name}")
    print(f"✅ Loaded {df_spark.count()} training examples")
    
    # Display sample
    print("\n=== Sample Data ===")
    spark.table(table_name).show(3, truncate=50)
    
except FileNotFoundError:
    print(f"❌ File not found: {csv_path}")
    print("\nPlease upload training_data.csv to your workspace first")
    print("Or update the csv_path variable above")

# Method 2: Load from uploaded file in Databricks
# If you uploaded CSV via Databricks UI to a volume:
"""
volume_path = f"/Volumes/{catalog}/{schema}/data/training_data.csv"
df_spark = spark.read.csv(volume_path, header=True, inferSchema=True)
df_spark.write.format("delta").mode("overwrite").saveAsTable(table_name)
"""

# Method 3: Use dbutils to upload
"""
# Upload file interactively
dbutils.fs.cp("file:/local/path/training_data.csv", f"dbfs:/FileStore/training_data.csv")

# Then read and convert to Delta
df_spark = spark.read.csv("dbfs:/FileStore/training_data.csv", header=True, inferSchema=True)
df_spark.write.format("delta").mode("overwrite").saveAsTable(table_name)
"""

# Verify the table exists
print(f"\n=== Table Information ===")
print(f"Table: {table_name}")
print(f"Row count: {spark.table(table_name).count()}")
print(f"\nSchema:")
spark.table(table_name).printSchema()
