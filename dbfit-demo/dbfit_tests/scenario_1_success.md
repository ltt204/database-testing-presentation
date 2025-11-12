# Test Case 1: Success Case - Complete a pending order

This test verifies the "happy path" for completing an order.

## Test Setup
```php
!path lib/*.jar

!|dbfit.PostgresTest|
!|Connect|localhost:5544|myuser|mypassword|mydatabase|
```

## 1. Initial State (Given)

First, we ensure the database is in a known state. We use the `scenario_1.sql` script to reset data and create a pending order. The `Execute File` command runs our setup script.
```
!|Execute File|sql_queries/scenario_1.sql|
```
We can verify the initial state of the `Products` and `Orders` tables.
```php
**Initial Products:**
!|Query|SELECT productname, stockquantity FROM products ORDER BY productname|
|productname|stockquantity|
|Laptop Dell XPS|10|
|Mouse Logitech|50|
```
**Initial Order:**
```
!|Query|SELECT orderid, status, totalamount FROM orders WHERE orderid = 1|
|orderid|status|totalamount|
|1|Pending|0.00|
```

## 2. Action (When)

Now, we execute the main function `fn_complete_order` for the pending order (OrderID = 1).
```php
!|Execute|SELECT fn_complete_order(1)|
|fn_complete_order?|
|Order completed successfully|
```

## 3. Final State (Then)

After the function runs, we verify that the database state has changed as expected.
**Final Products (Stock should be reduced):**
```php
!|Query|SELECT productname, stockquantity FROM products ORDER BY productname|
|productname|stockquantity?|
|Laptop Dell XPS|8|
|Mouse Logitech|47|
```
**Final Order (Status and TotalAmount should be updated):**
```
!|Query|SELECT orderid, status, totalamount FROM orders WHERE orderid = 1|
|orderid|status?|totalamount?|
|1|Completed|2475.00|
```

---

# Test Case 2: Insufficient Stock

## Test Setup
```php
!path lib/*.jar

!|dbfit.PostgresTest|
!|Connect|localhost:5544|myuser|mypassword|mydatabase|
```

## 1. Initial State (Given)

Set up the database with insufficient stock for the order. The `Execute File` command runs our setup script.
```
!|Execute File|sql_queries/scenario_2_functions.sql|
```
Verify the initial state of the `Products` and `Orders` tables.
```php
**Initial Products:**
!|Query|SELECT productname, stockquantity FROM products ORDER BY productname|
|productname|stockquantity|
|Laptop Dell XPS|1|
|Mouse Logitech|50|
```
**Initial Order:**
```
!|Query|SELECT orderid, status, totalamount FROM orders WHERE orderid = 1|
|orderid|status|totalamount|
|1|Pending|0.00|
```

## 2. Action (When)

Execute the main function `fn_complete_order` for the pending order (OrderID = 1).
```php
!|Execute|SELECT fn_complete_order(1)|
|fn_complete_order?|
|Insufficient stock for one or more items|
```

## 3. Final State (Then)

Verify that the database state remains unchanged.
**Final Products:**
```php
!|Query|SELECT productname, stockquantity FROM products ORDER BY productname|
|productname|stockquantity?|
|Laptop Dell XPS|1|
|Mouse Logitech|50|
```
**Final Order:**
```
!|Query|SELECT orderid, status, totalamount FROM orders WHERE orderid = 1|
|orderid|status?|totalamount?|
|1|Pending|0.00|
```

---

# Test Case 3: Already Completed Order

## Test Setup
```php
!path lib/*.jar

!|dbfit.PostgresTest|
!|Connect|localhost:5544|myuser|mypassword|mydatabase|
```

## 1. Initial State (Given)

Set up the database with an already completed order. The `Execute File` command runs our setup script.
```
!|Execute File|sql_queries/scenario_3.sql|
```
Verify the initial state of the `Orders` table.
```php
**Initial Order:**
!|Query|SELECT orderid, status, totalamount FROM orders WHERE orderid = 1|
|orderid|status|totalamount|
|1|Completed|2475.00|
```

## 2. Action (When)

Execute the main function `fn_complete_order` for the completed order (OrderID = 1).
```php
!|Execute|SELECT fn_complete_order(1)|
|fn_complete_order?|
|Order is not in Pending status|
```

## 3. Final State (Then)

Verify that the database state remains unchanged.
**Final Order:**
```php
!|Query|SELECT orderid, status, totalamount FROM orders WHERE orderid = 1|
|orderid|status?|totalamount?|
|1|Completed|2475.00|
```