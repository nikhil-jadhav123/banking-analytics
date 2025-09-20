from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, rand, expr, concat, col, round, date_format
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, BooleanType
import random
from datetime import datetime, timedelta

def generate_synthetic_transactions(spark, num_transactions, customers_df, start_date, fraud_rate=0.01):
    """
    Generates synthetic transaction data using PySpark.
    """
    # Create a list of customer IDs
    customer_ids = [row.CustomerID for row in customers_df.collect()]
    
    # Define lists for random choices
    transaction_types = ['Deposit', 'Withdrawal', 'Transfer', 'Payment']
    currencies = ['USD', 'EUR', 'GBP']
    merchant_names = ['Amazon', 'Walmart', 'Starbucks', 'Shell', 'Online Transfer', 'ATM']
    locations = ['New York, NY', 'Los Angeles, CA', 'Chicago, IL', 'Houston, TX', 'Miami, FL', 'Online']
    
    # Generate the data in a parallel way
    rows = []
    for _ in range(num_transactions):
        transaction_type = random.choice(transaction_types)
        is_payment = 1 if transaction_type == 'Payment' else 0
        merchant_name = random.choice(merchant_names) if is_payment else ''
        description = f"{transaction_type} for {merchant_name}" if is_payment else f"{transaction_type} transaction"
        
        # Create a row with generated data
        rows.append((
            f"TRN{random.randint(100000, 999999)}",
            random.choice(customer_ids),
            start_date + timedelta(days=random.randint(0, 29)),
            random.choice(transaction_types),
            round(random.uniform(5.00, 2000.00), 2),
            random.choice(currencies),
            description,
            merchant_name,
            random.choice(locations),
            random.random() < fraud_rate
        ))

    # Define schema for the DataFrame
    schema = StructType([
        StructField("TransactionID", StringType(), True),
        StructField("CustomerID", StringType(), True),
        StructField("TransactionDate", StringType(), True),
        StructField("TransactionTime", StringType(), True),
        StructField("TransactionType", StringType(), True),
        StructField("Amount", DoubleType(), True),
        StructField("Currency", StringType(), True),
        StructField("Description", StringType(), True),
        StructField("MerchantName", StringType(), True),
        StructField("Location", StringType(), True),
        StructField("IsFraudulent", BooleanType(), True)
    ])

    # Create the DataFrame
    new_transactions_df = spark.createDataFrame(rows)
    
    # Split the timestamp into date and time columns
    new_transactions_df = new_transactions_df.withColumn("TransactionDate", date_format(col("TransactionDate"), "yyyy-MM-dd"))
    new_transactions_df = new_transactions_df.withColumn("TransactionTime", date_format(col("TransactionDate"), "HH:mm:ss"))
    
    return new_transactions_df

# --- Main Script to Generate & Simulate Monthly Update ---

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("BankingTransactionGenerator") \
    .getOrCreate()

# 1. Load existing customer data (simulated for first run)
customers_df = spark.createDataFrame([
    (f'CUST{str(i).zfill(3)}', f'FN{i}', f'LN{i}') for i in range(1, 101)
], ['CustomerID', 'FirstName', 'LastName'])

# Define the month for which you want to generate data
current_year = 2024
current_month = 2
start_of_month = datetime(current_year, current_month, 1)

# Generate transactions for the current month
num_transactions_this_month = 5000
new_transactions_df = generate_synthetic_transactions(
    spark, num_transactions_this_month, customers_df, start_of_month
)

# Define output path for the new monthly file
output_dir = "data/banking_transactions_monthly/"
output_file = f"{output_dir}transactions_{current_year}_{str(current_month).zfill(2)}.csv"

# Write the DataFrame to a single CSV file
new_transactions_df.coalesce(1).write \
    .mode("overwrite") \
    .csv(output_file, header=True)

print(f"Generated {num_transactions_this_month} transactions for {current_year}-{current_month} and saved to {output_file}")

# Stop the Spark session
spark.stop()
