-- Xóa các bảng cũ (theo thứ tự ngược lại) để tránh lỗi
-- 'CASCADE' sẽ tự động xóa các ràng buộc (foreign keys) liên quan
DROP TABLE IF EXISTS OrderItems;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Users;

-- Bảng Users
CREATE TABLE Users (
    UserID SERIAL PRIMARY KEY,
    Email VARCHAR(100) UNIQUE NOT NULL,
    FullName VARCHAR(50)
);

-- Bảng Products
CREATE TABLE Products (
    ProductID SERIAL PRIMARY KEY,
    ProductName VARCHAR(100) NOT NULL,
    -- DBML 'decimal' không rõ ràng, tạm dùng (10, 2) cho giá cả
    UnitPrice DECIMAL(10, 2) NOT NULL, 
    StockQuantity INT NOT NULL DEFAULT 0,
    
    -- Kịch bản 4: Đảm bảo tồn kho không bao giờ âm
    CONSTRAINT check_stock_positive CHECK (StockQuantity >= 0)
);

-- Tạo Index cho Products
CREATE INDEX idx_product_name ON Products(ProductName);

-- Bảng Orders
CREATE TABLE Orders (
    OrderID SERIAL PRIMARY KEY,
    UserID INT NOT NULL,
    Status VARCHAR(20) DEFAULT 'Pending',
    OrderDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Tạm dùng (12, 2) cho tổng tiền
    TotalAmount DECIMAL(12, 2) DEFAULT 0,
    
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Bảng OrderItems
CREATE TABLE OrderItems (
    OrderID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL,
    -- Giá tại thời điểm mua, cũng dùng (10, 2)
    UnitPrice DECIMAL(10, 2) NOT NULL, 
    
    -- Kịch bản 4: Đảm bảo số lượng mua > 0
    CONSTRAINT check_quantity_positive CHECK (Quantity > 0),
    
    -- Một sản phẩm chỉ xuất hiện 1 lần trong 1 đơn hàng
    PRIMARY KEY (OrderID, ProductID),
    
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

-- Tạo các index như trong DBML
CREATE INDEX idx_orderitems_orderid ON OrderItems(OrderID);
CREATE INDEX idx_orderitems_productid ON OrderItems(ProductID);

--==================================================
-- SEED SCRIPT FOR tSQLt/DbFit DEMO
--==================================================

-- 1. DỌN DẸP DỮ LIỆU CŨ (Để script có thể chạy lại)
-- RESTART IDENTITY: Reset các cột SERIAL (UserID, ProductID, OrderID) về 1
-- CASCADE: Tự động xóa các record con (OrderItems) khi xóa record cha (Orders)
TRUNCATE TABLE 
    OrderItems, 
    Orders, 
    Products, 
    Users
RESTART IDENTITY CASCADE;


-- 2. SEED BẢNG USERS
INSERT INTO Users (Email, FullName) VALUES
('alice@example.com', 'Alice Smith'),
('bob@example.com', 'Bob Johnson');

SELECT * FROM Users;


-- 3. SEED BẢNG PRODUCTS
-- Đây là trạng thái TỒN KHO HIỆN TẠI
INSERT INTO Products (ProductName, UnitPrice, StockQuantity) VALUES
('Laptop Pro', 1200.00, 50),
('Wireless Mouse', 25.50, 200),
('Mechanical Keyboard', 75.00, 100),
('4K Monitor', 300.00, 10); -- <-- Tồn kho thấp, hoàn hảo để test KB 4

SELECT * FROM Products;


-- 4. SEED MỘT ĐƠN HÀNG TRONG QUÁ KHỨ (Đã Hoàn thành)
-- Giả sử Alice (UserID 1) đã mua hàng hôm qua
-- INSERT này sẽ tạo ra OrderID = 1
INSERT INTO Orders (UserID, Status, TotalAmount, OrderDate) VALUES
(1, 'Completed', 100.50, CURRENT_TIMESTAMP - INTERVAL '1 day');

-- Chi tiết của đơn hàng (OrderID 1)
-- Alice đã mua 1 Keyboard (ProductID 3) và 1 Mouse (ProductID 2)
INSERT INTO OrderItems (OrderID, ProductID, Quantity, UnitPrice) VALUES
(1, 3, 1, 75.00), -- 1 x Mechanical Keyboard @ 75.00
(1, 2, 1, 25.50); -- 1 x Wireless Mouse @ 25.50

SELECT * FROM Orders;
SELECT * FROM OrderItems;