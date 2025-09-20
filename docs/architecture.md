###Project Architecture###
Medallion Architecture for Transaction Analytics
This project is built on the Medallion Architecture, a data engineering design pattern that provides a structured approach for processing data. It organizes data into three distinct layers: Bronze, Silver, and Gold, ensuring data quality, reliability, and accessibility.

!(https://www.google.com/search?q=https://example.com/medallion-architecture-diagram.png)

Bronze Layer (Raw Data Lake)
Purpose: This is the entry point for all raw data. It serves as an immutable, append-only historical record.

Data: Contains raw, untransformed data ingested directly from source systems (e.g., transaction logs from core banking, customer master data).

Characteristics:

Data is stored as-is, without any cleaning or schema enforcement.

Files are often in their native format (e.g., CSV, JSON).

This layer is critical for data archival and auditing.

In this project:

The transactions.csv and customer_master.csv files are initially ingested into this layer.

Silver Layer (Cleaned & Conformed Data Lake)
Purpose: This layer contains trusted data that has been cleaned, validated, and enriched. It acts as a single source of truth for the organization.

Data: Raw data from the Bronze layer is transformed here. This includes:

Parsing and cleaning invalid records.

Applying data type conversions and standardizing formats.

Joining different datasets (e.g., joining transaction data with customer information).

De-duplicating records.

Characteristics:

Data is structured and organized (e.g., partitioned by date).

Stored in an optimized format like Delta Lake, which provides ACID transactions and time travel capabilities.

Serves as the foundation for analytical and machine learning tasks.

In this project:

The Databricks notebooks (NB_Customer_Bronze_To_Silver.py and NB_Transactions_Bronze_To_Silver.py) perform the transformations to create the tables in this layer.

Gold Layer (Curated & Aggregated Data Warehouse)
Purpose: This is the final layer, providing curated, aggregated, and highly optimized data for reporting and business intelligence.

Data: Contains business-level aggregations and pre-calculated metrics from the Silver layer.

Characteristics:

Data is often modeled in a star or snowflake schema for easy consumption by BI tools.

Queries are fast and efficient as complex joins and aggregations are pre-computed.

In this project:

Azure Synapse Analytics views (gold_layer_views.sql) and tables are used to create the Gold layer, which is directly consumed by the Power BI dashboard.

Examples include views for vw_EnrichedDailyTransactions and vw_MonthlyCustomerSpending.

By following this architecture, the project ensures data quality, governance, and reusability across different business applications.
