### **File customer_master.csv:**
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
### **transactions.csv:**
| Column Name | Data Type | Description |
|---|---|---|
| TransactionID | String | Unique identifier for each transaction |
| CustomerID | String | Customer ID associated with the transaction |
| TransactionDate | Date | Date of the transaction (YYYY-MM-DD) |
| TransactionTime | String | Time of the transaction (HH:MM:SS) |
| TransactionType | String | Type of transaction (Deposit, Withdrawal, Transfer, Payment) |
| Amount | Decimal | Monetary amount of the transaction |
| Currency | String | Currency of the transaction (USD, EUR, etc.) |
| Description | String | Brief description of the transaction |
| MerchantName | String | Name of the merchant (if applicable) |
| Location | String | City/State of the transaction (e.g., Los Angeles, CA) |
| IsFraudulent | Boolean | Indicator for potentially fraudulent transaction (TRUE/FALSE) |


Files/Tables explained.
