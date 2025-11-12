# Kịch bản 4: Kiểm thử Hồi quy với DbFit và PostgreSQL

Đây là bộ test case để kiểm tra hồi quy khi triển khai tính năng mới liên quan đến giá sản phẩm và lịch sử giá.

## 1. Thiết lập môi trường kiểm thử

Đầu tiên, chúng ta kết nối với quyền quản trị để chạy script khởi tạo cơ sở dữ liệu, tạo bảng, và thiết lập các stored procedure (v1 và v2).

!|dbfit.PostgresTest|
|Connect|host=localhost;port=5432;database=postgres;user=postgres;password=postgres|
|Execute file|db_schema_init.sql|
|Execute file|sql_queries/scenario_4_setup_postgres.sql|

## 2. Kiểm thử chức năng cũ (v1)

!|dbfit.PostgresTest|
|Connect|host=localhost;port=5432;database=postgres;user=postgres;password=postgres|

### 2.1. Thêm sản phẩm vào đơn hàng với giá truyền thủ công

|Execute|CALL usp_AddOrderItem_v1(1, 1, 2, 100.00)|
|Query|SELECT orderid, productid, quantity, unitprice FROM orderitems WHERE orderid=1 AND productid=1|
|OrderID|ProductID|Quantity|UnitPrice|
|1|1|2|100.00|

### 2.2. Thêm sản phẩm với giá sai

|Execute|CALL usp_AddOrderItem_v1(1, 1, 1, 50.00)|
|Query|SELECT unitprice FROM orderitems WHERE orderid=1 AND productid=1 AND quantity=1|
|UnitPrice|
|50.00|

## 3. Kiểm thử chức năng mới (v2)

!|dbfit.PostgresTest|
|Connect|host=localhost;port=5432;database=postgres;user=postgres;password=postgres|

### 3.1. Thêm sản phẩm vào đơn hàng với giá tự động lấy

!|Execute Ddl|CALL usp_AddOrderItem_v2(1, 1, 2)|

!|Query|SELECT orderid, productid, quantity, unitprice FROM orderitems WHERE orderid=1 AND productid=1|
|OrderID|ProductID|Quantity|UnitPrice|
|1|1|2|100.00|

### 3.2. Thêm sản phẩm không tồn tại

!|Execute Ddl|CALL usp_AddOrderItem_v2(1, 999, 1)|

!|Execute|@|
|exception|Không tìm thấy sản phẩm|

### 3.3. Kiểm tra lịch sử giá

!|Query|SELECT productid, unitprice FROM "ProductPriceHistory" WHERE productid=1|
|ProductID|UnitPrice|
|1|100.00|

## 4. Kiểm thử hồi quy

### 4.1. Gọi stored procedure với 4 tham số (v2)

|Execute|CALL usp_AddOrderItem_v2(1, 1, 2, 100.00)|
|Execute|@|
|exception|Procedure or function usp_AddOrderItem_v2 has too many arguments specified|

### 4.2. Thay đổi giá sản phẩm giữa các lần thêm

|Execute|UPDATE "Products" SET unitprice=150.00 WHERE productid=1|
|Execute|CALL usp_AddOrderItem_v2(1, 1, 1)|
|Query|SELECT unitprice FROM orderitems WHERE orderid=1 AND productid=1 AND quantity=1|
|UnitPrice|
|150.00|

### 4.3. Kiểm tra tính toàn vẹn dữ liệu

|Query|SELECT COUNT(*) FROM orderitems WHERE unitprice NOT IN (SELECT unitprice FROM "Products")|
|count|
|0|