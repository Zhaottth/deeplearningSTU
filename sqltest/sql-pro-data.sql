-- SQL 专业训练：独立练习库。首次运行；不包含 DROP / TRUNCATE。
-- MySQL 8.0.18+；所有样例时间按 UTC 解释，金额统一为 CNY。
CREATE DATABASE IF NOT EXISTS sql_pro_lab CHARACTER SET utf8mb4;
USE sql_pro_lab;
CREATE TABLE users(id INT PRIMARY KEY, signup_date DATE NOT NULL);
CREATE TABLE orders(id INT PRIMARY KEY,user_id INT NOT NULL,paid_at DATETIME NOT NULL,
 amount DECIMAL(12,2) NOT NULL,status VARCHAR(12) NOT NULL,
 FOREIGN KEY(user_id) REFERENCES users(id),CHECK(amount>=0));
CREATE TABLE refunds(id INT PRIMARY KEY,order_id INT NOT NULL,refunded_at DATETIME NOT NULL,
 amount DECIMAL(12,2) NOT NULL,FOREIGN KEY(order_id) REFERENCES orders(id),CHECK(amount>0));
CREATE TABLE events(id INT PRIMARY KEY,user_id INT NOT NULL,event_at DATETIME NOT NULL,
 kind VARCHAR(12) NOT NULL,FOREIGN KEY(user_id) REFERENCES users(id));
CREATE TABLE items(order_id INT NOT NULL,sku VARCHAR(12) NOT NULL,qty INT NOT NULL,
 unit_price DECIMAL(12,2) NOT NULL,PRIMARY KEY(order_id,sku),
 FOREIGN KEY(order_id) REFERENCES orders(id),CHECK(qty>0),CHECK(unit_price>=0));
CREATE TABLE employees(id INT PRIMARY KEY,manager_id INT NULL,name VARCHAR(20) NOT NULL,
 FOREIGN KEY(manager_id) REFERENCES employees(id));
INSERT INTO users VALUES (1,'2025-01-01'),(2,'2025-01-01'),(3,'2025-01-02'),(4,'2025-01-03'),(5,'2025-01-05');
INSERT INTO orders VALUES
 (101,1,'2025-01-01 09:00:00',100,'paid'),(102,1,'2025-01-02 10:00:00',100,'paid'),
 (103,2,'2025-01-02 10:00:00',200,'paid'),(104,3,'2025-01-03 12:00:00',50,'cancelled'),
 (105,2,'2025-01-04 11:00:00',300,'paid'),(106,3,'2025-01-05 09:00:00',80,'paid'),
 (107,1,'2025-01-05 09:00:00',100,'paid'),(108,4,'2025-01-07 09:00:00',120,'paid');
INSERT INTO refunds VALUES (1,101,'2025-01-03 08:00:00',20),(2,101,'2025-01-04 08:00:00',30),
 (3,103,'2025-02-01 08:00:00',200);
INSERT INTO items VALUES (101,'A',1,60),(101,'B',2,20),(102,'A',1,100),
 (103,'B',2,100),(104,'C',1,50),(105,'A',3,100),(106,'C',1,80),(107,'B',1,100),(108,'A',1,120);
INSERT INTO events VALUES
 (1,1,'2025-01-01 08:00:00','view'),(2,1,'2025-01-01 08:10:00','cart'),
 (3,1,'2025-01-01 08:40:00','pay'),(4,1,'2025-01-01 09:11:00','view'),
 (5,1,'2025-01-02 10:00:00','view'),(6,1,'2025-01-03 10:00:00','view'),
 (7,2,'2025-01-01 09:00:00','pay'),(8,2,'2025-01-01 09:05:00','view'),
 (9,2,'2025-01-03 09:00:00','view'),(10,3,'2025-01-02 09:00:00','view'),
 (11,3,'2025-01-03 09:00:00','view'),(12,4,'2025-01-03 12:00:00','view');
INSERT INTO employees VALUES (1,NULL,'CEO');
INSERT INTO employees VALUES (2,1,'研发'),(3,1,'销售');
INSERT INTO employees VALUES (4,2,'平台');
