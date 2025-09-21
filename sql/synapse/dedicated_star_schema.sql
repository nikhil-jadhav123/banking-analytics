-- Dimension tables
CREATE TABLE DimDate (
  DateKey INT PRIMARY KEY,
  FullDate DATE,
  DayOfMonth INT,
  Month INT,
  MonthName NVARCHAR(20),
  Quarter INT,
  Year INT,
  DayOfWeek INT,
  DayNameOfWeek NVARCHAR(20)
);

CREATE TABLE DimTime (
  TimeKey INT PRIMARY KEY,
  FullTime TIME,
  Hour INT, Minute INT, Second INT
);

CREATE TABLE DimCustomer (
  CustomerKey INT IDENTITY(1,1) PRIMARY KEY,
  CustomerID VARCHAR(50) UNIQUE,
  FirstName VARCHAR(100), LastName VARCHAR(100),
  Email VARCHAR(255), Phone VARCHAR(50),
  Address VARCHAR(255), City VARCHAR(100),
  State VARCHAR(50), ZipCode VARCHAR(20),
  DateOfBirth DATE, AccountType VARCHAR(50), OpeningDate DATE
);

CREATE TABLE DimTransactionType (
  TransactionTypeKey INT IDENTITY(1,1) PRIMARY KEY,
  TransactionType VARCHAR(50) UNIQUE
);

CREATE TABLE DimMerchant (
  MerchantKey INT IDENTITY(1,1) PRIMARY KEY,
  MerchantName VARCHAR(255) UNIQUE
);

-- Fact
CREATE TABLE FactTransactions (
  TransactionSK BIGINT IDENTITY(1,1) PRIMARY KEY,
  TransactionID VARCHAR(50) UNIQUE,
  DateKey INT FOREIGN KEY REFERENCES DimDate(DateKey),
  TimeKey INT FOREIGN KEY REFERENCES DimTime(TimeKey),
  CustomerKey INT FOREIGN KEY REFERENCES DimCustomer(CustomerKey),
  TransactionTypeKey INT FOREIGN KEY REFERENCES DimTransactionType(TransactionTypeKey),
  MerchantKey INT NULL FOREIGN KEY REFERENCES DimMerchant(MerchantKey),
  Amount DECIMAL(10,2),
  Currency VARCHAR(10),
  Description VARCHAR(255),
  Location VARCHAR(255),
  IsFraudulent BIT,
  TransactionDateTime DATETIME2
);
