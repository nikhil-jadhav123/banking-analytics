**vw_EnrichedDailyTransactions**

| TransactionID | TransactionDate | TransactionTime | TransactionType | Amount | Currency | Description | MerchantName | Location | IsFraudulent | TransactionDate_Time | CustomerID | CustomerName | CustomerEmail | CustomerCity | CustomerState | CustomerAccountType | BirthYear | Age |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TRN001 | 1/1/2024 | 10:30 | Deposit | 500 | USD | Salary Deposit | N/A | Online | FALSE | 1/1/2024 10:30 | CUST001 | Jane Smith | jane.smith@example.org | Anytown | CA | Checking | 1995 | 29 |
| TRN002 | 1/1/2024 | 11:15 | Withdrawal | 50 | USD | ATM Withdrawal | Amazon | New York, NY | FALSE | 1/1/2024 11:15 | CUST002 | John Smith | john.s@example.com | Anywhere | CA | Checking | 1985 | 39 |
| TRN003 | 1/2/2024 | 14:00 | Payment | 200 | USD | Online Shopping | Amazon | Online | FALSE | 1/2/2024 14:00 | CUST002 | John Smith | john.s@example.com | Somewhere | CA | Checking | 1985 | 39 |
| TRN004 | 1/2/2024 | 16:45 | Transfer | 200 | USD | Transfer to Savings | N/A | Online | FALSE | 1/2/2024 16:45 | CUST003 | Peter Jones | p.j@example.com | Everywhere | CA | Savings | 1990 | 34 |
| TRN005 | 1/3/2024 | 9:00 | Withdrawal | 1500 | USD | Suspicious large withdrawal | N/A | Miami, FL | TRUE | 1/3/2024 9:00 | CUST002 | Jane Smith | j.smith@example.com | Anytown | CA | Checking | 1985 | 39 |

**vw_MonthlyCustomerSpending**

| CustomerID | TransactionDate | TransactionType | TotalAmountMonth |
|---|---|---|---|
| CUST001 | 2024-01-01 | Deposit | 500 |
| CUST002 | 2024-01-01 | Withdrawal | 50 |
| CUST002 | 2024-01-02 | Payment | 200 |
| CUST002 | 2024-01-03 | Withdrawal | 1500 |
| CUST003 | 2024-01-02 | Transfer | 200 |

**DimCustomer**

| CustomerID | FirstName | LastName | Email | Phone | Address | City | State | ZipCode | DateOfBirth | AccountType | OpeningDate | ProcessingTimestamp |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CUST001 | Julie | Doe | julie.doe@example.com | 555-1234 | 123 Oak Ave | Anytown | CA | 90210 | 3/15/1985 | Savings | 1/1/2018 | 6/1/2024 19:20 |
| CUST002 | Jane | Smith | jane.smith@example.com | 555-5678 | 456 Elm St | Otherville | NY | 10001 | 11/1/1978 | Credit Card | 1/1/2019 | 6/1/2024 19:20 |
| CUST003 | Robert | Johnson | rob.j@example.com | 555-8765 | 789 Pine Ln | Otherville | NY | 10001 | 11/1/1978 | Credit Card | 5/1/2019 | 6/1/2024 19:20 |

**DimTransactionType**

| TransactionTypeKey | TransactionType |
|---|---|
| 1 | Deposit |
| 2 | Withdrawal |
| 3 | Payment |
| 4 | Transfer |

**DimMerchant**

| MerchantKey | MerchantName |
|---|---|
| 1 | Amazon |

**FactTransaction**
| TransactionSK | TransactionDate | DateKey | TransactionTypeKey | MerchantKey | Amount | Currency | Description | Location | IsFraudulent | TransactionDate_Time |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | TRN001 | 20240101 | 1 | 1 | 500 | USD | Salary Deposit | Online | FALSE | 1/1/2024 10:30 |
| 2 | TRN002 | 20240101 | 2 | 2 | 50 | USD | ATM Withdrawal | New York, NY | FALSE | 1/1/2024 11:15 |
| 3 | TRN003 | 20240102 | 3 | 1 | 200 | USD | Online Shopping | Seattle, WA | FALSE | 1/2/2024 14:00 |
| 4 | TRN004 | 20240102 | 4 | 2 | 200 | USD | Transfer to Savings | N/A | FALSE | 1/2/2024 16:45 |
| 5 | TRN005 | 20240103 | 5 | 2 | 1500 | USD | suspicious large withdrawal | Miami, FL | TRUE | 1/3/2024 9:00 |
