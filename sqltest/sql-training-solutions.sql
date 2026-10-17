USE sql_training_lab;

-- 1. 01 · 找到高金额支付订单
SELECT id, amount
FROM orders
WHERE status = 'paid' AND amount >= 200
ORDER BY amount DESC, id ASC;

-- 2. 02 · 谁是高价值客户？
SELECT customer_id, SUM(amount) AS revenue
FROM orders
WHERE status = 'paid'
GROUP BY customer_id
HAVING SUM(amount) >= 450
ORDER BY revenue DESC, customer_id;

-- 3. 03 · 所有客户都要出现在报表里
SELECT c.id, c.name, COUNT(o.id) AS paid_count,
       COALESCE(SUM(o.amount), 0) AS revenue
FROM customers c
LEFT JOIN orders o
  ON o.customer_id = c.id AND o.status = 'paid'
GROUP BY c.id, c.name
ORDER BY c.id;

-- 4. 04 · 找出从未下单的客户
SELECT c.id, c.name
FROM customers c
WHERE NOT EXISTS (
  SELECT 1 FROM orders o WHERE o.customer_id = c.id
)
ORDER BY c.id;

-- 5. 05 · 每位客户最近的一笔支付
WITH ranked AS (
  SELECT customer_id, id, amount,
    ROW_NUMBER() OVER (
      PARTITION BY customer_id
      ORDER BY created_at DESC, id DESC
    ) AS rn
  FROM orders WHERE status = 'paid'
)
SELECT customer_id, id, amount
FROM ranked WHERE rn = 1
ORDER BY customer_id;

-- 6. 06 · 每日收入与累计收入
WITH daily AS (
  SELECT DATE(created_at) AS day, SUM(amount) AS revenue
  FROM orders WHERE status = 'paid'
  GROUP BY DATE(created_at)
)
SELECT day, revenue,
  SUM(revenue) OVER (
    ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_revenue
FROM daily ORDER BY day;

-- 7. 07 · 每个客户金额最高的两个档位
WITH ranked AS (
  SELECT customer_id, id, amount,
    DENSE_RANK() OVER (
      PARTITION BY customer_id ORDER BY amount DESC
    ) AS amount_rank
  FROM orders WHERE status = 'paid'
)
SELECT customer_id, id, amount, amount_rank
FROM ranked WHERE amount_rank <= 2
ORDER BY customer_id, amount_rank, id;

-- 8. 08 · 对比每位客户前一笔消费
WITH compared AS (
  SELECT customer_id, id, amount, created_at,
    LAG(amount) OVER (
      PARTITION BY customer_id ORDER BY created_at, id
    ) AS previous_amount
  FROM orders WHERE status = 'paid'
)
SELECT customer_id, id, amount, previous_amount,
       amount - previous_amount AS delta
FROM compared
ORDER BY customer_id, created_at, id;