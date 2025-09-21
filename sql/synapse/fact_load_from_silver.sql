-- Populate dimensions first (idempotent patterns intentionally simplified)
INSERT INTO DimCustomer (CustomerID, FirstName, LastName, Email, Phone, Address, City, State, ZipCode, DateOfBirth, AccountType, OpeningDate)
SELECT DISTINCT c.CustomerID, c.FirstName, c.LastName, c.Email, c.Phone, c.Address, c.City, c.State, c.ZipCode, c.DateOfBirth, c.AccountType, c.OpeningDate
FROM customer_silver c
WHERE c.CustomerID NOT IN (SELECT CustomerID FROM DimCustomer);

INSERT INTO DimTransactionType (TransactionType)
SELECT DISTINCT TransactionType FROM transactions_silver
WHERE TransactionType IS NOT NULL
  AND TransactionType NOT IN (SELECT TransactionType FROM DimTransactionType);

INSERT INTO DimMerchant (MerchantName)
SELECT DISTINCT MerchantName FROM transactions_silver
WHERE ISNULL(MerchantName,'') <> ''
  AND MerchantName NOT IN (SELECT MerchantName FROM DimMerchant);

-- Fact load
INSERT INTO FactTransactions (DateKey, TimeKey, CustomerKey, TransactionTypeKey, MerchantKey, Amount, Currency, Description, Location, IsFraudulent, TransactionDateTime, TransactionID)
SELECT
  CAST(FORMAT(ts.TransactionDate, 'yyyyMMdd') AS INT) AS DateKey,
  CAST(FORMAT(ts.TransactionDateTime, 'HHmmss') AS INT) AS TimeKey,
  dc.CustomerKey,
  dtt.TransactionTypeKey,
  ISNULL(dm.MerchantKey, NULL) AS MerchantKey,
  ts.Amount, ts.Currency, ts.Description, ts.Location, ts.IsFraudulent, ts.TransactionDateTime, ts.TransactionID
FROM transactions_silver ts
JOIN DimCustomer dc ON ts.CustomerID = dc.CustomerID
JOIN DimTransactionType dtt ON ts.TransactionType = dtt.TransactionType
LEFT JOIN DimMerchant dm ON ts.MerchantName = dm.MerchantName
WHERE ts.TransactionID NOT IN (SELECT TransactionID FROM FactTransactions);
