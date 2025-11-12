# Kịch bản 3: Kiểm thử Bảo mật với DbFit và PostgreSQL

Đây là bộ test case để kiểm tra các quy tắc phân quyền và Row-Level Security (RLS) trên PostgreSQL.

## 1. Thiết lập môi trường kiểm thử

Kết nối với quyền quản trị (postgres) để chạy script khởi tạo schema và thiết lập bảo mật.

!|dbfit.PostgresTest|
|Connect|localhost:5432|postgres|postgres||mydatabase|

## 2. Kiểm thử quyền của `ordermanager`

`ordermanager` (thuộc role `ordermanagers`) phải có khả năng xem tất cả đơn hàng và cập nhật sản phẩm.

!|dbfit.PostgresTest|
|Connect|localhost:5432|ordermanager|Pass@123|mydatabase|

### 2.1. `ordermanager` có thể xem tất cả đơn hàng (RLS bỏ qua cho role này)

|Query|select count(*) from orders|
|count|
|2|

### 2.2. `ordermanager` có thể cập nhật bất kỳ đơn hàng nào

|Execute|UPDATE orders SET Status='Shipped' WHERE orderid=2|
|Query|SELECT Status FROM orders WHERE orderid=2|
|Status|
|Shipped|

### 2.3. `ordermanager` có thể cập nhật số lượng sản phẩm

|Execute|UPDATE "products" SET "StockQuantity"=90 WHERE "ProductID"=1|
|Query|SELECT "StockQuantity" FROM "products" WHERE "ProductID"=1|
|StockQuantity|
|90|

!3  Kiểm thử quyền của `customeruser` và RLS

`customeruser` chỉ được thấy và thao tác trên đơn hàng của chính mình, được xác định bởi `UserID` trong session context.

!|dbfit.PostgresTest|
|Connect|localhost:5432|customeruser|Pass@123|mydatabase|

!4 1. Thiết lập ngữ cảnh cho `UserID` = 1

|Execute|SET session app.current_user_id = '1'|

!4 2. `customeruser` (UserID=1) chỉ thấy đơn hàng của mình

|Query|select count(*) from orders|
|count|
|1|

|Query|select orderid, userid from orders|
|OrderID|UserID|
|1|1|

!4 3. `customeruser` (UserID=1) không thể xem đơn hàng của người khác (UserID=2)

|Query|select count(*) from orders where userid = 2|
|count|
|0|

!4 4. `customeruser` (UserID=1) không thể cập nhật đơn hàng của người khác

|Execute|UPDATE orders SET Status='Cancelled' WHERE orderid=2|
|Query|SELECT Status FROM orders WHERE orderid=2|
|Status|
|Shipped|

*Ghi chú: Trạng thái vẫn là 'Shipped' vì RLS đã ngăn chặn câu lệnh UPDATE (0 dòng bị ảnh hưởng).*

!4 5. `customeruser` (UserID=1) không thể chèn đơn hàng cho người khác (UserID=2) - Bị RLS `WITH CHECK` chặn

|Execute|INSERT INTO orders (userid, status, totalamount) VALUES (2, 'Fraud', 999)|
|Execute|@|
|exception|new row violates row-level security policy for table orders|

!4 6. `customeruser` không có quyền cập nhật sản phẩm

|Execute|UPDATE products SET stockquantity=50|
|Execute|@|
|exception|permission denied for table products|

!3  Kiểm thử quyền của `readonlyuser`

`readonlyuser` chỉ có quyền đọc dữ liệu, không thể thay đổi.

!|dbfit.PostgresTest|
|Connect|localhost:5432|readonlyuser|Pass@123|mydatabase|

!4 1. `readonlyuser` có thể xem tất cả đơn hàng (không bị RLS giới hạn vì hàm RLS không xét role này)
*Lưu ý: Theo logic RLS hiện tại, readonlyuser sẽ không thấy gì cả vì nó không phải 'ordermanagers' và không có context 'app.current_user_id'. Nếu muốn readonlyuser thấy tất cả, bạn cần sửa hàm RLS. Giả sử readonlyuser cũng cần context.*

|Execute|SET session app.current_user_id = '1'|
|Query|select count(*) from orders|
|count|
|1|

!4 2. `readonlyuser` không thể xóa đơn hàng

|Execute|DELETE FROM orders WHERE orderid=1|
|Execute|@|
|exception|permission denied for table orders|

!4 3. `readonlyuser` không thể cập nhật sản phẩm

|Execute|UPDATE "products" SET "UnitPrice"=100|
|Execute|@|
|exception|permission denied for table "products"|