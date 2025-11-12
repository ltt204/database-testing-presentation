-- =============================================================================
-- SCENARIO 1: Integration Testing - Order Creation with Stock Management
-- PostgreSQL (PL/pgSQL) compatible functions
-- =============================================================================

-- Drop existing functions to ensure a clean slate
DROP FUNCTION IF EXISTS fn_calculate_order_total(INT);
DROP FUNCTION IF EXISTS fn_complete_order(INT);


-- =============================================================================
-- 1. Dependency Function (Calculator - No persistence)
-- Name: fn_calculate_order_total
-- Description: Calculates the total amount of an order and checks if all
--              items in that order are in stock.
-- Parameters:
--   p_order_id: The ID of the order to check.
-- Returns:
--   A table with two columns:
--     - TotalAmount: The calculated total cost of the order.
--     - IsStockAvailable: A boolean indicating if all items are available.
-- =============================================================================
CREATE OR REPLACE FUNCTION fn_calculate_order_total(
    p_order_id INT
) 
RETURNS TABLE (TotalAmount DECIMAL, IsStockAvailable BOOLEAN) AS $$
DECLARE
    v_item_total DECIMAL;
    v_insufficient_stock BOOLEAN;
BEGIN
    -- Calculate total and check stock availability in a single query
    SELECT
        SUM(oi.Quantity * oi.UnitPrice),
        EXISTS (
            SELECT 1
            FROM OrderItems oi
            JOIN Products p ON oi.ProductID = p.ProductID
            WHERE oi.OrderID = p_order_id AND p.StockQuantity < oi.Quantity
        )
    INTO
        v_item_total,
        v_insufficient_stock
    FROM OrderItems oi
    WHERE oi.OrderID = p_order_id;

    -- Return the results
    RETURN QUERY SELECT
        COALESCE(v_item_total, 0),
        NOT v_insufficient_stock;
END;
$$ LANGUAGE plpgsql;


-- =============================================================================
-- 2. Main Function (Caller - Persists to DB)
-- Name: fn_complete_order
-- Description: Completes a 'Pending' order. It updates stock levels,
--              sets the order status to 'Completed', and records the total amount.
-- Parameters:
--   p_order_id: The ID of the order to complete.
-- Returns:
--   A text message indicating the result (success or specific error).
-- =============================================================================
CREATE OR REPLACE FUNCTION fn_complete_order(
    p_order_id INT
)
RETURNS TEXT AS $$
DECLARE
    v_total_amount DECIMAL;
    v_is_stock_available BOOLEAN;
    v_current_status VARCHAR(20);
    v_result_message TEXT;
BEGIN
    -- Check current order status
    SELECT Status INTO v_current_status
    FROM Orders
    WHERE OrderID = p_order_id;

    -- Handle non-existent order
    IF NOT FOUND THEN
        v_result_message := 'Order not found';
        RETURN v_result_message;
    END IF;

    -- Handle order not in 'Pending' state
    IF v_current_status <> 'Pending' THEN
        v_result_message := 'Order is not in Pending status';
        RETURN v_result_message;
    END IF;

    -- Call dependency function to get calculations
    SELECT TotalAmount, IsStockAvailable
    INTO v_total_amount, v_is_stock_available
    FROM fn_calculate_order_total(p_order_id);

    -- Handle insufficient stock
    IF NOT v_is_stock_available THEN
        v_result_message := 'Insufficient stock for one or more items';
        RETURN v_result_message;
    END IF;

    -- If all checks pass, proceed with updates
    BEGIN
        -- Update stock quantities
        UPDATE Products p
        SET StockQuantity = p.StockQuantity - oi.Quantity
        FROM OrderItems oi
        WHERE p.ProductID = oi.ProductID AND oi.OrderID = p_order_id;

        -- Update order status and total amount
        UPDATE Orders
        SET Status = 'Completed',
            TotalAmount = v_total_amount
        WHERE OrderID = p_order_id;

        v_result_message := 'Order completed successfully';

    EXCEPTION
        -- In case of any error during the update transaction, roll back
        WHEN OTHERS THEN
            v_result_message := 'An unexpected error occurred. Transaction rolled back.';
            -- The transaction is automatically rolled back on exception in PL/pgSQL
            RETURN v_result_message;
    END;

    RETURN v_result_message;
END;
$$ LANGUAGE plpgsql;


-- =============================================================================
-- 3. Test Data Seeding Script for Scenario 1
-- Description: This script sets up the specific state required to test the
--              'fn_complete_order' function. It creates a new user, adds
--              products, and creates a single 'Pending' order with items.
--              This is intended to be run after the main schema and before
--              a DbFit test.
-- =============================================================================
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
    VALUES ('Laptop Dell XPS', 1200.00, 1)
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
