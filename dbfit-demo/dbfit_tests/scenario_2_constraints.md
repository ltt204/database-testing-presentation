# DbFit Test Cases for Scenario 2
# DbFit Test Cases for Scenario 2
## **Constraint Tests:**

##### **Negative Stock Quantity:**
!|Execute|TRUNCATE TABLE Products RESTART IDENTITY CASCADE|
!|Execute Procedure|sp_insert_product|
|p_product_name|p_unit_price|p_stock_quantity|
|Test Product|10.00|5|

!|Execute Procedure Expect Exception|sp_update_product_stock|
|p_product_id|p_stock|
|1|-1|

##### **Zero Quantity Order:**

!|Execute|TRUNCATE TABLE Users, Products, Orders, OrderItems RESTART IDENTITY CASCADE|

!|Execute Procedure Expect Exception|sp_insert_user|
|p_email                            |p_fullname    |
|user@test.com                      |Test User     |

##### **Negative Price:**

!|Execute|TRUNCATE TABLE Products RESTART IDENTITY CASCADE|

!|Execute Procedure Expect Exception|sp_insert_product            |
|p_product_name                     |p_unit_price|p_stock_quantity|
|Test Product                       |-10.00      |5               |

##### **Invalid Status:**

!|Execute|TRUNCATE TABLE Users, Orders RESTART IDENTITY CASCADE|

!|Execute Procedure Expect Exception|sp_insert_user|
|p_email                            |p_fullname    |
|user@test.com                      |Test User     |
                              |Shipped |'[]'::jsonb|

##### **Duplicate Email:**

!|Execute|TRUNCATE TABLE Users RESTART IDENTITY CASCADE|

!|Execute Procedure Expect Exception|sp_insert_user|
|p_email                            |p_fullname    |
|test@example.com                   |Test User     |


##### **Duplicate Order Item:**

!|Execute|TRUNCATE TABLE Users, Products, Orders, OrderItems RESTART IDENTITY CASCADE|

!|Execute Procedure Expect Exception|sp_insert_user|
|p_email                            |p_fullname    |
|user@test.com                      |Test User     |

## **Foreign Key Tests:**

##### **Invalid UserID:**

!|Execute|TRUNCATE TABLE Users, Orders RESTART IDENTITY CASCADE|

!|Execute Procedure Expect Exception|sp_insert_order|
|p_user_id|p_status|p_items|
|9999|Pending|'[]'::jsonb|

##### **Invalid ProductID:**

!|Execute|TRUNCATE TABLE Users, Products, Orders, OrderItems RESTART IDENTITY CASCADE|

!|Execute Procedure Expect Exception|sp_insert_user|
|p_email|p_fullname|
|user@test.com|Test User|

!|Execute Procedure Expect Exception|sp_insert_order|
|p_user_id|p_status|p_items|
|1|Pending|'[]'::jsonb|


!|Execute Procedure Expect Exception|sp_insert_order_item|
|p_order_id|p_product_id|p_quantity|p_unit_price|
|1|9999|1|10.00|

##### **Delete User with Orders:**

!|Execute|TRUNCATE TABLE Users, Orders RESTART IDENTITY CASCADE|
|!Execute Procedure|sp_insert_user|
|p_email|p_fullname|
|test@example.com|Test User|

!|Execute Procedure Expect Exception|sp_insert_order|
|p_user_id|p_status|p_items|
|1|Pending|'[]'::jsonb|


!|Execute Procedure Expect Exception|sp_delete_user|
|p_user_id|
|1|

## **Default Value Tests:**

##### **Order Without Date:**

!|Execute|TRUNCATE TABLE Users, Orders RESTART IDENTITY CASCADE|

!|Execute Procedure Expect Exception|sp_insert_user|
|p_email|p_fullname|
|user@test.com|Test User|

!|Execute Procedure Expect Exception|sp_insert_order|
|p_user_id|p_status|p_items|
|1|Pending|'[]'::jsonb|

!|Query|SELECT orderdate IS NOT NULL AS has_date FROM Orders WHERE orderid = 1|
|has_date?|
|true|

##### **Order Without Status:**

!|Execute|TRUNCATE TABLE Users, Orders RESTART IDENTITY CASCADE|

!|Execute Procedure Expect Exception|sp_insert_user|
|p_email|p_fullname|
|user@test.com|Test User|

!|Execute|INSERT INTO Orders (UserID, OrderDate) VALUES (1, '2025-11-11')|

!|Query|SELECT status FROM Orders WHERE userid = 1|
|status?|
|Pending|

##### **Product Without Stock:**

!|Execute|TRUNCATE TABLE Products RESTART IDENTITY CASCADE|

!|Execute Procedure Expect Exception|sp_insert_product|
|p_product_name|p_unit_price|p_stock_quantity|
|Test Product|10.00|0|

!|Query|SELECT stockquantity FROM Products WHERE productname = 'Test Product'|
|stockquantity?|
|0|

## **NULL Tests:**

##### **Product Without Name:**

!|Execute|TRUNCATE TABLE Products RESTART IDENTITY CASCADE|

!|Execute Procedure Expect Exception|sp_insert_product|
|p_product_name|p_unit_price|p_stock_quantity|
|NULL|10.00|5|

##### **Order Without UserID:**

!|Execute|TRUNCATE TABLE Orders RESTART IDENTITY CASCADE|

!|Execute Procedure Expect Exception|sp_insert_order|
|p_user_id|p_status|p_items|
|NULL|Pending|'[]'::jsonb|