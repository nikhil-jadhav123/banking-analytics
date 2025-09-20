from pyspark.sql.functions import col, to_date, lit, current_timestamp, year, month, dayofmonth
from pyspark.sql.types import DateType

# Define schema for raw customer data (important for CSVs)
customer_schema = "CustomerID STRING, FirstName STRING, LastName STRING, Email STRING, Phone STRING, Address STRING, City STRING, State STRING, ZipCode STRING, DateOfBirth STRING, AccountType STRING, OpeningDate STRING"

bronze_customer_path = "/mnt/bronze/customer_master_raw/customer_master.csv"
df_bronze_customer = spark.read.csv(bronze_customer_path, header=True, schema=customer_schema)

# Cleaning and Type Conversion
df_silver_customer = df_bronze_customer.withColumn("DateOfBirth", to_date(col("DateOfBirth"), "yyyy-MM-dd")) \
                                     .withColumn("OpeningDate", to_date(col("OpeningDate"), "yyyy-MM-dd"))

# Deduplicate customers by CustomerID (if duplicates possible)
df_silver_customer = df_silver_customer.dropDuplicates(subset=['CustomerID'])

# Add processing timestamp
df_silver_customer = df_silver_customer.withColumn("ProcessedTimestamp", current_timestamp())

# Write to Silver Layer (Delta Lake)
silver_customer_path = "/mnt/silver/customer_silver_delta/"
df_silver_customer.write.format("delta").mode("overwrite").save(silver_customer_path) # Overwrite for master data updates
print(f"Customer data written to Silver layer at: {silver_customer_path}")
