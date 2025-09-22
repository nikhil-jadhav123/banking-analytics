# Enterprise Banking Customer Transaction Analytics (Azure • Medallion)

Project Overview
This project provides a robust, end-to-end data pipeline solution built on the Microsoft Azure data stack. It is designed to ingest raw financial transaction data, transform it into a clean and structured format, and finally, present it in a performant, analytics-ready layer.

The core principle of this project is the Medallion Architecture, which organizes data into three logical layers: Bronze (raw), Silver (cleaned), and Gold (analytics-ready). This approach ensures data quality, governance, and a clear separation of concerns for each stage of the data lifecycle.

Key Features
Automated Ingestion: Scalable data ingestion from source systems to the Bronze layer using Azure Data Factory (ADF).

Data Transformation: A powerful, distributed data processing layer built on Azure Databricks with PySpark for cleaning, standardizing, and enriching raw data.

Analytics-Ready Schema: A dedicated Gold layer in Azure Synapse Analytics, modeled as a star schema for efficient reporting and business intelligence.

CI/CD Pipeline: Automated testing and deployment workflows using GitHub Actions to ensure code quality and reliable releases.

Comprehensive Documentation: Detailed guides for architecture, data dictionary, and operational procedures.

Architecture
This project is built on the Medallion Architecture, a data engineering design pattern that provides a structured approach for processing data. It organizes data into three distinct layers: Bronze, Silver, and Gold, ensuring data quality, reliability, and accessibility.

Bronze Layer (Raw Data Lake)
Purpose: This is the entry point for all raw data. It serves as an immutable, append-only historical record.

Data: Contains raw, untransformed data ingested directly from source systems (e.g., transaction logs from core banking, customer master data).

Characteristics:

Data is stored as-is, without any cleaning or schema enforcement.

Files are often in their native format (e.g., CSV, JSON).

This layer is critical for data archival and auditing.

In this project: The transactions.csv and customer_master.csv files are initially ingested into this layer.

Silver Layer (Cleaned & Conformed Data Lake)
Purpose: This layer contains trusted data that has been cleaned, validated, and enriched. It acts as a single source of truth for the organization.

Data: Raw data from the Bronze layer is transformed here.
This includes:

Parsing and cleaning invalid records.

Applying data type conversions and standardizing formats.

Joining different datasets (e.g., joining transaction data with customer information).

De-duplicating records.

Characteristics:

Data is structured and organized (e.g., partitioned by date).

Stored in an optimized format like Delta Lake, which provides ACID transactions and time travel capabilities.

Serves as the foundation for analytical and machine learning tasks.

In this project: The Databricks notebooks (NB_Customer_Bronze_To_Silver.py and NB_Transactions_Bronze_To_Silver.py) perform the transformations to create the tables in this layer.

Gold Layer (Curated & Aggregated Data Warehouse)
Purpose: This is the final layer, providing curated, aggregated, and highly optimized data for reporting and business intelligence.

Data: Contains business-level aggregations and pre-calculated metrics from the Silver layer.

Characteristics:

Data is often modeled in a star or snowflake schema for easy consumption by BI tools.

Queries are fast and efficient as complex joins and aggregations are pre-computed.

In this project: Azure Synapse Analytics views and tables are used to create the Gold layer, which is directly consumed by the Power BI dashboard.

Data Dictionary
This section provides a detailed breakdown of the data schemas for the primary datasets used in this project.

File customer_master.csv:
| Column Name | Data Type | Description |
|---|---|---|
| CustomerID | String | Unique identifier for each customer |
| FirstName | String | Customer's first name |
| LastName | String | Customer's last name |
| Email | String | Customer's email address |
| Phone | String | Customer's phone number |
| Address | String | Customer's address |
| City | String | Customer's city |
| State | String | Customer's state |
| ZipCode | String | Customer's zip code |
| DateOfBirth | Date | Customer's date of birth (YYYY-MM-DD) |
| AccountType | String | Type of bank account (Savings, Checking, Credit Card) |
| OpeningDate | Date | Date when the account was opened (YYYY-MM-DD) |

----------------------------------------------------------------------------------
transactions.csv:
| Column Name | Data Type | Description |
|---|---|---|
| TransactionID | String | Unique identifier for each transaction |
| CustomerID | String | Customer ID associated with the transaction |
| TransactionDate | Date | Date of the transaction (YYYY-MM-DD) |
| TransactionTime | String | Time of the transaction (HH:MM:SS) |
| TransactionType | String | Type of transaction (Deposit, Withdrawal, Transfer, Payment) |
----------------------------------------------------------------------------------
Analytics Layer (Gold) SQL Scripts
The following SQL scripts are used to create the analytics-ready Gold layer in Azure Synapse Analytics, leveraging the data in the Silver layer.

serverless_external_views.sql
This script creates external views on top of the Silver layer using the serverless SQL pool. This is ideal for ad-hoc queries and exploration.

dedicated_star_schema.sql
This script defines the dimensional model (star schema) in a dedicated SQL pool, which is optimized for high-performance BI queries.

fact_load_from_silver.sql
This script handles the incremental loading of data from the Silver layer into the Gold layer's dimension and fact tables.

gold_views.sql
This script creates a set of common views in the Gold layer for consumption by BI tools, pre-joining and enriching data for easy use.

**Sample Data Output**
This section shows examples of the data you can expect to see in the final Gold layer views and tables, after the pipeline has been run with the provided sample data.

FactTransaction
| TransactionSK | TransactionDate | DateKey | TransactionTypeKey | MerchantKey | Amount | Currency | Description | Location | IsFraudulent | TransactionDate_Time |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | TRN001 | 20240101 | 1 | 1 | 500 | USD | Salary Deposit | Online | FALSE | 1/1/2024 10:30 |
| 2 | TRN002 | 20240101 | 2 | 2 | 50 | USD | ATM Withdrawal | New York, NY | FALSE | 1/1/2024 11:15 |
| 3 | TRN003 | 20240102 | 3 | 1 | 200 | USD | Online Shopping | Seattle, WA | FALSE | 1/2/2024 14:00 |
| 4 | TRN004 | 20240102 | 4 | 2 | 200 | USD | Transfer to Savings | N/A | FALSE | 1/2/2024 16:45 |
| 5 | TRN005 | 20240103 | 5 | 2 | 1500 | USD | suspicious large withdrawal | Miami, FL | TRUE | 1/3/2024 09:00 |



Power BI Reports & Analytics
This project's Gold layer is designed to be consumed by Power BI for business intelligence and reporting. You can connect directly to the Synapse views to build powerful, interactive dashboards.

Power BI Guide
Connect to Synapse: Connect to the dedicated SQL pool in your Azure Synapse workspace.

Select Views: Import data from the following views:

vw_EnrichedDailyTransactions

vw_MonthlyCustomerSpending

vw_FraudulentTransactionSummary

Build Dashboards:

Customer 360: Create visualizations covering demographics, top customers, and account activity.

Transaction Activity: Use charts to show transaction volume, type breakdowns, and a map of transaction locations.

Fraud Monitoring: Build a dashboard to track fraudulent transactions by count, amount, date, location, and merchant.

Power BI Dashboards
Operations
Scheduling: Use ADF triggers for daily or hourly ingestion and post-ingestion transformations.

Monitoring: Monitor pipeline runs using ADF run history and Azure Monitor. Track Databricks job runs and Synapse SQL requests for performance and errors.

Cost Controls: Prefer Serverless SQL for ad-hoc queries to minimize costs. Use auto-stop clusters in Databricks for development environments.

Security & Governance
Secrets: Utilize Azure Key Vault to securely manage secrets. Use Managed Identities wherever possible to avoid storing credentials in code or configuration files.

Access Control: Implement Role-Based Access Control (RBAC) on storage containers to restrict data access. Use private endpoints for ADF, Databricks, and Synapse to ensure all communication is within a secure virtual network.

Data Handling: This project uses a synthetic dataset with no real PII (Personally Identifiable Information). For real-world applications, ensure sensitive data is pseudonymized or tokenized, and apply strict data access policies.

Project Structure
This repository is organized to logically separate different components of the data platform.


├── .github/workflows/          # CI/CD workflows for automation
│   └── ci.yml
├── requirements.txt            # Python dependencies for Databricks notebooks
├── data/                       # Sample data and data generation scripts
│   ├── sample/
│   │   ├── customer_master.csv
│   │   └── transactions.csv
│   └── generate_synthetic_data.py
├── databricks/                 # Databricks notebooks and utility scripts
│   ├── NB_Customer_Bronze_To_Silver.py
│   ├── NB_Transactions_Bronze_To_Silver.py
│   └── utils_mount_adls.py
├── sql/                        # SQL scripts for Azure Synapse Analytics
│   └── synapse/
│       ├── serverless_external_views.sql
│       ├── gold_views.sql
│       ├── dedicated_star_schema.sql
│       └── fact_load_from_silver.sql
├── adf/                        # Azure Data Factory artifacts (JSON)
│   ├── linkedServices/
│   ├── datasets/
│   └── pipelines/
├── docs/                       # Project documentation
│   ├── architecture.md
│   ├── data_dictionary.md
│   ├── powerbi_guide.md
│   ├── operations.md
│   └── security_and_governance.md
└── powerbi/                    # Power BI artifacts
    └── README.md

data/: Contains small sample files for quick local setup and a script (generate_synthetic_data.py) to create larger, realistic datasets for testing and development.

databricks/: Houses all the Databricks notebook code, written in PySpark, for the transformation layer. The utils_mount_adls.py script is a crucial utility for connecting to ADLS.

sql/: All SQL scripts for creating external views, loading data, and defining the final star schema in Synapse Analytics.

adf/: The entire Data Factory project is exported here, with JSON files for linked services, datasets, and pipelines. This allows for automated deployment of the pipeline using CI/CD.

docs/: This is a critical folder. It contains detailed documentation on various aspects of the project, including its high-level architecture, a complete data dictionary, and a guide for Power BI developers.

Getting Started
Follow these steps to set up and run the data pipeline.

Prerequisites
An Azure Subscription.

Git installed on your machine.

Python 3.8+ and pip.

Access to an Azure Data Lake Storage account, Azure Databricks workspace, and an Azure Synapse Analytics workspace.

Install Dependencies:

pip install -r requirements.txt

This will install pyspark==3.4.1 and faker==24.4.0.

Azure Setup
Configure Azure Resources:

Create an Azure Data Lake Storage (ADLS) account and create the bronze, silver, and gold file systems.

Create an Azure Databricks workspace.

Create an Azure Synapse Analytics workspace with a dedicated SQL pool and a serverless SQL pool.

Mount ADLS in Databricks:

Create a secret scope in your Databricks workspace (e.g., kv-scope).

Store the service principal details (tenant-id, sp-app-id, sp-sec) as secrets.

Run the utils_mount_adls.py notebook in your Databricks workspace to mount the bronze and silver containers.

Running the Pipeline
Manual Data Ingestion (for local testing):

Upload the customer_master.csv and transactions.csv from the data/sample/ directory into your ADLS Bronze container.

Alternatively, run the generate_synthetic_data.py script to generate new data.

Orchestration with Azure Data Factory:

Import the JSON files from the adf/ directory into your Azure Data Factory workspace.

Configure the linked services with the correct connection details for your storage account and Databricks workspace.

Trigger the ingestion pipelines (PL_Ingest...) and then the transformation pipelines (PL_Transform...) to start the data flow.

Creating the Analytics Layer in Synapse:

Connect to your Azure Synapse Analytics workspace.

Run the SQL scripts in the sql/synapse/ directory in the correct order:

serverless_external_views.sql

dedicated_star_schema.sql

fact_load_from_silver.sql (can be configured to run as part of the ADF pipeline)

gold_views.sql

Further Documentation
For more in-depth information, please refer to the documents in the docs/ folder:

Architecture: docs/architecture.md

Data Dictionary: docs/data_dictionary.md

Power BI Guide: docs/powerbi_guide.md

Operations & Monitoring: docs/operations.md

Security & Governance: docs/security_and_governance.md


License
This project is licensed under the MIT License. See the LICENSE file for details.
