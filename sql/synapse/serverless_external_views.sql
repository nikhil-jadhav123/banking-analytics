-- STORAGE: https://<storageacct>.dfs.core.windows.net/silver/
-- Best with database scoped credentials + external data source, but OPENROWSET is simplest for demo.

-- Customers (Silver)
CREATE OR ALTER VIEW customer_silver AS
SELECT *
FROM OPENROWSET(
  BULK 'https://<storageacct>.dfs.core.windows.net/silver/customer_silver_delta/',
  FORMAT = 'DELTA'
) WITH (
  CustomerID VARCHAR(50),
  FirstName VARCHAR(100),
  LastName VARCHAR(100),
  Email VARCHAR(255),
  Phone VARCHAR(50),
  Address VARCHAR(255),
  City VARCHAR(100),
  State VARCHAR(50),
  ZipCode VARCHAR(20),
  DateOfBirth DATE,
  AccountType VARCHAR(50),
  OpeningDate DATE,
  ProcessedTimestamp DATETIME2
) AS rows;

-- Transactions (Silver)
CREATE OR ALTER VIEW transactions_silver AS
SELECT *
FROM OPENROWSET(
  BULK 'https://<storageacct>.dfs.core.windows.net/silver/transactions_silver_delta/',
  FORMAT = 'DELTA'
) AS rows;
