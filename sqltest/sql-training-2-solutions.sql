USE coffee_training_2;
-- 01 · 所有门店的员工数
SELECT s.store_id, s.store_name, COUNT(e.employee_id) AS employee_count
FROM stores s LEFT JOIN employees e ON e.store_id=s.store_id
GROUP BY s.store_id,s.store_name ORDER BY s.store_id;

USE coffee_training_2;
-- 02 · 每件商品的实际收入
SELECT p.product_id, COALESCE(SUM(s.quantity),0) AS qty,
 COALESCE(SUM(s.amount),0) AS revenue,
 ROUND(SUM(s.amount)/NULLIF(SUM(s.quantity),0),2) AS unit_revenue
FROM products p LEFT JOIN sales s ON s.product_id=p.product_id
GROUP BY p.product_id ORDER BY p.product_id;

USE coffee_training_2;
-- 03 · 每店最畅销的产品
WITH totals AS (
 SELECT store_id,product_id,SUM(quantity) AS qty FROM sales
 GROUP BY store_id,product_id
), ranked AS (
 SELECT *,DENSE_RANK() OVER(PARTITION BY store_id ORDER BY qty DESC) AS rk FROM totals
)
SELECT store_id,product_id,qty FROM ranked WHERE rk=1
ORDER BY store_id,product_id;

USE coffee_training_2;
-- 04 · 门店员工贡献榜
WITH totals AS (
 SELECT e.employee_id,e.store_id,COALESCE(SUM(s.amount),0) AS revenue
 FROM employees e LEFT JOIN sales s ON s.employee_id=e.employee_id
 GROUP BY e.employee_id,e.store_id
)
SELECT *,DENSE_RANK() OVER(PARTITION BY store_id ORDER BY revenue DESC) AS rk
FROM totals ORDER BY store_id,rk,employee_id;

USE coffee_training_2;
-- 05 · 每日收入与累计
WITH daily AS (
 SELECT sale_date AS day,SUM(amount) AS revenue FROM sales GROUP BY sale_date
)
SELECT day,revenue,SUM(revenue) OVER(
 ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
) AS running_revenue FROM daily ORDER BY day;

USE coffee_training_2;
-- 06 · 自然月环比，缺月补零
WITH months AS (
 SELECT CAST('2024-01-01' AS DATE) AS month
 UNION ALL SELECT CAST('2024-02-01' AS DATE)
 UNION ALL SELECT CAST('2024-03-01' AS DATE)
), monthly AS (
 SELECT m.month,COALESCE(SUM(s.amount),0) AS revenue
 FROM months m LEFT JOIN sales s ON s.store_id=2
 AND s.sale_date>=m.month AND s.sale_date<DATE_ADD(m.month,INTERVAL 1 MONTH)
 GROUP BY m.month
), compared AS (
 SELECT *,LAG(revenue) OVER(ORDER BY month) AS prev FROM monthly
)
SELECT month,revenue,prev,ROUND((revenue-prev)/NULLIF(prev,0)*100,2) AS growth_pct
FROM compared ORDER BY month;

USE ev_training_2;
-- 07 · 已售车辆的售后覆盖
WITH sold AS (SELECT DISTINCT vin FROM sales)
SELECT s.vin,COUNT(r.service_id) AS service_count
FROM sold s LEFT JOIN service_records r ON r.vin=s.vin
GROUP BY s.vin ORDER BY s.vin;

USE ev_training_2;
-- 08 · 顾问客户数与销售额
SELECT s.sales_rep,COUNT(DISTINCT s.customer_id) AS customer_count,
 SUM(v.sale_price) AS revenue_wan
FROM sales s JOIN vehicles v ON v.vin=s.vin
GROUP BY s.sales_rep ORDER BY s.sales_rep COLLATE utf8mb4_bin;

USE ev_training_2;
-- 09 · 购车后三个月内保养
SELECT c.customer_id,c.name FROM customers c
WHERE EXISTS (
 SELECT 1 FROM sales s WHERE s.customer_id=c.customer_id
 AND s.sale_date>='2024-01-01' AND s.sale_date<'2025-01-01'
 AND EXISTS (
  SELECT 1 FROM service_records r WHERE r.vin=s.vin AND r.service_type='保养'
  AND r.service_date>=s.sale_date
  AND r.service_date<DATE_ADD(s.sale_date,INTERVAL 3 MONTH)
 )
) ORDER BY c.customer_id;

USE ev_training_2;
-- 10 · 每车相邻服务间隔
WITH compared AS (
 SELECT *,LAG(service_date) OVER(PARTITION BY vin ORDER BY service_date,service_id) AS previous_date
 FROM service_records
)
SELECT vin,service_id,previous_date,DATEDIFF(service_date,previous_date) AS gap_days
FROM compared ORDER BY vin,service_date,service_id;

USE ev_training_2;
-- 11 · 从销售到首次售后
WITH first_service AS (
 SELECT s.sale_id,s.sale_date,MIN(r.service_date) AS first_date
 FROM sales s LEFT JOIN service_records r
 ON r.vin=s.vin AND r.service_date>=s.sale_date
 GROUP BY s.sale_id,s.sale_date
)
SELECT COUNT(first_date) AS serviced_sales,
 ROUND(AVG(DATEDIFF(first_date,sale_date)),2) AS avg_days
FROM first_service;

USE ev_training_2;
-- 12 · 不重复销售额的城市报表
WITH revenue AS (
 SELECT s.store_city,SUM(v.sale_price) AS revenue_wan
 FROM sales s JOIN vehicles v ON v.vin=s.vin GROUP BY s.store_city
), sold AS (
 SELECT DISTINCT store_city,vin FROM sales
), costs AS (
 SELECT s.store_city,COALESCE(SUM(r.cost),0) AS service_cost_yuan
 FROM sold s LEFT JOIN service_records r ON r.vin=s.vin GROUP BY s.store_city
)
SELECT a.store_city,a.revenue_wan,b.service_cost_yuan
FROM revenue a JOIN costs b ON b.store_city=a.store_city
ORDER BY a.store_city COLLATE utf8mb4_bin;

USE coffee_training_2;
-- 13 · 从未卖出的商品
SELECT p.product_id,p.product_name FROM products p
WHERE NOT EXISTS (SELECT 1 FROM sales s WHERE s.product_id=p.product_id)
ORDER BY p.product_id;

USE coffee_training_2;
-- 14 · 高于本店平均交易额
SELECT s.sale_id,s.store_id,s.amount FROM sales s
WHERE s.amount>(SELECT AVG(x.amount) FROM sales x WHERE x.store_id=s.store_id)
ORDER BY s.sale_id;

USE coffee_training_2;
-- 15 · 每店最近一条销售
WITH ranked AS (
 SELECT *,ROW_NUMBER() OVER(PARTITION BY store_id ORDER BY sale_date DESC,sale_id DESC) AS rn
 FROM sales
)
SELECT store_id,sale_id,sale_date,amount FROM ranked WHERE rn=1 ORDER BY store_id;

USE coffee_training_2;
-- 16 · 每店收入占全链比例
WITH totals AS (
 SELECT st.store_id,COALESCE(SUM(s.amount),0) AS revenue
 FROM stores st LEFT JOIN sales s ON s.store_id=st.store_id GROUP BY st.store_id
)
SELECT store_id,revenue,ROUND(revenue/NULLIF(SUM(revenue) OVER(),0)*100,2) AS share_pct
FROM totals ORDER BY store_id;

USE coffee_training_2;
-- 17 · 类别收入横向展示
SELECT st.store_id,
 SUM(CASE WHEN p.category='咖啡' THEN s.amount ELSE 0 END) AS coffee_revenue,
 SUM(CASE WHEN p.category='糕点' THEN s.amount ELSE 0 END) AS pastry_revenue
FROM stores st LEFT JOIN sales s ON s.store_id=st.store_id
LEFT JOIN products p ON p.product_id=s.product_id
GROUP BY st.store_id ORDER BY st.store_id;

USE coffee_training_2;
-- 18 · 最近三笔移动平均
SELECT store_id,sale_id,amount,
 ROUND(AVG(amount) OVER(PARTITION BY store_id ORDER BY sale_date,sale_id
 ROWS BETWEEN 2 PRECEDING AND CURRENT ROW),2) AS avg_last3
FROM sales ORDER BY store_id,sale_date,sale_id;

USE ev_training_2;
-- 19 · 车型内的售价档位
SELECT vin,model,sale_price,
 DENSE_RANK() OVER(PARTITION BY model ORDER BY sale_price DESC) AS price_rank
FROM vehicles ORDER BY vin;

USE ev_training_2;
-- 20 · 车型维修成本与覆盖
SELECT v.model,
 COUNT(CASE WHEN r.service_type='维修' THEN r.service_id END) AS repair_events,
 COUNT(DISTINCT CASE WHEN r.service_type='维修' THEN v.vin END) AS repaired_vehicles,
 ROUND(AVG(CASE WHEN r.service_type='维修' THEN r.cost END),2) AS avg_repair_cost
FROM vehicles v LEFT JOIN service_records r ON r.vin=v.vin
GROUP BY v.model ORDER BY v.model COLLATE utf8mb4_bin;

USE ev_training_2;
-- 21 · 标记首次服务
WITH ranked AS (
 SELECT *,ROW_NUMBER() OVER(PARTITION BY vin ORDER BY service_date,service_id) AS rn
 FROM service_records
)
SELECT vin,service_id,CASE WHEN rn=1 THEN 1 ELSE 0 END AS is_first
FROM ranked ORDER BY vin,service_date,service_id;

USE ev_training_2;
-- 22 · 每车服务成本累计
SELECT vin,service_id,cost,
 SUM(cost) OVER(PARTITION BY vin ORDER BY service_date,service_id
 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_cost
FROM service_records ORDER BY vin,service_date,service_id;

USE ev_training_2;
-- 23 · 多次购车客户
SELECT c.customer_id,c.name,COUNT(*) AS purchase_count,SUM(v.sale_price) AS revenue_wan
FROM customers c JOIN sales s ON s.customer_id=c.customer_id
JOIN vehicles v ON v.vin=s.vin
GROUP BY c.customer_id,c.name HAVING COUNT(*)>=2 ORDER BY c.customer_id;

USE ev_training_2;
-- 24 · 已售但从未维修的车辆
SELECT v.vin,v.model FROM vehicles v
WHERE EXISTS (SELECT 1 FROM sales s WHERE s.vin=v.vin)
AND NOT EXISTS (
 SELECT 1 FROM service_records r WHERE r.vin=v.vin AND r.service_type='维修'
) ORDER BY v.vin;