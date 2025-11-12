
-- Bảng ProductPriceHistory để lưu lịch sử giá sản phẩm
CREATE TABLE ProductPriceHistory (
    PriceHistoryID SERIAL PRIMARY KEY,
    ProductID INT NOT NULL REFERENCES Products(ProductID),
    UnitPrice DECIMAL(10, 2) NOT NULL,
    EffectiveDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Stored Procedure v1: Thêm sản phẩm vào đơn hàng với giá truyền thủ công
CREATE OR REPLACE PROCEDURE usp_AddOrderItem_v1(
    IN sp_OrderID INT,
    IN sp_ProductID INT,
    IN sp_Quantity INT,
    IN sp_UnitPrice DECIMAL(10, 2)
)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO OrderItems (OrderID, ProductID, Quantity, UnitPrice)
    VALUES (sp_OrderID, sp_ProductID, sp_Quantity, sp_UnitPrice);
END;
$$;

-- Stored Procedure v2: Thêm sản phẩm vào đơn hàng với giá tự động lấy từ Products
CREATE OR REPLACE PROCEDURE usp_AddOrderItem_v2(
    IN sp_OrderID INT,
    IN sp_ProductID INT,
    IN sp_Quantity INT
)
LANGUAGE plpgsql AS $$
DECLARE
    CurrentPrice DECIMAL(10, 2);
BEGIN
    -- Lấy giá hiện tại từ bảng Products
    SELECT UnitPrice INTO CurrentPrice
    FROM Products
    WHERE ProductID = sp_ProductID;

    IF CurrentPrice IS NULL THEN
        RAISE EXCEPTION 'Không tìm thấy sản phẩm';
    END IF;

    -- Ghi log giá vào bảng ProductPriceHistory
    INSERT INTO ProductPriceHistory (ProductID, UnitPrice)
    VALUES (sp_ProductID, CurrentPrice);

    -- Thêm chi tiết đơn hàng với giá hiện tại
    INSERT INTO OrderItems (OrderID, ProductID, Quantity, UnitPrice)
    VALUES (sp_OrderID, sp_ProductID, sp_Quantity, CurrentPrice);
END;
$$;