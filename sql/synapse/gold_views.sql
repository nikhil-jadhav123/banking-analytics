-- Enriched Daily Transactions
CREATE OR ALTER VIEW vw_EnrichedDailyTransactions AS
SELECT
  t.TransactionID,
  t.TransactionDate,
  t.TransactionDateTime,
  t.TransactionType,
  t.Amount,
  t.Currency,
  t.Description,
  t.MerchantName,
  t.Location,
  t.IsFraudulent,
  c.CustomerID,
  c.FirstName,
  c.LastName,
  c.Email,
  c.City AS CustomerCity,
  c.State AS CustomerState,
  c.AccountType,
  YEAR(c.DateOfBirth) AS BirthYear,
  DATEDIFF(year, c.DateOfBirth, GETDATE()) AS Age
FROM transactions_silver t
JOIN customer_silver c ON t.CustomerID = c.CustomerID;

-- Monthly Customer Spending
CREATE OR ALTER VIEW vw_MonthlyCustomerSpending AS
SELECT
  c.CustomerID, c.FirstName, c.LastName, c.City, c.State,
  FORMAT(t.TransactionDate, 'yyyy-MM') AS TransactionMonth,
  t.TransactionType,
  SUM(t.Amount) AS TotalMonthlyAmount
FROM transactions_silver t
JOIN customer_silver c ON t.CustomerID = c.CustomerID
GROUP BY
  c.CustomerID, c.FirstName, c.LastName, c.City, c.State,
  FORMAT(t.TransactionDate, 'yyyy-MM'), t.TransactionType;

-- Fraudulent Transaction Summary
CREATE OR ALTER VIEW vw_FraudulentTransactionSummary AS
SELECT
  t.TransactionDate,
  t.TransactionType,
  t.Location,
  SUM(t.Amount) AS TotalFraudAmount,
  COUNT(DISTINCT t.TransactionID) AS NumberOfFraudTransactions
FROM transactions_silver t
WHERE t.IsFraudulent = 1
GROUP BY t.TransactionDate, t.TransactionType, t.Location;
