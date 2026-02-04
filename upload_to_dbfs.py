"""
Helper script to upload training data to DBFS
Run this in Databricks or use Databricks CLI
"""

# If running in Databricks notebook:
import shutil

# Copy training data to DBFS
shutil.copy("training_data.csv", "/dbfs/FileStore/training_data.csv")
print("✓ training_data.csv uploaded to /dbfs/FileStore/training_data.csv")

# Alternatively, use Databricks CLI:
# databricks fs cp training_data.csv dbfs:/FileStore/training_data.csv
