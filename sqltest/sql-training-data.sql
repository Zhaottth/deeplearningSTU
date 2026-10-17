-- MySQL 8.0.16+，请在独立练习环境运行。首次导入使用。
-- 不删除已有表；若已导入，请勿重复执行 INSERT。
CREATE DATABASE IF NOT EXISTS sql_training_lab CHARACTER SET utf8mb4;
USE sql_training_lab;
CREATE TABLE customers (
  id INT PRIMARY KEY,
  name VARCHAR(50) NOT NULL
);
CREATE TABLE orders (
  id INT PRIMARY KEY,
  customer_id INT NOT NULL,
  amount DECIMAL(10,2) NOT NULL CHECK (amount >= 0),
  status VARCHAR(10) NOT NULL,
  created_at DATETIME NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES customers(id)
);
INSERT INTO customers (id,name) VALUES
  (1,'林晨'),(2,'陈悦'),(3,'王宁'),(4,'周禾');
INSERT INTO orders (id,customer_id,amount,status,created_at) VALUES
  (101,1,100.00,'paid','2026-01-01 10:00:00'),
  (102,1,200.00,'paid','2026-01-02 10:00:00'),
  (103,1,50.00,'refunded','2026-01-02 12:00:00'),
  (104,2,200.00,'paid','2026-01-01 11:00:00'),
  (105,2,200.00,'paid','2026-01-03 09:00:00'),
  (106,3,80.00,'pending','2026-01-02 10:00:00'),
  (107,1,200.00,'paid','2026-01-03 09:00:00'),
  (108,2,50.00,'paid','2026-01-03 09:00:00');
