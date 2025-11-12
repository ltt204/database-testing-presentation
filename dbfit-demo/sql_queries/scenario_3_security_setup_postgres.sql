-- Kịch bản 3: Thiết lập Bảo mật và RLS cho PostgreSQL

-- 1. DỌN DẸP MÔI TRƯỜNG CŨ

-- Bước 1: Ngắt mọi kết nối đang hoạt động từ các user test
-- Điều này BẮT BUỘC để có thể DROP ROLE
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE usename IN ('ordermanager', 'readonlyuser', 'customeruser');

-- Bước 2: Xóa các đối tượng phụ thuộc (Policy, Function)
DROP POLICY IF EXISTS "OrdersSecurityPolicy" ON "orders";
DROP FUNCTION IF EXISTS fn_security_predicate_orders(integer);
DROP PROCEDURE IF EXISTS usp_set_user_context(integer);

-- Bước 3: Thu hồi quyền
REVOKE ALL PRIVILEGES ON TABLE "orders", "orderitems", "products", "users" FROM "ordermanagers";
REVOKE ALL PRIVILEGES ON TABLE "orders", "orderitems", "products", "users" FROM "readers";

-- Bước 4: Xóa USER (member) TRƯỚC, sau đó mới xóa GROUP ROLE
DROP ROLE IF EXISTS "ordermanager", "readonlyuser", "customeruser";
DROP ROLE IF EXISTS "ordermanagers", "readers";


-- 2. TẠO NGƯỜI DÙNG VÀ VAI TRÒ (Giữ nguyên như cũ)
CREATE USER "ordermanager" WITH PASSWORD 'Pass@123';
CREATE USER "readonlyuser" WITH PASSWORD 'Pass@123';
CREATE USER "customeruser" WITH PASSWORD 'Pass@123'; 

CREATE ROLE "ordermanagers";
CREATE ROLE "readers";

GRANT "ordermanagers" TO "ordermanager";
GRANT "readers" TO "readonlyuser";

-- 3. CẤP QUYỀN
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE "orders", "orderitems" TO "ordermanagers";
GRANT USAGE, SELECT ON SEQUENCE "orders_orderid_seq" TO "ordermanagers";
GRANT SELECT, UPDATE ON TABLE "products" TO "ordermanagers";

GRANT SELECT ON TABLE "orders", "orderitems", "products", "users" TO "readers";

GRANT SELECT, INSERT, UPDATE ON TABLE "orders" TO "customeruser";
GRANT SELECT, INSERT, UPDATE ON TABLE "orderitems" TO "customeruser";
GRANT SELECT ON TABLE "products", "users" TO "customeruser";
GRANT USAGE, SELECT ON SEQUENCE "orders_orderid_seq" TO "customeruser";

-- 4. THIẾT LẬP RLS 
ALTER TABLE "orders" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "orders" FORCE ROW LEVEL SECURITY;

CREATE OR REPLACE FUNCTION fn_security_predicate_orders(user_id_to_check integer)
RETURNS boolean AS $$
BEGIN
    IF pg_has_role(current_user, 'ordermanagers', 'member') THEN
        RETURN TRUE;
    END IF;
    RETURN user_id_to_check = current_setting('app.current_user_id', true)::integer;
END;
$$ LANGUAGE plpgsql;

CREATE POLICY "OrdersSecurityPolicy" ON "orders"
    FOR ALL
    TO PUBLIC
    USING (fn_security_predicate_orders("userid"))
    WITH CHECK (fn_security_predicate_orders("userid"));

-- 5. DỮ LIỆU TEST
TRUNCATE TABLE "users", "products", "orders", "orderitems" RESTART IDENTITY CASCADE;

INSERT INTO "users" ("email", "fullname") VALUES
('customer1@example.com', 'Customer One'),
('customer2@example.com', 'Customer Two');

INSERT INTO "products" ("productname", "unitprice", "stockquantity") VALUES
('Product A', 50.00, 100);
-- ON CONFLICT ("productname") DO NOTHING;

INSERT INTO "orders" ("userid", "status", "totalamount") VALUES
(1, 'Pending', 100.00),  -- OrderID = 1
(2, 'Completed', 150.00); -- OrderID = 2

INSERT INTO "orderitems" ("orderid", "productid", "quantity", "unitprice") VALUES
(1, 1, 2, 50.00),
(2, 1, 3, 50.00);