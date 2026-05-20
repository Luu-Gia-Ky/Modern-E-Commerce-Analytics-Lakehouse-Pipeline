-- Khởi tạo các schema theo chuẩn Data Warehouse
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS marts;

-- Bảng đích để Spark ghi dữ liệu Silver vào trước khi dbt xử lý
CREATE TABLE IF NOT EXISTS raw.orders (
    order_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50),
    order_date TIMESTAMP,
    product_id VARCHAR(50),
    quantity INT,
    price NUMERIC(10, 2),
    status VARCHAR(20),
    updated_at TIMESTAMP
);