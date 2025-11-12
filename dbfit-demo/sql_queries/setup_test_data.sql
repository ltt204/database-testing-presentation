-- Stored Procedure: Setup Test Data for Regression Testing
CREATE OR REPLACE PROCEDURE usp_SetupTestData()
LANGUAGE plpgsql AS $$
DECLARE
    sp_UserID INT;
    sp_OrderID INT;
BEGIN
    -- Insert test user
    INSERT INTO Users (Email, FullName) VALUES ('regtest@example.com', 'Regression Test User')
    RETURNING UserID INTO sp_UserID;

    -- Insert test products
    INSERT INTO Products (ProductName, UnitPrice, StockQuantity) VALUES
    ('Widget', 100.00, 50),
    ('Gadget', 200.00, 30);

    -- Insert test order
    INSERT INTO Orders (UserID, Status) VALUES (sp_UserID, 'Pending')
    RETURNING OrderID INTO sp_OrderID;

    -- Optionally, you can add more test data here if needed
END;
$$;

-- Grant execute permission to relevant roles
GRANT EXECUTE ON PROCEDURE usp_SetupTestData() TO PUBLIC;