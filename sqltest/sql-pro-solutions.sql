USE sql_pro_lab;

-- 25 · 订单生命周期净额
-- 按订单输出所有 paid 订单的 gross、refunded、net，退款取数据中全部时间；按 id 排序。
WITH r AS (SELECT order_id,SUM(amount) refunded FROM refunds GROUP BY order_id)
SELECT o.id,o.amount gross,COALESCE(r.refunded,0) refunded,o.amount-COALESCE(r.refunded,0) net
FROM orders o LEFT JOIN r ON r.order_id=o.id WHERE o.status='paid' ORDER BY o.id;

-- 26 · 明细与退款同时关联
-- 每笔 paid 订单输出件数 qty 与退款 refunded；不允许直接将两个明细连接后求和。
WITH i AS (SELECT order_id,SUM(qty) qty FROM items GROUP BY order_id),
r AS (SELECT order_id,SUM(amount) refunded FROM refunds GROUP BY order_id)
SELECT o.id,COALESCE(i.qty,0) qty,COALESCE(r.refunded,0) refunded
FROM orders o LEFT JOIN i ON i.order_id=o.id LEFT JOIN r ON r.order_id=o.id
WHERE o.status='paid' ORDER BY o.id;

-- 27 · 每人最近两笔有效订单
-- 仅 paid，按 paid_at DESC,id DESC 选每用户最近两笔；输出按 user_id、rn 排序。
WITH x AS (SELECT user_id,id,ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY paid_at DESC,id DESC) rn
FROM orders WHERE status='paid') SELECT user_id,id,rn FROM x WHERE rn<=2 ORDER BY user_id,rn;

-- 28 · 收入占比之后再筛用户
-- 先按 paid 订单毛额计算所有购买用户的收入占比，最后仅展示用户 1；百分比保留两位。
WITH a AS (SELECT user_id,SUM(amount) revenue FROM orders WHERE status='paid' GROUP BY user_id),
b AS (SELECT user_id,revenue,ROUND(100*revenue/NULLIF(SUM(revenue) OVER(),0),2) pct FROM a)
SELECT * FROM b WHERE user_id=1;

-- 29 · 日历补零与逐日累计
-- 输出 1 月 1–7 日 daily_gross、running_gross，paid 毛额、无订单日补零。
WITH RECURSIVE cal AS (SELECT DATE('2025-01-01') d UNION ALL SELECT d+INTERVAL 1 DAY FROM cal WHERE d<'2025-01-07'),
a AS (SELECT DATE(paid_at) d,SUM(amount) v FROM orders WHERE status='paid' GROUP BY DATE(paid_at))
SELECT c.d,COALESCE(a.v,0) daily_gross,SUM(COALESCE(a.v,0)) OVER(ORDER BY c.d ROWS UNBOUNDED PRECEDING) running_gross
FROM cal c LEFT JOIN a ON a.d=c.d ORDER BY c.d;

-- 30 · 三日滚动均值
-- 1 月 1–7 日，按补零收入求当前及前两日均值；起始不足三天按实际天数平均，保留两位。
WITH RECURSIVE cal AS (SELECT DATE('2025-01-01') d UNION ALL SELECT d+INTERVAL 1 DAY FROM cal WHERE d<'2025-01-07'),
a AS (SELECT DATE(paid_at) d,SUM(amount) v FROM orders WHERE status='paid' GROUP BY DATE(paid_at))
SELECT c.d,ROUND(AVG(COALESCE(a.v,0)) OVER(ORDER BY c.d ROWS BETWEEN 2 PRECEDING AND CURRENT ROW),2) avg3
FROM cal c LEFT JOIN a ON a.d=c.d ORDER BY c.d;

-- 31 · 最长连续活跃天数
-- 任意事件算活跃；先去重用户日，输出有活跃用户的最长连续天数。
WITH d AS (SELECT DISTINCT user_id,DATE(event_at) dt FROM events),
n AS (SELECT user_id,dt,ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY dt) rn FROM d),
g AS (SELECT user_id,DATE_SUB(dt,INTERVAL rn DAY) grp FROM n),
c AS (SELECT user_id,grp,COUNT(*) days FROM g GROUP BY user_id,grp)
SELECT user_id,MAX(days) longest FROM c GROUP BY user_id ORDER BY user_id;

-- 32 · 行为会话切分
-- 仅用户 1，间隔严格大于 30 分钟开新会话，恰好 30 分钟仍同会话；按时间和 id 输出会话号。
WITH p AS (SELECT id,event_at,LAG(event_at) OVER(ORDER BY event_at,id) prev FROM events WHERE user_id=1),
f AS (SELECT *,CASE WHEN prev IS NULL OR event_at>prev+INTERVAL 30 MINUTE THEN 1 ELSE 0 END fresh FROM p)
SELECT id,SUM(fresh) OVER(ORDER BY event_at,id ROWS UNBOUNDED PRECEDING) session_no FROM f ORDER BY event_at,id;

-- 33 · 注册队列 D1 留存
-- 截至 1 月 7 日（含），按 signup_date 输出注册人数、次日任意活跃人数和百分比；包含零留存队列。
WITH x AS (SELECT u.*,EXISTS(SELECT 1 FROM events e WHERE e.user_id=u.id
AND e.event_at>=u.signup_date+INTERVAL 1 DAY AND e.event_at<u.signup_date+INTERVAL 2 DAY) kept
FROM users u WHERE u.signup_date<='2025-01-06')
SELECT signup_date,COUNT(*) users,SUM(kept) retained,ROUND(100*SUM(kept)/COUNT(*),2) pct
FROM x GROUP BY signup_date ORDER BY signup_date;

-- 34 · 严格顺序漏斗
-- 找出存在 view→cart→pay 严格递增时间链、且首尾不超过一小时的用户；允许跨会话，用户只输出一次。
SELECT u.id FROM users u WHERE EXISTS (
SELECT 1 FROM events v JOIN events c ON c.user_id=v.user_id AND c.kind='cart' AND c.event_at>v.event_at
JOIN events p ON p.user_id=v.user_id AND p.kind='pay' AND p.event_at>c.event_at
WHERE v.user_id=u.id AND v.kind='view' AND p.event_at<=v.event_at+INTERVAL 1 HOUR) ORDER BY u.id;

-- 35 · 现金流与订单净额分开
-- 按月统计 paid 订单资金流入减退款流出；退款按退款日期，按月输出 net_cash。
WITH flow AS (SELECT paid_at t,amount v FROM orders WHERE status='paid'
UNION ALL SELECT r.refunded_at,-r.amount FROM refunds r JOIN orders o ON o.id=r.order_id WHERE o.status='paid')
SELECT DATE_FORMAT(t,'%Y-%m') month,SUM(v) net_cash FROM flow GROUP BY DATE_FORMAT(t,'%Y-%m') ORDER BY month;

-- 36 · 首次购买后七天复购
-- 以 paid_at,id 确定首笔 paid；输出首笔之后且不晚于首笔时间加七天的其它有效订单数，含未买用户。
WITH x AS (SELECT *,ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY paid_at,id) rn FROM orders WHERE status='paid'),
f AS (SELECT * FROM x WHERE rn=1)
SELECT u.id,COUNT(o.id) repurchases FROM users u LEFT JOIN f ON f.user_id=u.id
LEFT JOIN orders o ON o.user_id=u.id AND o.status='paid'
AND (o.paid_at>f.paid_at OR (o.paid_at=f.paid_at AND o.id>f.id))
AND o.paid_at<=f.paid_at+INTERVAL 7 DAY GROUP BY u.id ORDER BY u.id;

-- 37 · 有效订单金额中位数
-- 计算全部 paid 订单的中位数，NULL 不适用（金额非空）。
WITH x AS (SELECT amount,ROW_NUMBER() OVER(ORDER BY amount,id) rn,COUNT(*) OVER() n FROM orders WHERE status='paid')
SELECT AVG(amount) median_amount FROM x WHERE rn IN (FLOOR((n+1)/2),FLOOR((n+2)/2));

-- 38 · 前两档金额保留并列
-- 每用户取最高两个金额档位的所有 paid 订单，按 user_id、id 输出。
WITH x AS (SELECT user_id,id,amount,DENSE_RANK() OVER(PARTITION BY user_id ORDER BY amount DESC) dr FROM orders WHERE status='paid')
SELECT user_id,id,amount,dr FROM x WHERE dr<=2 ORDER BY user_id,id;

-- 39 · 复合游标分页
-- paid 订单按 paid_at DESC,id DESC 排序，已读到 107（2025-01-05 09:00:00），取后面三条。
SELECT id,paid_at FROM orders WHERE status='paid' AND
(paid_at<'2025-01-05 09:00:00' OR (paid_at='2025-01-05 09:00:00' AND id<107))
ORDER BY paid_at DESC,id DESC LIMIT 3;

-- 40 · 买过全部目标商品
-- 找出 paid 订单中买过 A 和 B 的用户，目标集合由 CTE 明确；按用户排序。
WITH target AS (SELECT 'A' sku UNION ALL SELECT 'B')
SELECT u.id FROM users u WHERE NOT EXISTS (SELECT 1 FROM target t WHERE NOT EXISTS (
SELECT 1 FROM orders o JOIN items i ON i.order_id=o.id
WHERE o.user_id=u.id AND o.status='paid' AND i.sku=t.sku)) ORDER BY u.id;

-- 41 · 买 A 但从未买 B
-- 按 paid 订单定义购买，找出买过 A 且从未买 B 的用户。
SELECT u.id FROM users u WHERE EXISTS (SELECT 1 FROM orders o JOIN items i ON i.order_id=o.id
WHERE o.user_id=u.id AND o.status='paid' AND i.sku='A')
AND NOT EXISTS (SELECT 1 FROM orders o JOIN items i ON i.order_id=o.id
WHERE o.user_id=u.id AND o.status='paid' AND i.sku='B') ORDER BY u.id;

-- 42 · 组织树路径
-- 从 CEO(id=1) 递归列出下属，含根，输出 id、depth、ID 路径，按 id 排序；限制最多 20 层并检测路径重复。
WITH RECURSIVE org AS (
SELECT id,0 depth,CAST(id AS CHAR(1000)) path FROM employees WHERE id=1
UNION ALL SELECT e.id,o.depth+1,CONCAT(o.path,',',e.id) FROM employees e JOIN org o ON e.manager_id=o.id
WHERE o.depth<20 AND FIND_IN_SET(e.id,o.path)=0)
SELECT id,depth,path FROM org ORDER BY id;

-- 43 · 区间合并的嵌套陷阱
-- 给定闭区间 [1,10]、[2,3]、[9,12]、[15,16]，重叠或端点相等就合并，输出合并区间。
WITH a AS (SELECT 1 s,10 e UNION ALL SELECT 2,3 UNION ALL SELECT 9,12 UNION ALL SELECT 15,16),
p AS (SELECT *,MAX(e) OVER(ORDER BY s,e ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) prev_max FROM a),
f AS (SELECT *,CASE WHEN prev_max IS NULL OR s>prev_max THEN 1 ELSE 0 END fresh FROM p),
g AS (SELECT *,SUM(fresh) OVER(ORDER BY s,e ROWS UNBOUNDED PRECEDING) grp FROM f)
SELECT MIN(s) start_at,MAX(e) end_at FROM g GROUP BY grp ORDER BY start_at;

-- 44 · 订单与明细对账
-- paid 订单金额应等于明细 qty*unit_price 合计，找出异常 id、header_total、line_total；无明细也算异常。
SELECT o.id,o.amount header_total,SUM(i.qty*i.unit_price) line_total FROM orders o LEFT JOIN items i ON i.order_id=o.id
WHERE o.status='paid' GROUP BY o.id,o.amount HAVING COUNT(i.order_id)=0 OR o.amount<>SUM(i.qty*i.unit_price) ORDER BY o.id;

-- 45 · 截至指定日的用户价值
-- 截至 1 月 4 日结束，输出所有用户的 paid 订单数与净额；订单和退款都必须早于 1 月 5 日。
WITH r AS (SELECT order_id,SUM(amount) v FROM refunds WHERE refunded_at<'2025-01-05' GROUP BY order_id),
a AS (SELECT o.user_id,COUNT(*) n,SUM(o.amount-COALESCE(r.v,0)) net FROM orders o LEFT JOIN r ON r.order_id=o.id
WHERE o.status='paid' AND o.paid_at<'2025-01-05' GROUP BY o.user_id)
SELECT u.id,COALESCE(a.n,0) orders_count,COALESCE(a.net,0) net FROM users u LEFT JOIN a ON a.user_id=u.id ORDER BY u.id;

-- 46 · 退款风险检查
-- 找出 paid 订单累计退款超过订单金额的记录；输出 id、amount、refunded。
SELECT o.id,o.amount,SUM(r.amount) refunded FROM orders o JOIN refunds r ON r.order_id=o.id
WHERE o.status='paid' GROUP BY o.id,o.amount HAVING SUM(r.amount)>o.amount ORDER BY o.id;

-- 47 · 商品用户渗透率
-- 按有有效销售的 sku，输出购买用户数和占全部 paid 购买用户的百分比，按 sku 排序。
WITH b AS (SELECT DISTINCT o.user_id,i.sku FROM orders o JOIN items i ON i.order_id=o.id WHERE o.status='paid'),
den AS (SELECT COUNT(DISTINCT user_id) n FROM orders WHERE status='paid')
SELECT b.sku,COUNT(*) buyers,ROUND(100*COUNT(*)/NULLIF(den.n,0),2) pct FROM b CROSS JOIN den GROUP BY b.sku,den.n ORDER BY b.sku;

-- 48 · 累计贡献达到 80%
-- 按每用户 paid 毛额降序、user_id 升序，取累计贡献首次达到或超过 80% 所需的最少前缀用户。
WITH a AS (SELECT user_id,SUM(amount) v FROM orders WHERE status='paid' GROUP BY user_id),
b AS (SELECT *,SUM(v) OVER() total,SUM(v) OVER(ORDER BY v DESC,user_id ROWS UNBOUNDED PRECEDING) running FROM a)
SELECT user_id,v,running,ROUND(100*running/NULLIF(total,0),2) cumulative_pct FROM b WHERE running-v<0.8*total ORDER BY v DESC,user_id;