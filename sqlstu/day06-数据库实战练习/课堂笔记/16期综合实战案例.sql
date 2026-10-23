create database coffee_chain_db;
use coffee_chain_db;

create table stores(
    store_id int primary key auto_increment,
    store_name varchar(50) UNIQUE not null,
    city varchar(30) not null,
    open_date date not null
);

create table employees(
    employee_id int primary key auto_increment,
    employee_name varchar(50) not null,
    hire_date date not null,
    position varchar(30) not null,
    store_id int not null
);

create table products(
    product_id int primary key auto_increment,
    product_name varchar(50) UNIQUE not null,
    category varchar(30),
    price decimal(10,2) not null
);


create table sales(
    sale_id int primary key auto_increment,
    sale_date date not null,
    quantity int,
    amount decimal(10,2),
    employee_id int,
    store_id int,
    product_id int
);

insert into stores values
(1, '星光咖啡北京店', '北京', '2020-01-15'  ),
(2, '晨曦咖啡上海店', '上海', '2019-05-20'  ),
(3, '绿叶咖啡广州店', '广州', '2021-03-10'  ),
(4, '蓝天咖啡深圳店', '深圳', '2018-11-05'  ),
(5, '阳光咖啡成都店', '成都', '2022-07-25'  ),
(6, '海洋咖啡杭州店', '杭州', '2020-09-30'  ),
(7, '山峰咖啡重庆店', '重庆', '2019-02-18'  ),
(8, '河流咖啡南京店', '南京', '2021-06-12'  ),
(9, '森林咖啡武汉店', '武汉', '2018-04-08'  ),
(10, '沙漠咖啡西安店', '西安', '2022-10-22'  ),
(11, '湖泊咖啡天津店', '天津', '2020-12-01'  ),
(12, '云朵咖啡青岛店', '青岛', '2019-08-14'  ),
(13, '星星咖啡大连店', '大连', '2021-11-19'  ),
(14, '月亮咖啡厦门店', '厦门', '2018-07-03'  ),
(15, '太阳咖啡苏州店', '苏州', '2022-02-28'  ),
(16, '彩虹咖啡合肥店', '合肥', '2020-05-07'  ),
(17, '风筝咖啡济南店', '济南', '2019-10-16'  ),
(18, '雪花咖啡哈尔滨店', '哈尔滨', '2021-01-21' ),
(19, '雨滴咖啡沈阳店', '沈阳', '2018-03-09'  ),
(20, '露珠咖啡长沙店', '长沙', '2022-04-13'  ) ;

insert into employees values
(1, '李明', '2020-02-01', '店长', 1),
(2, '王芳', '2019-06-01', '服务员', 2),
(3, '张伟', '2021-04-01', '服务员', 3),
(4, '刘娜', '2018-12-01', '店长', 4),
(5, '陈浩', '2022-08-01', '服务员', 5),
(6, '孙静', '2020-10-01', '服务员', 6),
(7, '周鹏', '2019-03-01', '店长', 7),
(8, '吴晓', '2021-07-01', '服务员', 8),
(9, '郑磊', '2018-05-01', '服务员', 9),
(10, '王敏', '2022-11-01', '店长', 10),
(11, '赵阳', '2020-01-01', '服务员', 11),
(12, '钱丽', '2019-09-01', '服务员', 12),
(13, '孙杰', '2021-12-01', '店长', 13),
(14, '李娜', '2018-08-01', '服务员', 14),
(15, '周芳', '2022-03-01', '服务员', 15),
(16, '吴刚', '2020-06-01', '店长', 16),
(17, '郑梅', '2019-11-01', '服务员', 17),
(18, '王浩', '2021-02-01', '服务员', 18),
(19, '赵晓', '2018-04-01', '店长', 19),
(20, '钱伟', '2022-05-01', '服务员', 20),
(21, '孙阳', '2020-07-01', '服务员', 1),
(22, '李杰', '2019-12-01', '店长', 2),
(23, '周娜', '2021-05-01', '服务员', 3),
(24, '吴芳', '2018-09-01', '服务员', 4),
(25, '郑浩', '2022-01-01', '店长', 5),
(26, '王静', '2020-03-01', '服务员', 6),
(27, '赵鹏', '2019-04-01', '服务员', 7),
(28, '钱晓', '2021-08-01', '店长', 8),
(29, '孙磊', '2018-10-01', '服务员', 9),
(30, '李敏', '2022-06-01', '服务员', 10),
(31, '周阳', '2020-11-01', '店长', 11),
(32, '吴丽', '2019-01-01', '服务员', 12),
(33, '郑杰', '2021-03-01', '服务员', 13),
(34, '王娜', '2018-06-01', '店长', 14),
(35, '赵芳', '2022-09-01', '服务员', 15),
(36, '钱刚', '2020-04-01', '服务员', 16),
(37, '孙梅', '2019-07-01', '店长', 17),
(38, '李浩', '2021-10-01', '服务员', 18),
(39, '周晓', '2018-02-01', '服务员', 19),
(40, '吴伟', '2022-12-01', '店长', 20);





insert into products VALUES
(1, '美式咖啡', '咖啡', 18.00),
(2, '拿铁', '咖啡', 22.00),
(3, '卡布奇诺', '咖啡', 20.00),
(4, '玛奇朵', '咖啡', 25.00),
(5, ' espresso', '咖啡', 15.00),
(6, '巧克力蛋糕', '糕点', 28.00),
(7, '芝士蛋糕', '糕点', 30.00),
(8, '蓝莓松饼', '糕点', 12.00),
(9, '巧克力曲奇', '糕点', 10.00),
(10, '杏仁酥', '糕点', 8.00),
(11, '绿茶', '饮料', 15.00),
(12, '红茶', '饮料', 14.00),
(13, '果汁', '饮料', 18.00),
(14, '苏打水', '饮料', 10.00),
(15, '矿泉水', '饮料', 5.00),
(16, '三明治', '小食', 25.00),
(17, '沙拉', '小食', 20.00),
(18, '薯条', '小食', 15.00),
(19, '鸡翅', '小食', 22.00),
(20, '披萨片', '小食', 28.00),
(21, '焦糖玛奇朵', '咖啡', 26.00),
(22, '香草拿铁', '咖啡', 23.00),
(23, '榛子咖啡', '咖啡', 24.00),
(24, '提拉米苏', '糕点', 32.00),
(25, '红丝绒蛋糕', '糕点', 35.00),
(26, '柠檬茶', '饮料', 16.00),
(27, '姜茶', '饮料', 17.00),
(28, '薯片', '小食', 12.00),
(29, '坚果拼盘', '小食', 18.00),
(30, '水果沙拉', '小食', 22.00);

insert into sales values
(1, '2023-01-05', 3, 54.00, 1, 1, 1),
(2, '2023-01-10', 2, 44.00, 2, 2, 2),
(3, '2023-02-15', 1, 20.00, 3, 3, 3),
(4, '2023-02-20', 4, 100.00, 4, 4, 4),
(5, '2023-03-25', 5, 140.00, 5, 5, 6),
(6, '2023-03-30', 2, 24.00, 6, 6, 8),
(7, '2023-04-05', 3, 45.00, 7, 7, 11),
(8, '2023-04-10', 1, 10.00, 8, 8, 9),
(9, '2023-05-15', 6, 48.00, 9, 9, 10),
(10, '2023-05-20', 2, 36.00, 10, 10, 13),
(11, '2023-06-25', 4, 100.00, 11, 11, 16),
(12, '2023-06-30', 3, 60.00, 12, 12, 17),
(13, '2023-07-05', 1, 15.00, 13, 13, 18),
(14, '2023-07-10', 5, 110.00, 14, 14, 19),
(15, '2023-08-15', 2, 56.00, 15, 15, 20),
(16, '2023-08-20', 3, 69.00, 16, 16, 22),
(17, '2023-09-25', 4, 96.00, 17, 17, 23),
(18, '2023-09-30', 1, 32.00, 18, 18, 24),
(19, '2023-10-05', 2, 70.00, 19, 19, 25),
(20, '2023-10-10', 3, 48.00, 20, 20, 26),
(21, '2023-11-15', 5, 60.00, 21, 1, 27),
(22, '2023-11-20', 2, 36.00, 22, 2, 28),
(23, '2023-12-25', 4, 72.00, 23, 3, 29),
(24, '2023-12-30', 1, 22.00, 24, 4, 30),
(25, '2024-01-05', 3, 54.00, 25, 5, 1),
(26, '2024-01-10', 2, 44.00, 26, 6, 2),
(27, '2024-02-15', 6, 120.00, 27, 7, 3),
(28, '2024-02-20', 4, 100.00, 28, 8, 4),
(29, '2024-03-25', 1, 28.00, 29, 9, 6),
(30, '2024-03-30', 3, 36.00, 30, 10, 8),
(31, '2024-04-05', 2, 30.00, 31, 11, 11),
(32, '2024-04-10', 5, 50.00, 32, 12, 9),
(33, '2024-05-15', 4, 32.00, 33, 13, 10),
(34, '2024-05-20', 1, 18.00, 34, 14, 13),
(35, '2024-06-25', 3, 75.00, 35, 15, 16),
(36, '2024-06-30', 2, 40.00, 36, 16, 17),
(37, '2024-07-05', 6, 90.00, 37, 17, 18),
(38, '2024-07-10', 4, 88.00, 38, 18, 19),
(39, '2024-08-15', 1, 28.00, 39, 19, 20),
(40, '2024-08-20', 3, 78.00, 40, 20, 22),
(41, '2024-09-25', 2, 48.00, 1, 1, 23),
(42, '2024-09-30', 5, 160.00, 2, 2, 24),
(43, '2024-10-05', 4, 140.00, 3, 3, 25),
(44, '2024-10-10', 1, 16.00, 4, 4, 26),
(45, '2024-11-15', 3, 54.00, 5, 5, 27),
(46, '2024-11-20', 2, 24.00, 6, 6, 28),
(47, '2024-12-25', 6, 108.00, 7, 7, 29),
(48, '2024-12-30', 4, 88.00, 8, 8, 30),
(49, '2025-01-05', 1, 18.00, 9, 9, 1),
(50, '2025-01-10', 3, 66.00, 10, 10, 2);


select * from employees;
select * from products;
select * from sales ;
select * from stores;


# 1. 查询所有门店的名称和开业日期（单表查询）。
select store_name,open_date from stores;
# 2. 查询所有员工的姓名、职位和所属门店名称（多表查询，涉及employees和stores）。
select e.employee_name,e.position ,s.store_name from employees e
    left join stores s ON e.store_id = s.store_id;
# 3. 查询所有产品的名称、类别和价格，按价格降序排序（单表查询）。
select product_name,category , price from products order by price desc;
# 4. 查询2023年所有销售的总金额（单表查询，使用聚合函数）。
select sum(amount) from sales
    where year(sale_date) = 2023;


# 5. 查询每个门店的员工数量（多表查询，涉及employees和stores，使用GROUP BY）。
select store_name , count(e.employee_id) from stores s
    left JOIN employees e ON s.store_id = e.store_id
    GROUP BY  store_name;

# 6. 查询价格高于20元的咖啡类别产品（单表查询，使用WHERE）。
select * from products
    where category = '咖啡' and price > 20;
# 7. 查询每个产品的总销售数量和总金额（多表查询，涉及sales和products，使用GROUP BY和聚合）。
select * from products;
select * from sales;
select product_name ,sum(quantity) ,sum(amount) from products  p
    LEFT JOIN sales s ON p.product_id = s.product_id
    GROUP BY  product_name;
# 8. 查询每个员工的销售总金额，并按金额降序排序（多表查询，涉及sales和employees）。
select employee_name , sum(amount) as sum_amount from employees e
    left join sales s ON e.employee_id = s.employee_id
    GROUP BY employee_name
    order by sum_amount desc;
# 9. 查询2024年每个月的总销售金额（单表查询，使用DATE函数和GROUP BY）。
select month(sale_date) , sum(amount) from sales
    where year(sale_date) = 2024
    GROUP BY month(sale_date);
# 11. 使用窗口函数ROW_NUMBER()为每个门店的员工按入职日期排名（多表查询，涉及PARTITION BY）。
select *,
    rank() over(PARTITION BY  store_name order by hire_date)
    from stores s
    left join employees e ON s.store_id = e.store_id;

# 12. 查询每个类别的产品平均价格（单表查询，使用GROUP BY和AVG）。
select category , avg(price) from products
    GROUP BY category ;
# 13. 查询销售金额超过100元的记录，包括产品名称和员工姓名（多表查询，涉及sales、products和employees）。
select * from sales s
    left join products p ON s.product_id = p.product_id
    LEFT JOIN employees e ON s.employee_id = e.employee_id
    where amount>100;
# 14. 使用窗口函数RANK()为所有产品按价格排名（单表查询）。
select *,
       rank() over(order by price)
       from products;

# 15. 查询每个门店的总销售金额，并找出销售最高的门店（多表查询，使用GROUP BY和ORDER BY LIMIT）。
# limit 不完全准确
select s.store_name,sum(amount) sum_amount from stores s
    left join sales s2 ON s.store_id = s2.store_id
    GROUP BY  s.store_name
    order by  sum_amount desc
    limit 1;
# 排名方案
with t as (SELECT s.store_name,
                  SUM(amount)                                sum_amount,
                  RANK() OVER (ORDER BY SUM(amount) DESC) AS rank_amount
           FROM stores s
                    LEFT JOIN sales s2 ON s.store_id = s2.store_id
           GROUP BY s.store_name)
select * from t where rank_amount = 1;

# 子查询
WITH t1 as(
    select sum(amount) as sum_amount from sales GROUP BY  store_id
)
select max(sum_amount) from t1;


# 子查询 忽略
with t2 as (
    SELECT s.store_name,
                  SUM(amount)  sum_amount
           FROM stores s
                    LEFT JOIN sales s2 ON s.store_id = s2.store_id
           GROUP BY s.store_name
)
select * from t2 where sum_amount = (
    WITH t1 as(
    select sum(amount) as sum_amount from sales GROUP BY  store_id
)
select max(sum_amount) from t1)
;
# 16. 使用窗口函数LAG()查询每个销售日期的前一个销售日期的金额差异（单表查询，按日期排序）。
select sale_date,amount,
       lag(amount,1,0) OVER (order by sale_date) as lag_amount,
       amount - lag(amount,1,0) OVER () diff_amount
       from sales;
# 17. 查询员工职位为“店长”的所有信息，包括所属门店城市（多表查询）。
select * from employees e
    left join stores s ON e.store_id = s.store_id
    where e.position='店长';
# 18. 使用窗口函数NTILE(4)将所有销售记录分成4组，按金额排序（单表查询）。
select *,
       ntile(4) over( order by amount)
       from sales;

# 19. 查询每个产品的累计销售金额，使用窗口函数SUM() OVER (ORDER BY)（多表查询）。
select product_name , category,amount ,
       sum(amount)  over( PARTITION BY product_name order by sale_date) as sum_amount
    from products p
    left join sales s ON p.product_id = s.product_id;
# 20. 查询每个门店的员工销售排名，使用DENSE_RANK()窗口函数（多表查询，涉及sales、employees和stores，按门店分区）。
select s.store_id,store_name, employee_name,sum(s2.amount) 销售总金额,
    dense_rank() OVER (PARTITION BY store_name order by sum(s2.amount)) r1
    from stores s
    left join employees e ON s.store_id = e.store_id
    left join sales s2 ON e.employee_id = s2.employee_id
    GROUP BY  s.store_id,store_name, employee_name;




# 10. 查询每个门店(门店表 store)的热门(销售量sales)产品(商品表products)（销售数量最多的产品，使用多表查询和子查询）。
# 几张表关联
# 三个表关联
select * from stores s
    left join sales s2 ON s.store_id = s2.store_id
    left join products p on s2.product_id = p.product_id;

#select * from products p
#   left join sales s ON p.product_id = s.product_id
#   left join stores s2 ON s.store_id = s2.store_id;
with t as(
    select s.store_name,p.product_name,sum(quantity) as total_num from stores s
        left join sales s2 ON s.store_id = s2.store_id
        left join products p on s2.product_id = p.product_id
        group by   s.store_name,p.product_name
) , t2 as(
    select *,
       rank() over( PARTITION BY  store_name order by total_num desc) rank_num
       from t
)
select * from t2 where rank_num=1;


with t2  as(
    with t as(
    select s.store_name,p.product_name,sum(quantity) as total_num from stores s
        left join sales s2 ON s.store_id = s2.store_id
        left join products p on s2.product_id = p.product_id
        group by   s.store_name,p.product_name
)
    select *,
       rank() over( PARTITION BY  store_name order by total_num desc) rank_num
       from t

    )
select * from t2 where rank_num = 1;





with t as(
    select s.store_name,p.product_name,sum(quantity) as total_num ,
           rank() over( PARTITION BY  store_name order by sum(quantity) desc) rank_num
           from stores s
        left join sales s2 ON s.store_id = s2.store_id
        left join products p on s2.product_id = p.product_id
        group by   s.store_name,p.product_name
)
select * from t where rank_num=1;







################################################################################################
-- 创建数据库
CREATE DATABASE IF NOT EXISTS ev_sales_analytics
DEFAULT CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE ev_sales_analytics;

-- ============================================================
-- 1. 客户信息表（customers）
-- ============================================================
DROP TABLE IF EXISTS `customers`;
CREATE TABLE `customers` (
    `customer_id` INT NOT NULL AUTO_INCREMENT COMMENT '客户ID，主键，自增',
    `name` VARCHAR(50) NOT NULL COMMENT '客户姓名',
    `gender` CHAR(1) NOT NULL COMMENT '性别：M-男，F-女',
    `phone` VARCHAR(20) NOT NULL COMMENT '手机号，唯一',
    `city` VARCHAR(30) NOT NULL COMMENT '所在城市',
    `registration_date` DATE NOT NULL COMMENT '注册日期',
    PRIMARY KEY (`customer_id`),
    UNIQUE KEY `uk_phone` (`phone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='客户信息表';

-- ============================================================
-- 2. 车辆信息表（vehicles）
-- ============================================================
DROP TABLE IF EXISTS `vehicles`;
CREATE TABLE `vehicles` (
    `vin` VARCHAR(18) NOT NULL COMMENT '车辆识别码，主键',
    `model` VARCHAR(30) NOT NULL COMMENT '车型型号',
    `brand` VARCHAR(20) NOT NULL COMMENT '品牌，固定为GreenDrive',
    `production_date` DATE NOT NULL COMMENT '生产日期',
    `battery_capacity` DECIMAL(5,1) NOT NULL COMMENT '电池容量（kWh）',
    `sale_price` DECIMAL(10,2) NOT NULL COMMENT '售价（万元）',
    PRIMARY KEY (`vin`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='车辆信息表';

-- ============================================================
-- 3. 销售记录表（sales）
-- ============================================================
DROP TABLE IF EXISTS `sales`;
CREATE TABLE `sales` (
    `sale_id` INT NOT NULL AUTO_INCREMENT COMMENT '销售记录ID，主键，自增',
    `vin` VARCHAR(18) NOT NULL COMMENT '车辆识别码，外键',
    `customer_id` INT NOT NULL COMMENT '客户ID，外键',
    `sale_date` DATE NOT NULL COMMENT '销售日期',
    `sales_rep` VARCHAR(30) NOT NULL COMMENT '销售顾问姓名',
    `store_city` VARCHAR(30) NOT NULL COMMENT '销售门店所在城市',
    PRIMARY KEY (`sale_id`),
    CONSTRAINT `fk_sales_vin` FOREIGN KEY (`vin`) REFERENCES `vehicles` (`vin`),
    CONSTRAINT `fk_sales_customer` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='销售记录表';

-- ============================================================
-- 4. 售后服务表（service_records）
-- ============================================================
DROP TABLE IF EXISTS `service_records`;
CREATE TABLE `service_records` (
    `service_id` INT NOT NULL AUTO_INCREMENT COMMENT '服务记录ID，主键，自增',
    `vin` VARCHAR(18) NOT NULL COMMENT '车辆识别码，外键',
    `service_date` DATE NOT NULL COMMENT '服务日期',
    `service_type` VARCHAR(20) NOT NULL COMMENT '服务类型：保养、维修、软件升级',
    `cost` DECIMAL(8,2) NOT NULL DEFAULT 0.00 COMMENT '费用（元）',
    `description` VARCHAR(200) DEFAULT NULL COMMENT '服务描述',
    PRIMARY KEY (`service_id`),
    CONSTRAINT `fk_service_vin` FOREIGN KEY (`vin`) REFERENCES `vehicles` (`vin`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='售后服务表';

-- ============================================================
-- 5. 插入基础数据
-- ============================================================

-- 5.1 插入客户信息（35条）
INSERT INTO `customers` (`customer_id`, `name`, `gender`, `phone`, `city`, `registration_date`) VALUES
(1, '张伟', 'M', '13800138001', '北京', '2022-03-15'),
(2, '李娜', 'F', '13800138002', '上海', '2022-04-20'),
(3, '王强', 'M', '13800138003', '广州', '2022-05-10'),
(4, '刘芳', 'F', '13800138004', '深圳', '2022-06-18'),
(5, '陈明', 'M', '13800138005', '杭州', '2022-07-22'),
(6, '赵静', 'F', '13800138006', '成都', '2022-08-30'),
(7, '黄磊', 'M', '13800138007', '武汉', '2022-09-12'),
(8, '周敏', 'F', '13800138008', '西安', '2022-10-05'),
(9, '吴刚', 'M', '13800138009', '南京', '2022-11-14'),
(10, '徐丽', 'F', '13800138010', '重庆', '2022-12-01'),
(11, '孙浩', 'M', '13800138011', '天津', '2023-01-08'),
(12, '胡燕', 'F', '13800138012', '苏州', '2023-02-17'),
(13, '郭峰', 'M', '13800138013', '郑州', '2023-03-25'),
(14, '何婷', 'F', '13800138014', '长沙', '2023-04-30'),
(15, '高勇', 'M', '13800138015', '青岛', '2023-05-19'),
(16, '林雪', 'F', '13800138016', '大连', '2023-06-22'),
(17, '郑凯', 'M', '13800138017', '宁波', '2023-07-11'),
(18, '谢芳', 'F', '13800138018', '厦门', '2023-08-09'),
(19, '冯磊', 'M', '13800138019', '福州', '2023-09-03'),
(20, '邓丽', 'F', '13800138020', '济南', '2023-10-15'),
(21, '韩强', 'M', '13800138021', '合肥', '2023-11-20'),
(22, '曹敏', 'F', '13800138022', '昆明', '2023-12-05'),
(23, '彭伟', 'M', '13800138023', '南昌', '2024-01-10'),
(24, '曾静', 'F', '13800138024', '石家庄', '2024-02-14'),
(25, '吕刚', 'M', '13800138025', '太原', '2024-03-08'),
(26, '苏红', 'F', '13800138026', '哈尔滨', '2024-04-02'),
(27, '卢明', 'M', '13800138027', '长春', '2024-05-07'),
(28, '蒋芳', 'F', '13800138028', '沈阳', '2024-06-12'),
(29, '蔡勇', 'M', '13800138029', '贵阳', '2024-07-18'),
(30, '贾婷', 'F', '13800138030', '南宁', '2024-08-22'),
(31, '丁磊', 'M', '13800138031', '海口', '2024-09-05'),
(32, '魏敏', 'F', '13800138032', '兰州', '2024-10-10'),
(33, '程浩', 'M', '13800138033', '银川', '2024-11-15'),
(34, '袁丽', 'F', '13800138034', '西宁', '2024-12-01'),
(35, '潘强', 'M', '13800138035', '乌鲁木齐', '2025-01-08');

-- 5.2 插入车辆信息（42条）
INSERT INTO `vehicles` (`vin`, `model`, `brand`, `production_date`, `battery_capacity`, `sale_price`) VALUES
('VIN000000000000001', 'Model S', 'GreenDrive', '2022-02-10', 100.0, 35.80),
('VIN000000000000002', 'iX3', 'GreenDrive', '2022-03-05', 80.0, 28.50),
('VIN000000000000003', 'NIO ET7', 'GreenDrive', '2022-04-12', 150.0, 45.20),
('VIN000000000000004', 'Model S', 'GreenDrive', '2022-05-20', 100.0, 36.00),
('VIN000000000000005', 'iX3', 'GreenDrive', '2022-06-15', 80.0, 28.80),
('VIN000000000000006', 'NIO ET7', 'GreenDrive', '2022-07-08', 150.0, 45.50),
('VIN000000000000007', 'Model S', 'GreenDrive', '2022-08-22', 100.0, 35.90),
('VIN000000000000008', 'iX3', 'GreenDrive', '2022-09-30', 80.0, 28.60),
('VIN000000000000009', 'NIO ET7', 'GreenDrive', '2022-10-18', 150.0, 45.30),
('VIN000000000000010', 'Model S', 'GreenDrive', '2022-11-05', 100.0, 36.10),
('VIN000000000000011', 'iX3', 'GreenDrive', '2022-12-12', 80.0, 28.70),
('VIN000000000000012', 'NIO ET7', 'GreenDrive', '2023-01-20', 150.0, 45.40),
('VIN000000000000013', 'Model S', 'GreenDrive', '2023-02-28', 100.0, 35.85),
('VIN000000000000014', 'iX3', 'GreenDrive', '2023-03-15', 80.0, 28.55),
('VIN000000000000015', 'NIO ET7', 'GreenDrive', '2023-04-10', 150.0, 45.25),
('VIN000000000000016', 'Model S', 'GreenDrive', '2023-05-22', 100.0, 36.05),
('VIN000000000000017', 'iX3', 'GreenDrive', '2023-06-30', 80.0, 28.65),
('VIN000000000000018', 'NIO ET7', 'GreenDrive', '2023-07-18', 150.0, 45.35),
('VIN000000000000019', 'Model S', 'GreenDrive', '2023-08-05', 100.0, 35.95),
('VIN000000000000020', 'iX3', 'GreenDrive', '2023-09-12', 80.0, 28.75),
('VIN000000000000021', 'NIO ET7', 'GreenDrive', '2023-10-20', 150.0, 45.45),
('VIN000000000000022', 'Model S', 'GreenDrive', '2023-11-28', 100.0, 36.15),
('VIN000000000000023', 'iX3', 'GreenDrive', '2023-12-15', 80.0, 28.85),
('VIN000000000000024', 'NIO ET7', 'GreenDrive', '2024-01-10', 150.0, 45.55),
('VIN000000000000025', 'Model S', 'GreenDrive', '2024-02-22', 100.0, 35.88),
('VIN000000000000026', 'iX3', 'GreenDrive', '2024-03-30', 80.0, 28.58),
('VIN000000000000027', 'NIO ET7', 'GreenDrive', '2024-04-18', 150.0, 45.28),
('VIN000000000000028', 'Model S', 'GreenDrive', '2024-05-05', 100.0, 36.08),
('VIN000000000000029', 'iX3', 'GreenDrive', '2024-06-12', 80.0, 28.68),
('VIN000000000000030', 'NIO ET7', 'GreenDrive', '2024-07-20', 150.0, 45.38),
('VIN000000000000031', 'Model S', 'GreenDrive', '2024-08-28', 100.0, 35.98),
('VIN000000000000032', 'iX3', 'GreenDrive', '2024-09-15', 80.0, 28.78),
('VIN000000000000033', 'NIO ET7', 'GreenDrive', '2024-10-10', 150.0, 45.48),
('VIN000000000000034', 'Model S', 'GreenDrive', '2024-11-22', 100.0, 36.18),
('VIN000000000000035', 'iX3', 'GreenDrive', '2024-12-30', 80.0, 28.88),
('VIN000000000000036', 'NIO ET7', 'GreenDrive', '2025-01-18', 150.0, 45.58),
('VIN000000000000037', 'Model S', 'GreenDrive', '2025-02-05', 100.0, 35.82),
('VIN000000000000038', 'iX3', 'GreenDrive', '2025-03-12', 80.0, 28.52),
('VIN000000000000039', 'NIO ET7', 'GreenDrive', '2025-04-20', 150.0, 45.22),
('VIN000000000000040', 'Model S', 'GreenDrive', '2025-05-28', 100.0, 36.02),
('VIN000000000000041', 'iX3', 'GreenDrive', '2025-06-15', 80.0, 28.62),
('VIN000000000000042', 'NIO ET7', 'GreenDrive', '2025-07-10', 150.0, 45.32);

-- 5.3 插入销售记录（42条）
INSERT INTO `sales` (`sale_id`, `vin`, `customer_id`, `sale_date`, `sales_rep`, `store_city`) VALUES
(1, 'VIN000000000000001', 1, '2022-03-20', '李销售', '北京'),
(2, 'VIN000000000000002', 2, '2022-04-25', '王顾问', '上海'),
(3, 'VIN000000000000003', 3, '2022-05-15', '张经理', '广州'),
(4, 'VIN000000000000004', 4, '2022-06-22', '刘专员', '深圳'),
(5, 'VIN000000000000005', 5, '2022-07-25', '陈销售', '杭州'),
(6, 'VIN000000000000006', 6, '2022-08-30', '赵顾问', '成都'),
(7, 'VIN000000000000007', 7, '2022-09-15', '黄经理', '武汉'),
(8, 'VIN000000000000008', 8, '2022-10-10', '周专员', '西安'),
(9, 'VIN000000000000009', 9, '2022-11-18', '吴销售', '南京'),
(10, 'VIN000000000000010', 10, '2022-12-05', '徐顾问', '重庆'),
(11, 'VIN000000000000011', 11, '2023-01-12', '孙经理', '天津'),
(12, 'VIN000000000000012', 12, '2023-02-20', '胡专员', '苏州'),
(13, 'VIN000000000000013', 13, '2023-03-28', '郭销售', '郑州'),
(14, 'VIN000000000000014', 14, '2023-04-30', '何顾问', '长沙'),
(15, 'VIN000000000000015', 15, '2023-05-22', '高经理', '青岛'),
(16, 'VIN000000000000016', 16, '2023-06-25', '林专员', '大连'),
(17, 'VIN000000000000017', 17, '2023-07-15', '郑销售', '宁波'),
(18, 'VIN000000000000018', 18, '2023-08-12', '谢顾问', '厦门'),
(19, 'VIN000000000000019', 19, '2023-09-08', '冯经理', '福州'),
(20, 'VIN000000000000020', 20, '2023-10-18', '邓专员', '济南'),
(21, 'VIN000000000000021', 21, '2023-11-25', '韩销售', '合肥'),
(22, 'VIN000000000000022', 22, '2023-12-10', '曹顾问', '昆明'),
(23, 'VIN000000000000023', 23, '2024-01-15', '彭经理', '南昌'),
(24, 'VIN000000000000024', 24, '2024-02-18', '曾专员', '石家庄'),
(25, 'VIN000000000000025', 25, '2024-03-12', '吕销售', '太原'),
(26, 'VIN000000000000026', 26, '2024-04-05', '苏顾问', '哈尔滨'),
(27, 'VIN000000000000027', 27, '2024-05-10', '卢经理', '长春'),
(28, 'VIN000000000000028', 28, '2024-06-15', '蒋专员', '沈阳'),
(29, 'VIN000000000000029', 29, '2024-07-22', '蔡销售', '贵阳'),
(30, 'VIN000000000000030', 30, '2024-08-25', '贾顾问', '南宁'),
(31, 'VIN000000000000031', 31, '2024-09-08', '丁经理', '海口'),
(32, 'VIN000000000000032', 32, '2024-10-12', '魏专员', '兰州'),
(33, 'VIN000000000000033', 33, '2024-11-18', '程销售', '银川'),
(34, 'VIN000000000000034', 34, '2024-12-05', '袁顾问', '西宁'),
(35, 'VIN000000000000035', 35, '2025-01-12', '潘经理', '乌鲁木齐'),
(36, 'VIN000000000000036', 1, '2025-02-20', '李销售', '北京'),
(37, 'VIN000000000000037', 2, '2025-03-25', '王顾问', '上海'),
(38, 'VIN000000000000038', 3, '2025-04-30', '张经理', '广州'),
(39, 'VIN000000000000039', 4, '2025-05-15', '刘专员', '深圳'),
(40, 'VIN000000000000040', 5, '2025-06-18', '陈销售', '杭州'),
(41, 'VIN000000000000041', 6, '2025-07-22', '赵顾问', '成都'),
(42, 'VIN000000000000042', 7, '2025-08-05', '黄经理', '武汉');

-- 5.4 插入售后服务记录（38条）
INSERT INTO `service_records` (`service_id`, `vin`, `service_date`, `service_type`, `cost`, `description`) VALUES
(1, 'VIN000000000000001', '2022-06-10', '保养', 300.00, '首次保养'),
(2, 'VIN000000000000001', '2022-12-15', '软件升级', 0.00, '免费OTA升级'),
(3, 'VIN000000000000002', '2022-07-20', '保养', 280.00, '常规保养'),
(4, 'VIN000000000000003', '2022-08-05', '维修', 1200.00, '电池管理系统故障'),
(5, 'VIN000000000000004', '2022-09-12', '保养', 300.00, '首次保养'),
(6, 'VIN000000000000005', '2022-10-18', '软件升级', 0.00, '免费OTA升级'),
(7, 'VIN000000000000006', '2022-11-22', '维修', 800.00, '充电接口故障'),
(8, 'VIN000000000000007', '2022-12-30', '保养', 300.00, '常规保养'),
(9, 'VIN000000000000008', '2023-01-15', '保养', 280.00, '首次保养'),
(10, 'VIN000000000000009', '2023-02-20', '软件升级', 0.00, '免费OTA升级'),
(11, 'VIN000000000000010', '2023-03-25', '维修', 1500.00, '电机异响'),
(12, 'VIN000000000000011', '2023-04-30', '保养', 300.00, '常规保养'),
(13, 'VIN000000000000012', '2023-05-18', '保养', 300.00, '首次保养'),
(14, 'VIN000000000000013', '2023-06-22', '软件升级', 0.00, '免费OTA升级'),
(15, 'VIN000000000000014', '2023-07-15', '维修', 900.00, '空调系统故障'),
(16, 'VIN000000000000015', '2023-08-10', '保养', 280.00, '常规保养'),
(17, 'VIN000000000000016', '2023-09-05', '保养', 300.00, '首次保养'),
(18, 'VIN000000000000017', '2023-10-12', '软件升级', 0.00, '免费OTA升级'),
(19, 'VIN000000000000018', '2023-11-18', '维修', 1100.00, '刹车系统升级'),
(20, 'VIN000000000000019', '2023-12-22', '保养', 300.00, '常规保养'),
(21, 'VIN000000000000020', '2024-01-15', '保养', 280.00, '首次保养'),
(22, 'VIN000000000000021', '2024-02-20', '软件升级', 0.00, '免费OTA升级'),
(23, 'VIN000000000000022', '2024-03-25', '维修', 1300.00, '电池冷却系统故障'),
(24, 'VIN000000000000023', '2024-04-30', '保养', 300.00, '常规保养'),
(25, 'VIN000000000000024', '2024-05-18', '保养', 300.00, '首次保养'),
(26, 'VIN000000000000025', '2024-06-22', '软件升级', 0.00, '免费OTA升级'),
(27, 'VIN000000000000026', '2024-07-15', '维修', 700.00, '车载屏幕故障'),
(28, 'VIN000000000000027', '2024-08-10', '保养', 280.00, '常规保养'),
(29, 'VIN000000000000028', '2024-09-05', '保养', 300.00, '首次保养'),
(30, 'VIN000000000000029', '2024-10-12', '软件升级', 0.00, '免费OTA升级'),
(31, 'VIN000000000000030', '2024-11-18', '维修', 1000.00, '轮胎更换'),
(32, 'VIN000000000000031', '2024-12-22', '保养', 300.00, '常规保养'),
(33, 'VIN000000000000032', '2025-01-15', '保养', 280.00, '首次保养'),
(34, 'VIN000000000000033', '2025-02-20', '软件升级', 0.00, '免费OTA升级'),
(35, 'VIN000000000000034', '2025-03-25', '维修', 1400.00, '自动驾驶模块校准'),
(36, 'VIN000000000000035', '2025-04-30', '保养', 300.00, '常规保养'),
(37, 'VIN000000000000036', '2025-05-18', '保养', 300.00, '首次保养'),
(38, 'VIN000000000000037', '2025-06-22', '软件升级', 0.00, '免费OTA升级');

-- 验证数据插入结果
SELECT 'customers' AS table_name, COUNT(*) AS record_count FROM customers
UNION ALL
SELECT 'vehicles', COUNT(*) FROM vehicles
UNION ALL
SELECT 'sales', COUNT(*) FROM sales
UNION ALL
SELECT 'service_records', COUNT(*) FROM service_records;



# customers  客户表  sales 销售表 service_records 服务记录 vehicles车辆信息表
# 1. 单表-客户**：统计各城市的客户数量，按数量降序排列。
select * from customers;
select city , count(*) from customers GROUP BY  city;

# 2. **单表-车辆**：查询所有车辆的型号、电池容量及售价，按售价从高到低排序。
select model , battery_capacity , sale_price from vehicles v order by sale_price desc;
# 3. **单表-销售**：计算2023年每月的销售数量（按月份分组）。
select month(sale_date), count(*) from sales where  year(sale_date) = 2023
    GROUP BY  month(sale_date) ;
# 4. **单表-服务**：统计各类售后服务（保养/维修/软件升级）的总次数。
select service_type,count(*) from service_records sr
    group by service_type;
# 5. **单表-服务**：找出单次维修成本最高的3条记录。
select * from service_records
    where service_type = '维修'
    order by cost desc
    limit 3 ;
# 6. **多表-客户+销售**：查询每位客户的姓名、所在城市及购车日期（需连接 `customers` 和 `sales`）。
select c.name,c.city , s.sale_date , sale_id from customers c
    left join sales s ON c.customer_id = s.customer_id;
# 7. **多表-车辆+销售**：列出所有已售车辆的VIN、型号、销售日期及销售的城市。
select s.vin, v.model,sale_date,s.store_city from sales s
    left join vehicles v on s.vin = v.vin;
# 8. **多表-销售+服务**：统计每辆车（VIN）的售后服务次数（包括0次）。
select v.vin,count(sr.service_id) from vehicles v
    left join service_records sr ON v.vin = sr.vin
    group by v.vin;
# 9. **多表-客户+车辆+销售**：查询购买“NIO ET7”车型的客户姓名及所在城市。
select c.name , c.city , s.store_city
    from customers c
    left join sales s ON c.customer_id = s.customer_id
    left join vehicles v on s.vin = v.vin
    where v.model= 'NIO ET7';
# 10. **多表-车辆+服务**：计算各车型（model）的平均维修成本（仅含维修类型）。
select model , avg(sr.cost) from vehicles v
    left join service_records sr ON v.vin = sr.vin
    where service_type='维修'
    group by model;
# 11. **窗口函数-销售**：为每笔销售记录按销售日期排序，显示“当日累计销售额”（使用 `SUM() OVER()`）。
select *,
       sum(sale_price) over(PARTITION BY sale_date order by sale_date )
       from sales s
    left join vehicles v ON s.vin=v.vin;
# 12. **窗口函数-客户**：按客户注册日期排序，显示每位客户的“注册排名”（使用 `ROW_NUMBER()`）。
select *,
       row_number() over( order by registration_date ) as 注册排名
       from customers;

# 13. **窗口函数-车辆**：对每款车型（model）按售价降序排列，显示“车型内售价排名”（使用 `RANK()`）。
select *,
       rank() over(PARTITION BY  model order by sale_price desc) as r1
from vehicles v;
# 14. **窗口函数-服务**：计算每辆车（VIN）每次服务与上一次服务的间隔天数（使用 `LAG()`）。

select *,
       lag(service_date) over( PARTITION BY  vin) 前一次的服务日期,
       datediff(service_date ,  lag(service_date) over( PARTITION BY  vin order by service_date)   )
       from service_records;

# 16. **多表+聚合**：查询每个销售顾问（sales_rep）负责的客户数量及总销售额。
select s.sales_rep,count(customer_id),sum(sale_price) from sales s
    left join vehicles v ON  s.vin = v.vin
    group by s.sales_rep;
# 17. **多表+条件**：找出2024年购买车辆且在3个月内进行过保养的客户姓名。
select * from  sales;
select * from service_records;
select * from customers;

select *
    from sales s
    inner join service_records sr  on s.vin = sr.vin
    inner join customers c on c.customer_id = s.customer_id
    where year(s.sale_date) = 2024 and description='首次保养'
    and datediff(service_date , sale_date  ) <= 90;
    #and dateadd(sale_date , INTERVAL 3 MONTH ) >= service_date

# 18. **多表+分组**：按车型和城市分组，统计各城市各车型的销量。
select v.model , s.store_city , count(*) from sales s
    left join vehicles v on s.vin = v.vin
    group by v.model , s.store_city;
# 19. **窗口函数+条件**：对每辆车（VIN）的服务记录按日期排序，标记“是否首次服务”（使用 `ROW_NUMBER()` 判断）。
with t as (select *,
       row_number() over(PARTITION BY  vin order by service_date) as r1
from service_records
)
select *,if(r1=1 ,'是' , '否') as 是否首次服务 from t;



select *,
       case when row_number() over( PARTITION BY  vin order by service_date ) = 1 then '是' else '否' end as 是否首次
from service_records;

select *,
    case
        when  min(sr.service_date) over( PARTITION BY  v.vin ) = service_date  then '是' else '否'
    end as is_first_service
from vehicles v
    inner join service_records sr ON v.vin = sr.vin;




# 20. **综合指标**：计算客户从购车到首次售后服务的平均天数（需连接 `sales` 和 `service_records`，并用窗口函数取首次服务）。
with t as(
    select s.*, sr.service_date,
        min(service_date) over(PARTITION BY s.vin) as first_time,
        datediff(min(service_date) over(PARTITION BY s.vin) ,sale_date )  as diff_time
       from sales s
    left join service_records sr on s.vin = sr.vin
)
select avg(diff_time)  from t  where service_date = first_time ;


# 15. **多表+窗口函数**：统计各销售城市2023年的月度销售量，并显示“该城市历史最高月销量”（使用 `MAX() OVER(PARTITION BY ...)`）。
#15.1 统计各销售城市2023年的月度销售量
select store_city,month(sale_date),count(*) from sales s
    where year(sale_date) = 2023
    group by store_city,month(sale_date);

#15.2 该城市历史最高月销量
#15.2.1 统计了 所有的年份 月份 各城市的销量
select s.store_city,year(sale_date),month(sale_date) , count(*) as c
    from sales s
    GROUP BY s.store_city,year(sale_date),month(sale_date);
#15.2.2 统计了 所有的年份 月份 各城市的最高销量
with temp as (
    with t as (
        select s.store_city,year(sale_date),month(sale_date) , count(*) as c
            from sales s
            GROUP BY s.store_city,year(sale_date),month(sale_date)
    )
    select *,max(c) over(PARTITION BY  store_city) history_sale from t
)
select * from temp where c=history_sale;



# 综合
with t1 as(
    with temp as (
        with t as (
            select s.store_city,year(sale_date),month(sale_date) , count(*) as c
                from sales s
                GROUP BY s.store_city,year(sale_date),month(sale_date)
        )
        select *,max(c) over(PARTITION BY  store_city) history_sale from t
    )
    select * from temp where c=history_sale
), t2 as(
    select store_city,month(sale_date),count(*) from sales s
        where year(sale_date) = 2023
        group by store_city,month(sale_date)
)
select * from t2
    left join t1  on t1.store_city = t2.store_city;



#其他方案
select store_city,month(sale_date),count(*) from sales s
    where year(sale_date) = 2023
    group by store_city,month(sale_date);






WITH monthly_sales AS (
    SELECT
        store_city,
        YEAR(sale_date) AS sale_year,
        MONTH(sale_date) AS sale_mon,
        COUNT(*) AS count_sale
    FROM sales
    GROUP BY store_city, YEAR(sale_date), MONTH(sale_date)
),
monthly_with_history_max AS (
    SELECT
        *,
        MAX(count_sale) OVER (PARTITION BY store_city) AS max_mon_sale
    FROM monthly_sales
)
SELECT
    store_city,
    sale_mon,
    count_sale,
    max_mon_sale
FROM monthly_with_history_max
WHERE sale_year = 2023
ORDER BY store_city, sale_mon;



-- 销售表每年每月的按城市统计销量
with temp1 as (
    SELECT store_city,year(sale_date) 年份,month(sale_date) 月份,count(sale_id) num from sales
    group by store_city,year(sale_date) ,month(sale_date)
),
-- 添加最高月销量列
 temp2 as (
    select *, max(num) over(partition by store_city,月份) 该城市历史最高月销量 from temp1
 )
select * from temp2 where 年份 = 2023 order by store_city;



WITH t_2023 AS (
    -- 1. 提取2023年的销售数据
    SELECT
        store_city,
        MONTH(sale_date) AS mon,
        COUNT(*) AS monthly_sales
    FROM sales
    WHERE YEAR(sale_date) = 2023
    GROUP BY store_city, MONTH(sale_date)
),
t_history AS (
    -- 2. 提取所有历史数据，按城市和年月统计月销量
    SELECT
        store_city,
        YEAR(sale_date) AS ye,
        MONTH(sale_date) AS mon,
        COUNT(*) AS monthly_sales
    FROM sales
    GROUP BY store_city, YEAR(sale_date), MONTH(sale_date)
)
-- 3. 关联2023年数据与历史数据，并使用窗口函数计算历史最高月销量
SELECT
    distinct
    t_2023.store_city,
    t_2023.mon,
    t_2023.monthly_sales AS sales_2023,
    MAX(t_history.monthly_sales) OVER (PARTITION BY t_history.store_city) AS hist_max_monthly_sales
FROM t_2023
JOIN t_history
    ON t_2023.store_city = t_history.store_city
    AND t_2023.mon = t_history.mon;



with t as (
select store_city,date_format(sale_date,'%Y-%m') 日期,count(*) 月销量
from sales s
left join vehicles v on s.vin = v.vin
group by store_city,date_format(sale_date,'%Y-%m')),
 t2 as (
select *,max(月销量)over(partition by store_city ) 历史最高月销量
from t)
select * from t2
where t2.日期 like '2023%';









