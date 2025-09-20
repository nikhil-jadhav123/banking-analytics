from pyspark.sql.functions import col, to_date, lit, current_timestamp, concat_ws, lit, to_timestamp
from pyspark.sql.types import DecimalType, BooleanType

# Define schema for raw transaction data
transaction_schema = "TransactionID STRING, CustomerID STRING, TransactionDate STRING, TransactionTime STRING, TransactionType STRING, Amount DECIMAL(10,2), Currency STRING, Description STRING, MerchantName STRING, Location STRING, IsFraudulent STRING"

# Read latest transactions from bronze (assuming daily partitioned data)
bronze_transactions_path = "/mnt/bronze/transactions_raw/" # ADF will put data into dated subfolders
df_bronze_transactions = spark.read.csv(bronze_transactions_path, header=True, schema=transaction_schema)

# Cleaning and Type Conversion
df_silver_transactions = df_bronze_transactions.dropna(subset=['TransactionID', 'CustomerID', 'TransactionDate', 'Amount']) \
                                             .withColumn("TransactionDate", to_date(col("TransactionDate"), "yyyy-MM-dd")) \
                                             .withColumn("Amount", col("Amount").cast(DecimalType(10,2))) \
                                             .withColumn("IsFraudulent", col("IsFraudulent").cast(BooleanType()))

# Combine Date and Time for a single timestamp column
df_silver_transactions = df_silver_transactions.withColumn("TransactionDateTime",
                                                          to_timestamp(concat_ws(" ", col("TransactionDate"), col("TransactionTime")), "yyyy-MM-dd HH:mm:ss"))

# Deduplicate (e.g., by TransactionID)
df_silver_transactions = df_silver_transactions.dropDuplicates(subset=['TransactionID'])

# Filter out invalid amounts (e.g., negative transactions that shouldn't be negative for certain types)
df_silver_transactions = df_silver_transactions.filter(col("Amount") >= 0) # Adjust based on business rules

# Add processing timestamp
df_silver_transactions = df_silver_transactions.withColumn("ProcessedTimestamp", current_timestamp())

# Write to Silver Layer (Delta Lake), partitioned by TransactionDate for efficiency
silver_transactions_path = "/mnt/silver/transactions_silver_delta/"
df_silver_transactions.write.format("delta").mode("append").partitionBy("TransactionDate").save(silver_transactions_path)
print(f"Transaction data written to Silver layer at: {silver_transactions_path}")
