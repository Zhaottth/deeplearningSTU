-- MySQL 8.0.16+；六份笔记场景的精简改编数据，不是原始全量数据。
-- 首次导入使用；表已存在会报错，请勿重复插入。两个练习库互相独立。
CREATE DATABASE IF NOT EXISTS coffee_training_2 CHARACTER SET utf8mb4;
USE coffee_training_2;
CREATE TABLE stores (store_id INT PRIMARY KEY,store_name VARCHAR(50) NOT NULL UNIQUE,city VARCHAR(30) NOT NULL,open_date DATE NOT NULL);
CREATE TABLE employees (employee_id INT PRIMARY KEY,employee_name VARCHAR(50) NOT NULL,hire_date DATE NOT NULL,position VARCHAR(30) NOT NULL,store_id INT NOT NULL,FOREIGN KEY(store_id) REFERENCES stores(store_id));
CREATE TABLE products (product_id INT PRIMARY KEY,product_name VARCHAR(50) NOT NULL UNIQUE,category VARCHAR(30) NOT NULL,price DECIMAL(10,2) NOT NULL DEFAULT 0);
CREATE TABLE sales (sale_id INT PRIMARY KEY,sale_date DATE NOT NULL,quantity INT NOT NULL DEFAULT 1,amount DECIMAL(10,2) NOT NULL,employee_id INT NOT NULL,store_id INT NOT NULL,product_id INT NOT NULL,FOREIGN KEY(employee_id) REFERENCES employees(employee_id),FOREIGN KEY(store_id) REFERENCES stores(store_id),FOREIGN KEY(product_id) REFERENCES products(product_id));
INSERT INTO stores VALUES (1,'北京店','北京','2020-01-01'),(2,'上海店','上海','2020-02-01'),(3,'杭州店','杭州','2021-01-01');
INSERT INTO employees VALUES (1,'小林','2023-01-01','店长',1),(2,'小陈','2023-02-01','店员',1),(3,'小周','2023-01-01','店长',2),(4,'小吴','2024-01-01','店员',2);
INSERT INTO products VALUES (1,'美式','咖啡',20),(2,'拿铁','咖啡',30),(3,'蛋糕','糕点',25),(4,'可颂','糕点',15);
INSERT INTO sales VALUES
(1,'2024-01-01',2,40,1,1,1),(2,'2024-01-01',2,60,2,1,2),
(3,'2024-01-02',2,60,1,1,2),(4,'2024-02-01',1,20,2,1,1),
(5,'2024-01-01',3,60,3,2,1),(6,'2024-03-01',2,50,3,2,3);

CREATE DATABASE IF NOT EXISTS ev_training_2 CHARACTER SET utf8mb4;
USE ev_training_2;
CREATE TABLE customers (customer_id INT PRIMARY KEY,name VARCHAR(50) NOT NULL,gender CHAR(1) NOT NULL,phone VARCHAR(20) NOT NULL UNIQUE,city VARCHAR(30) NOT NULL,registration_date DATE NOT NULL);
CREATE TABLE vehicles (vin VARCHAR(18) PRIMARY KEY,model VARCHAR(30) NOT NULL,brand VARCHAR(20) NOT NULL,production_date DATE NOT NULL,battery_capacity DECIMAL(5,1) NOT NULL,sale_price DECIMAL(10,2) NOT NULL);
CREATE TABLE sales (sale_id INT PRIMARY KEY,vin VARCHAR(18) NOT NULL,customer_id INT NOT NULL,sale_date DATE NOT NULL,sales_rep VARCHAR(30) NOT NULL,store_city VARCHAR(30) NOT NULL,FOREIGN KEY(vin) REFERENCES vehicles(vin),FOREIGN KEY(customer_id) REFERENCES customers(customer_id));
CREATE TABLE service_records (service_id INT PRIMARY KEY,vin VARCHAR(18) NOT NULL,service_date DATE NOT NULL,service_type VARCHAR(20) NOT NULL,cost DECIMAL(8,2) NOT NULL DEFAULT 0,description VARCHAR(200),FOREIGN KEY(vin) REFERENCES vehicles(vin));
INSERT INTO customers VALUES (1,'张伟','M','13800000001','北京','2023-01-01'),(2,'李娜','F','13800000002','上海','2023-02-01'),(3,'王强','M','13800000003','北京','2023-03-01');
INSERT INTO vehicles VALUES ('V1','Model S','GreenDrive','2023-01-01',100,30),('V2','iX3','GreenDrive','2023-01-01',80,20),('V3','Model S','GreenDrive','2023-01-01',100,30),('V4','NIO ET7','GreenDrive','2023-01-01',150,40);
INSERT INTO sales VALUES (1,'V1',1,'2024-01-01','顾问甲','北京'),(2,'V2',2,'2024-01-02','顾问乙','上海'),(3,'V3',1,'2024-02-01','顾问甲','北京');
INSERT INTO service_records VALUES (1,'V1','2024-01-11','保养',300,'首次'),(2,'V1','2024-02-10','维修',1000,'维修'),(3,'V2','2024-04-02','保养',200,'满三个月'),(4,'V2','2024-04-12','软件升级',0,NULL),(5,'V1','2024-02-10','软件升级',0,NULL);
