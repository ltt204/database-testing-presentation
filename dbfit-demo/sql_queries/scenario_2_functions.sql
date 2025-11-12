-- Procedure: sp_insert_user
-- Description: Inserts a user into the Users table and handles constraint violations.
CREATE OR REPLACE PROCEDURE sp_insert_user(
    p_email VARCHAR(100),
    p_fullname VARCHAR(50)
)
LANGUAGE plpgsql
AS $$
BEGIN
    BEGIN
        INSERT INTO Users (Email, FullName)
        VALUES (p_email, p_fullname);
    EXCEPTION WHEN unique_violation THEN
        RAISE NOTICE 'User with email % already exists.', p_email;
    END;
END;
$$;

-- Procedure: sp_insert_product
-- Description: Inserts a product into the Products table.
CREATE OR REPLACE PROCEDURE sp_insert_product(
    p_product_name VARCHAR(100),
    p_unit_price NUMERIC,
    p_stock_quantity INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO Products (ProductName, UnitPrice, StockQuantity)
    VALUES (p_product_name, p_unit_price, p_stock_quantity);
END;
$$;

-- Procedure: sp_insert_order
-- Description: Inserts an order and its items, ensuring constraints are respected.
CREATE OR REPLACE PROCEDURE sp_insert_order(
    p_user_id INT,
    p_status VARCHAR(20),
    p_items JSONB
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_order_id INT;
    v_item JSONB;
BEGIN
    -- Insert the order
    INSERT INTO Orders (UserID, Status)
    VALUES (p_user_id, p_status)
    RETURNING OrderID INTO v_order_id;

    -- Loop through items and insert them
    FOR v_item IN SELECT * FROM jsonb_array_elements(p_items) LOOP
        BEGIN
            INSERT INTO OrderItems (OrderID, ProductID, Quantity, UnitPrice)
            VALUES (
                v_order_id,
                (v_item->>'ProductID')::INT,
                (v_item->>'Quantity')::INT,
                (v_item->>'UnitPrice')::NUMERIC
            );
        EXCEPTION WHEN foreign_key_violation THEN
            RAISE NOTICE 'Product ID % does not exist.', v_item->>'ProductID';
        END;
    END LOOP;
END;
$$;

-- Procedure: sp_insert_order_item
-- Description: Inserts an item into the OrderItems table.
CREATE OR REPLACE PROCEDURE sp_insert_order_item(
    p_order_id INT,
    p_product_id INT,
    p_quantity INT,
    p_unit_price NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO OrderItems (OrderID, ProductID, Quantity, UnitPrice)
    VALUES (p_order_id, p_product_id, p_quantity, p_unit_price);
END;
$$;

-- Procedure: sp_update_product_stock
-- Description: Updates the stock quantity of a product.
CREATE OR REPLACE PROCEDURE sp_update_product_stock(
    p_product_id INT,
    p_stock INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE Products
    SET StockQuantity = p_stock
    WHERE ProductID = p_product_id;

    IF NOT FOUND THEN
        RAISE NOTICE 'Product ID % does not exist.', p_product_id;
    END IF;
END;
$$;

-- Procedure: sp_delete_user
-- Description: Deletes a user from the Users table.
CREATE OR REPLACE PROCEDURE sp_delete_user(
    p_user_id INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM Users WHERE UserID = p_user_id;
END;
$$;

DO $$
DECLARE
    v_user_id INT;
    v_order_id INT;
    v_product_id_laptop INT;
    v_product_id_mouse INT;
BEGIN
    -- Clean up previous test data to ensure a fresh start
    TRUNCATE TABLE OrderItems, Orders, Products, Users RESTART IDENTITY CASCADE;

    -- Insert a user for the test
    INSERT INTO Users (Email, FullName)
    VALUES ('john.doe@test.com', 'John Doe')
    RETURNING UserID INTO v_user_id;

    -- Insert products for the test
    INSERT INTO Products (ProductName, UnitPrice, StockQuantity)
    VALUES ('Laptop Dell XPS', 1200.00, 10)
    RETURNING ProductID INTO v_product_id_laptop;

    INSERT INTO Products (ProductName, UnitPrice, StockQuantity)
    VALUES ('Mouse Logitech', 25.00, 50)
    RETURNING ProductID INTO v_product_id_mouse;

    -- Insert a 'Pending' order for the user
    INSERT INTO Orders (UserID, Status)
    VALUES (v_user_id, 'Pending')
    RETURNING OrderID INTO v_order_id;

    -- Insert items for that order
    INSERT INTO OrderItems (OrderID, ProductID, Quantity, UnitPrice)
    VALUES
        (v_order_id, v_product_id_laptop, 2, 1200.00), -- 2 Laptops
        (v_order_id, v_product_id_mouse, 3, 25.00);    -- 3 Mice
END $$;
