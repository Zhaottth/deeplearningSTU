from pathlib import Path
import json,re,html

ROOT=Path(__file__).resolve().parent.parent
bank=[]
sources=['单表查询.md','多表查询.md','MySQL函数.md','MySQL函数.md · 开窗函数','MySQL索引和函数.md','day08_数据分析综合实战1.md / 实战2.md']
topics=['单表查询与聚合','多表与子查询','内置函数与条件','窗口函数与分析','索引与备份','业务指标与口径']
def q(t,p,opts,a,e):
    bank.append(dict(topic=topics[t],type='m' if isinstance(a,list) else 's',q=html.escape(p),o=opts.split('|'),a=a if isinstance(a,list) else [a],e=html.escape(e)+'<br><span class="muted">依据：'+sources[t]+'</span>'))

q(0,'价格为 10、20、NULL 的三行，COUNT(*)、COUNT(price)、AVG(price) 分别是？','3、3、10|3、2、15|2、2、15|3、2、10',1,'COUNT(*) 数行，COUNT(price) 与 AVG(price) 忽略 NULL；平均值为 30/2。')
q(0,'查询各类别均价，只保留均价大于 100 的类别。应在哪一步过滤均价？','WHERE AVG(price)>100|HAVING AVG(price)>100|LIMIT 100|ON AVG(price)>100',1,'先 GROUP BY category_id 聚合，再 HAVING 过滤分组。')
q(0,'筛选“自营且价格在 100~200，或评分为空”的商品，哪个条件符合口径？',"is_self='自营' AND (price BETWEEN 100 AND 200 OR score IS NULL)|(is_self='自营' AND price BETWEEN 100 AND 200) OR score IS NULL|price>100 AND price<200|score=NULL",1,'评分为空的商品不要求自营；BETWEEN 包含两端。')
q(0,'每页 10 条，按 price DESC,id ASC 排序后取第 3 页，使用？','LIMIT 3,10|LIMIT 30,10|LIMIT 20,10|LIMIT 10,20',2,'偏移量=(页码-1)×每页数量。唯一 id 作为第二排序键能稳定处理同价商品。')
q(0,'关于 DISTINCT，哪些正确？','SELECT DISTINCT name,price 对字段组合去重|DISTINCT 会修改原表|同名不同价的行可能同时保留|DISTINCT 自动保证结果排序',[0,2],'DISTINCT 作用于选出的一整组列，不修改原表，也不保证顺序。')
q(0,"LIKE '_茶%' 可以匹配以下哪些值？",'红茶|茶|冰茶拿铁|奶香茶',[0,2],'下划线匹配一个字符，百分号匹配零个或多个字符；第二个字符必须是茶。')
q(0,'一张空表执行 SELECT COUNT(*), SUM(amount) FROM sales，结果是？','没有结果行|0、0|0、NULL|NULL、NULL',2,'没有 GROUP BY 的整体聚合仍返回一行；SUM 可用 COALESCE 补零。')
q(0,'同一查询层级中，筛选价格大于 100，再统计每类数量，正确的逻辑理解顺序是？','GROUP BY → WHERE → HAVING|WHERE → GROUP BY → HAVING|HAVING → WHERE → GROUP BY|LIMIT → GROUP BY → WHERE',1,'WHERE 过滤明细，GROUP BY 聚合，HAVING 过滤分组。这是逻辑理解顺序，不是物理执行计划。')
q(0,'SELECT category_id,name,AVG(price) FROM products GROUP BY category_id；name 不依赖 category_id。在 ONLY_FULL_GROUP_BY 下？','必取最贵商品名|必取最便宜商品名|通常报错，应重新定义名称粒度|自动拼接所有名称',2,'非聚合列需要满足分组或函数依赖要求；类别下有多个商品名，不能任取一个代表。')
q(0,'统计每类“有评分商品数”和“全部商品数”，应使用？','COUNT(score)、COUNT(*)|COUNT(*)、COUNT(score)|SUM(score)、COUNT(*)|COUNT(DISTINCT score)、SUM(score)',0,'评分重复仍是不同商品；COUNT(DISTINCT score) 统计的是不同评分数。')

q(1,'两表分别有 3 行、4 行，无连接条件的 CROSS JOIN 产生几行？','7|12|4|取决于主键是否相同',1,'笛卡尔积逐行配对，3×4=12。')
q(1,'LEFT JOIN 后想保留无销售门店，并只统计 2024 年销售，日期条件优先放在哪？','右表日期条件放 WHERE|ON 中与关联条件并列|HAVING COUNT(*)>0|ORDER BY',1,'右表日期条件放 WHERE 会排除 NULL 扩展行；放 ON 可保留左表门店。')
q(1,'门店 LEFT JOIN 销售后，无销售门店的 COUNT(*) 与 COUNT(s.sale_id) 是？','0、0|1、0|1、1|0、1',1,'LEFT JOIN 保留一条 NULL 扩展行；主键列的 COUNT 不计 NULL。')
q(1,'某客户有 2 张订单、3 张优惠券。分别按客户连接订单和券，聚合前有几行？','2|3|5|6',3,'两个一对多关系交叉产生 2×3 行；应各自先聚合，避免金额重复。')
q(1,'子查询返回 (1,NULL)，WHERE id NOT IN (子查询) 对 id=2 的判断是？','TRUE|FALSE|UNKNOWN，WHERE 不保留|语法报错',2,'2<>1 为真，但 2<>NULL 为未知，AND 结果未知。可用相关 NOT EXISTS 表达不存在。')
q(1,'查询高于本类别均价的商品，相关子查询中必须关联什么？','内层 category_id=外层 category_id|内层 id=外层 id|内层 price=外层 price|不需要关联，直接全表 AVG',0,'要比较本类别而非全表均价。外层与内层使用不同别名。')
q(1,'UNION 与 UNION ALL，哪些正确？','UNION 默认去重|UNION ALL 保留重复|两侧列数必须一致|UNION ALL 自动按第一列排序',[0,1,2],'集合合并按列位置对应，类型需兼容；结果顺序仍要显式 ORDER BY。')
q(1,'员工表 e 含 manager_id，查询所有员工及经理名，含无经理员工，应如何连接？','e INNER JOIN e|员工表 e LEFT JOIN 员工表 m ON e.manager_id=m.id|CROSS JOIN 后不筛选|只 SELECT manager_id 就能得到姓名',1,'自连接使用两个别名；LEFT JOIN 保留 manager_id 为 NULL 的员工。')
q(1,'MySQL 8.0 中要模拟完整外连接，并保留原始重复行，推荐？','直接 FULL OUTER JOIN|左右连接 UNION ALL，不做排除|LEFT JOIN UNION ALL 加右侧未匹配部分|INNER JOIN',2,'完整左连接加上右表独有行；右侧未匹配用左表非空主键 IS NULL 判断，避免重复输出匹配部分。')
q(1,'关于外键与复制表，哪些正确？','可空外键允许 NULL|未指定级联时，可随意删被引用父行|CREATE TABLE ... AS SELECT 不保证复制主键索引|CREATE TABLE ... LIKE 会复制全部数据',[0,2],'默认外键约束阻止破坏引用完整性的删除。LIKE 创建类似结构而不复制数据，且不复制外键定义。')

q(2,'FLOOR(-1.5)、CEIL(-1.5)、TRUNCATE(-1.59,1) 分别是？','-1、-2、-1.6|-2、-1、-1.5|-2、-1、-1.6|-1、-1、-1.5',1,'FLOOR 向负无穷取整，CEIL 向正无穷取整，TRUNCATE 按位截断。')
q(2,"utf8mb4 下，CHAR_LENGTH('咖啡') 和 LENGTH('咖啡') 分别是？",'2、2|6、2|2、6|4、6',2,'CHAR_LENGTH 计字符，LENGTH 计字节；这两个汉字各占 3 字节，不能泛化成所有字符都占 3 字节。')
q(2,"CONCAT('A',NULL,'B') 与 CONCAT_WS('-', 'A',NULL,'B') 的结果？",'AB、A-B|NULL、A-B|NULL、NULL|A-B、A--B',1,'CONCAT 有 NULL 参数会返回 NULL；CONCAT_WS 在分隔符非 NULL 时跳过其他 NULL 参数。')
q(2,"SUBSTR('SQL学习',4,2) 返回？",'L学|学习|QL|SQL',1,'MySQL 字符串位置从 1 开始，按字符截取。')
q(2,"DATE_FORMAT('2024-03-05 14:07:09','%Y-%m %H:%i') 返回？",'2024-03 14:07|2024-07 14:03|2024-03 14:03|2024-03-05',0,'%m 是月份，%i 是分钟，不要混淆。')
q(2,"DATEDIFF('2024-03-02 00:01:00','2024-03-01 23:59:00') 返回？",'0|1|2|120',1,'DATEDIFF 只比较日期部分，不表示完整经过了 24 小时。')
q(2,'计算起始时刻 start_at 到 end_at 的完整小时数，选择？','DATEDIFF(start_at,end_at)|TIMESTAMPDIFF(HOUR,start_at,end_at)|DATE_FORMAT(end_at,start_at)|TIMESTAMPDIFF(HOUR,end_at,start_at)',1,'TIMESTAMPDIFF 用结束减开始；DATEDIFF 的参数顺序与之不同，而且按日期差计算天数。')
q(2,'分数 85，CASE WHEN score>=60 THEN 合格 WHEN score>=80 THEN 良好 ELSE 不合格 END 的结果？','良好|合格|同时返回两个|报错',1,'CASE 取第一个满足的分支；应将高分阈值放前面。文字常量实际 SQL 中要加引号。')
q(2,'统计维修次数，哪个写法有错误？',"SUM(CASE WHEN service_type='维修' THEN 1 ELSE 0 END)|COUNT(CASE WHEN service_type='维修' THEN 1 END)|COUNT(CASE WHEN service_type='维修' THEN 1 ELSE 0 END)|SUM(IF(service_type='维修',1,0))",2,'COUNT 会统计所有非 NULL 值，0 也被计数。无匹配的分支应返回 NULL。')
q(2,'关于金额与比例格式，哪些正确？','FORMAT(amount,2) 返回用于展示的字符串|ROUND(amount,2) 可用于数值舍入|计算增长率可用 NULLIF(prev,0) 避免零分母|FORMAT 后排序始终等同数值排序',[0,1,2],'展示格式与计算应分开；字符串排序不一定是数值大小顺序。零基数增长率通常保留 NULL 表示无定义。')

q(3,'分数降序为 100、100、90，RANK 与 DENSE_RANK 分别得到？','1,2,3 和 1,2,3|1,1,3 和 1,1,2|1,1,2 和 1,1,3|1,2,2 和 1,2,2',1,'RANK 并列后跳号，DENSE_RANK 并列后不跳号。')
q(3,'每店只取两条销售记录，同金额以 sale_id 较小优先，用？','RANK() 按 amount 排名|DENSE_RANK() 按 amount 排名|ROW_NUMBER() 按 amount DESC,sale_id 排序|NTILE(2)',2,'ROW_NUMBER 给每行唯一序号，稳定排序后筛 rn<=2；有数据不足两行的店则返回实际行数。')
q(3,'每店取销售额最高的两个金额档位，包含全部并列，应使用？','ROW_NUMBER<=2|DENSE_RANK<=2|RANK=2|LIMIT 2',1,'两个档位强调不同金额；窗口排序不要加入唯一 id 破坏并列。')
q(3,'SELECT 中定义 ROW_NUMBER() AS rn 后，同层 WHERE rn=1 为什么不行？','窗口不能排序|WHERE 阶段不能使用尚未计算的窗口结果|rn 必须中文名|只要反引号即可',1,'用 CTE 或派生表先计算排名，再在外层 WHERE 筛选。')
q(3,'同一窗口两行 amount 均为 100；SUM(amount) OVER(ORDER BY amount) 的两个累计值通常为？','100、200|200、200|100、100|NULL、100',1,'可用该窗口语法时，默认 RANGE 到 CURRENT ROW 包含同排序值的同伴行；逐行累计需显式 ROWS 并稳定排序。')
q(3,'SUM(amount) OVER(PARTITION BY store_id) 的特点是？','每店只返回一行|保留明细行并附加店内总额|只返回店内最后一笔|与 COUNT(*) 相同',1,'窗口聚合保留行；GROUP BY 则将行合并为分组。')
q(3,'每月销售只存在 1 月和 3 月，按月份 LAG(amount) 在 3 月取到什么？','2 月自动补零|1 月值|NULL|报错',1,'LAG 是上一行，不一定是上一个自然月；要计算日历月环比应先补全月份。')
q(3,'NTILE(4) 将有 10 行的一个分区按稳定顺序分桶，各桶行数是？','2、2、2、4|3、3、2、2|4、2、2、2|全部相等',1,'尽量均分，余数优先分配到前面的桶；NTILE 不承诺相同金额在同一桶。')
q(3,'计算每车服务间隔，哪些设计正确？','PARTITION BY vin|ORDER BY service_date,service_id|第一条 LAG 默认 NULL|不分车直接按日期 LAG',[0,1,2],'每辆车独立序列，日期相同时用主键稳定排序；首条没有上次服务，不能伪造间隔。')
q(3,'要得到整组最后一个值，LAST_VALUE 默认窗口可能出什么问题？','默认永远返回 NULL|默认窗口常止于当前行，得到当前窗口末值|只能用于字符串|自动删除重复值',1,'明确 ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING，并给出稳定排序，才覆盖整个分区。')

q(4,'关于索引代价，哪些正确？','可能减少读取的数据量|额外占用存储|INSERT/UPDATE/DELETE 可能增加维护成本|索引越多一定越快',[0,1,2],'索引取舍由查询负载、写入量和数据分布决定。')
q(4,'联合普通 B-tree 索引 (store_id,sale_date)，哪类查询通常最适合连续前缀查找？','只筛 sale_date|store_id 等值且 sale_date 范围|只筛 amount|对 store_id 做任意函数计算',1,'最左前缀通常先利用 store_id 等值，再利用日期范围；是否选择该索引仍需看执行计划。')
q(4,'关于 IS NULL 与 <>，正确认识是？','它们必然让所有索引失效|它们在某些条件下仍可使用索引|必须一律删除这些条件|只能使用全表扫描',1,'笔记中的绝对说法要修正：是否用索引由选择性、覆盖性、代价估算等决定，应看 EXPLAIN。')
q(4,"筛选 2024 年 sale_date，面向普通日期索引更合适的写法是？","YEAR(sale_date)=2024|sale_date>='2024-01-01' AND sale_date<'2025-01-01'|DATE_FORMAT(sale_date,'%Y')='2024'|CAST(sale_date AS CHAR) LIKE '2024%'",1,'半开区间有利于普通索引范围查找，也能覆盖 DATETIME 的全年边界。函数索引等特殊设计需另看。')
q(4,"普通 B-tree 字符串索引，哪种 LIKE 更容易直接用于前缀范围查找？","LIKE '%咖啡%'|LIKE '%咖啡'|LIKE '咖啡%'|三者始终一样",2,'确定的起始前缀更有利；前置通配符通常无法用该索引做前缀定位，但不等于绝无索引扫描。')
q(4,'EXPLAIN 中 key 为 NULL，最稳妥的解读？','数据库没有任何索引|此表访问未选中索引键|SQL 语法错误|查询结果为空',1,'possible_keys 是候选，key 是实际选择；还要看 type、rows 和 Extra，不能只看单列。')
q(4,'哪些操作可以帮助确认优化是否有效？','对比同等数据与条件下的执行计划|比较扫描行数与耗时|只看是否创建索引成功|结合数据量与选择性评估',[0,1,3],'创建成功不代表优化成功，少量数据下全表扫描也可能更便宜。')
q(4,'MySQL 唯一索引列允许 NULL 时，能否有多个 NULL？','一定不允许|通常允许多个 NULL|只能有一个空字符串|不能创建索引',1,'唯一索引允许多个 NULL；主键则不允许 NULL。业务要求非空需要额外 NOT NULL。')
q(4,'关于备份工具，哪些正确？','mysqldump 通常在操作系统终端运行|mysql 客户端可用 SOURCE 路径导入 SQL|所有 mysqldump 输出必然不含 CREATE DATABASE|使用 -p 可在交互提示中输入密码',[0,1,3],'是否包含建库语句取决于参数，例如 --databases；不要在命令中直接暴露密码。')
q(4,'只需 store_id、sale_date，索引恰为 (store_id,sale_date)。所谓覆盖索引指？','查询所需字段都可从索引获得|索引会复制整个数据库|所有查询都不回表|索引会保证查询零耗时',0,'覆盖是针对具体查询而言，不是索引天然覆盖所有 SQL。')

q(5,'咖啡销售中一条记录 quantity=5，统计“卖出杯数”应优先使用？','COUNT(*)|COUNT(quantity)|SUM(quantity)|AVG(quantity)',2,'记录数、商品件数、收入是不同指标；本题假设所选商品数量单位为杯。')
q(5,'咖啡销售两行 amount 为 20、90，quantity 为 1、3，实际每件平均收入为？','55|27.5|30|110',1,'SUM(amount)/SUM(quantity)=110/4。AVG(amount) 是每条销售记录均额。')
q(5,'统计门店历史收入，应优先用销售表的 amount，原因是？','产品价格永不变|当前产品 price 可能已调整|JOIN 一定比单表错|amount 一定无需校验',1,'已记录交易金额反映当时口径，不能用当前目录单价覆盖历史金额。样例数据仍应验证质量。')
q(5,'一辆车有一次销售和三次售后，直接连接后 SUM(v.sale_price) 会？','只计算一次|重复三次|变成平均数|自动去重',1,'售后是一对多；销售额应按销售粒度汇总，或先将售后聚合到车辆粒度。')
q(5,'车辆售价单位为万元，售后 cost 为元。两者合计之前需要？','直接相加|统一单位，例如售价乘 10000|售价除 10000|全部转为字符串',1,'单位必须明确；也需确认业务是否真的需要合计两类收入。')
q(5,'同一顾问向一位客户售出两辆车，统计客户数应使用？','COUNT(*)|COUNT(sale_id)|COUNT(DISTINCT customer_id)|SUM(customer_id)',2,'客户数要去重；销售笔数是另一个指标。')
q(5,'“购车后三个月内保养”，本题定义包含购车当日、不含满三个月当天。正确边界是？','service_date>=sale_date AND service_date<DATE_ADD(sale_date,INTERVAL 3 MONTH)|DATEDIFF(service_date,sale_date)<=90|service_date<sale_date|只比较月份数字',0,'三个日历月不总是 90 天，且必须排除购车前记录。边界规则要事先说清。')
q(5,'按车型计算“平均每次维修费用”，应如何处理免费软件升级记录？','作为 0 费用加入分母|WHERE service_type=维修 后 AVG(cost)|所有售后 SUM(cost)/所有车辆数|先把所有车型混合',1,'此处分母是维修记录数，不是车辆数，也不是全部服务记录数；实际 SQL 中维修需加引号。')
q(5,'只有 2023 年数据进入窗口，MAX(月销量) OVER(PARTITION BY city) 可以命名为？','城市历史最高月销量|城市 2023 年最高月销量|全国历史最高月销量|城市年度总销量',1,'窗口只能看到过滤后数据；“历史最高”需要覆盖完整历史，不能先截成一年。')
q(5,'所有已售车辆的售后次数（含 0 次），哪些做法合理？','以已售 VIN 集合作为左表|COUNT(service_id)|无售后车辆依然显示|COUNT(*) 代替服务主键计数',[0,1,2],'如果销售表未约束 VIN 唯一，先确定去重的已售车辆集合，防止多次销售放大服务次数。')

coffee="""CREATE DATABASE IF NOT EXISTS coffee_training_2 CHARACTER SET utf8mb4;
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
"""
ev="""CREATE DATABASE IF NOT EXISTS ev_training_2 CHARACTER SET utf8mb4;
USE ev_training_2;
CREATE TABLE customers (customer_id INT PRIMARY KEY,name VARCHAR(50) NOT NULL,gender CHAR(1) NOT NULL,phone VARCHAR(20) NOT NULL UNIQUE,city VARCHAR(30) NOT NULL,registration_date DATE NOT NULL);
CREATE TABLE vehicles (vin VARCHAR(18) PRIMARY KEY,model VARCHAR(30) NOT NULL,brand VARCHAR(20) NOT NULL,production_date DATE NOT NULL,battery_capacity DECIMAL(5,1) NOT NULL,sale_price DECIMAL(10,2) NOT NULL);
CREATE TABLE sales (sale_id INT PRIMARY KEY,vin VARCHAR(18) NOT NULL,customer_id INT NOT NULL,sale_date DATE NOT NULL,sales_rep VARCHAR(30) NOT NULL,store_city VARCHAR(30) NOT NULL,FOREIGN KEY(vin) REFERENCES vehicles(vin),FOREIGN KEY(customer_id) REFERENCES customers(customer_id));
CREATE TABLE service_records (service_id INT PRIMARY KEY,vin VARCHAR(18) NOT NULL,service_date DATE NOT NULL,service_type VARCHAR(20) NOT NULL,cost DECIMAL(8,2) NOT NULL DEFAULT 0,description VARCHAR(200),FOREIGN KEY(vin) REFERENCES vehicles(vin));
INSERT INTO customers VALUES (1,'张伟','M','13800000001','北京','2023-01-01'),(2,'李娜','F','13800000002','上海','2023-02-01'),(3,'王强','M','13800000003','北京','2023-03-01');
INSERT INTO vehicles VALUES ('V1','Model S','GreenDrive','2023-01-01',100,30),('V2','iX3','GreenDrive','2023-01-01',80,20),('V3','Model S','GreenDrive','2023-01-01',100,30),('V4','NIO ET7','GreenDrive','2023-01-01',150,40);
INSERT INTO sales VALUES (1,'V1',1,'2024-01-01','顾问甲','北京'),(2,'V2',2,'2024-01-02','顾问乙','上海'),(3,'V3',1,'2024-02-01','顾问甲','北京');
INSERT INTO service_records VALUES (1,'V1','2024-01-11','保养',300,'首次'),(2,'V1','2024-02-10','维修',1000,'维修'),(3,'V2','2024-04-02','保养',200,'满三个月'),(4,'V2','2024-04-12','软件升级',0,NULL),(5,'V1','2024-02-10','软件升级',0,NULL);
"""
data='-- MySQL 8.0.16+；六份笔记场景的精简改编数据，不是原始全量数据。\n-- 首次导入使用；表已存在会报错，请勿重复插入。两个练习库互相独立。\n'+coffee+'\n'+ev
cases=[]
def case(db,title,topic,task,hint,sql,cols,rows,explain,extra):
    cases.append(dict(db=db,title=title,topic=topic,task=task,hint=hint,sql=sql,cols=cols.split('|'),rows=rows,explain=explain,extra=extra))
case('coffee_training_2','01 · 所有门店的员工数','左连接 / COUNT','返回所有门店的 store_id、store_name、employee_count，包含没有员工的门店；按 store_id 排序。','用员工主键计数，别用 COUNT(*)。',
'''SELECT s.store_id, s.store_name, COUNT(e.employee_id) AS employee_count
FROM stores s LEFT JOIN employees e ON e.store_id=s.store_id
GROUP BY s.store_id,s.store_name ORDER BY s.store_id;''','store_id|store_name|employee_count',[[1,'北京店',2],[2,'上海店',2],[3,'杭州店',0]],'杭州店没有员工，仍需保留。','再统计各店有销售记录的员工数，避免一位员工多笔销售造成重复。')
case('coffee_training_2','02 · 每件商品的实际收入','聚合 / 加权平均','按产品统计售出数量 qty、收入 revenue、每件平均收入 unit_revenue，包含未售产品；未售产品平均收入显示 NULL。按 product_id 排序。','总金额除以总数量，零分母用 NULLIF。',
'''SELECT p.product_id, COALESCE(SUM(s.quantity),0) AS qty,
 COALESCE(SUM(s.amount),0) AS revenue,
 ROUND(SUM(s.amount)/NULLIF(SUM(s.quantity),0),2) AS unit_revenue
FROM products p LEFT JOIN sales s ON s.product_id=p.product_id
GROUP BY p.product_id ORDER BY p.product_id;''','product_id|qty|revenue|unit_revenue',[[1,6,120,20],[2,4,120,30],[3,2,50,25],[4,0,0,'NULL']],'未售不意味着商品单价为 0，平均成交收入此时没有定义。','只保留收入至少 100 的商品，使用 HAVING。')
case('coffee_training_2','03 · 每店最畅销的产品','先聚合 / 并列排名','按销售门店统计总销售数量，取每店销量第一的全部并列产品。返回 store_id、product_id、qty，按门店和产品编号排序；无销售门店不返回。','先按门店和产品汇总，再按门店做 DENSE_RANK。',
'''WITH totals AS (
 SELECT store_id,product_id,SUM(quantity) AS qty FROM sales
 GROUP BY store_id,product_id
), ranked AS (
 SELECT *,DENSE_RANK() OVER(PARTITION BY store_id ORDER BY qty DESC) AS rk FROM totals
)
SELECT store_id,product_id,qty FROM ranked WHERE rk=1
ORDER BY store_id,product_id;''','store_id|product_id|qty',[[1,2,4],[2,1,3]],'先聚合到产品粒度，不能直接对单条销售数量排名。','把北京店美式增加 1 件，验证并列冠军会同时返回。')
case('coffee_training_2','04 · 门店员工贡献榜','多表 / 窗口','返回全部员工 employee_id、store_id、revenue、rk；没有销售算 0。在所属门店按收入做 DENSE_RANK，最终按门店、排名、员工编号排序。假设员工没有调店，销售 store_id 与员工归属一致。','员工 LEFT JOIN 销售，先按员工汇总再排名。',
'''WITH totals AS (
 SELECT e.employee_id,e.store_id,COALESCE(SUM(s.amount),0) AS revenue
 FROM employees e LEFT JOIN sales s ON s.employee_id=e.employee_id
 GROUP BY e.employee_id,e.store_id
)
SELECT *,DENSE_RANK() OVER(PARTITION BY store_id ORDER BY revenue DESC) AS rk
FROM totals ORDER BY store_id,rk,employee_id;''','employee_id|store_id|revenue|rk',[[1,1,100,1],[2,1,80,2],[3,2,110,1],[4,2,0,2]],'不能把 employee_id 放入排名窗口的 ORDER BY，否则收入相同也不会并列。','若员工调店，区分销售发生门店与当前归属门店。')
case('coffee_training_2','05 · 每日收入与累计','日期粒度 / 窗口边界','统计有销售日期的 day、revenue、running_revenue。按日期排序，累计包含当日全部收入。','先每天一行，再显式 ROWS 累计。',
'''WITH daily AS (
 SELECT sale_date AS day,SUM(amount) AS revenue FROM sales GROUP BY sale_date
)
SELECT day,revenue,SUM(revenue) OVER(
 ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
) AS running_revenue FROM daily ORDER BY day;''','day|revenue|running_revenue',[['2024-01-01',160,160],['2024-01-02',60,220],['2024-02-01',20,240],['2024-03-01',50,290]],'累计先统一成日粒度；没有销售的日期不会自动生成。','改成每店独立累计，并解释分区键。')
case('coffee_training_2','06 · 自然月环比，缺月补零','月份序列 / LAG','上海店 2024 年 1~3 月，每月输出 month、revenue、prev、growth_pct；无销售补 0，首月及上月收入为 0 时增长率为 NULL。','用三个目标月份构成日期表；左连接、汇总后再 LAG。',
'''WITH months AS (
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
FROM compared ORDER BY month;''','month|revenue|prev|growth_pct',[['2024-01-01',60,'NULL','NULL'],['2024-02-01',0,60,-100],['2024-03-01',50,0,'NULL']],'如果不补 2 月，3 月会错误地拿 1 月做环比。这里采用有界月份集合，不需要额外日历表。','扩展到所有门店：月份与门店 CROSS JOIN 后再连接销售。')
case('ev_training_2','07 · 已售车辆的售后覆盖','去重 / 左连接','返回所有已售 VIN 的 service_count（含 0）；按 VIN 排序，未售车辆 V4 不进入结果。','先取得已售 VIN 集合，再左连接服务。',
'''WITH sold AS (SELECT DISTINCT vin FROM sales)
SELECT s.vin,COUNT(r.service_id) AS service_count
FROM sold s LEFT JOIN service_records r ON r.vin=s.vin
GROUP BY s.vin ORDER BY s.vin;''','vin|service_count',[['V1',3],['V2',2],['V3',0]],'去重已售集合，防止同 VIN 多条销售记录放大服务次数。','改成所有车辆，V4 应以 0 次出现在结果中。')
case('ev_training_2','08 · 顾问客户数与销售额','去重客户 / 金额单位','每位顾问输出 sales_rep、customer_count、revenue_wan，按顾问名排序。销售额单位为万元，按销售记录计算；不要连接售后明细。','客户数 COUNT DISTINCT，金额关联车辆表后汇总。',
'''SELECT s.sales_rep,COUNT(DISTINCT s.customer_id) AS customer_count,
 SUM(v.sale_price) AS revenue_wan
FROM sales s JOIN vehicles v ON v.vin=s.vin
GROUP BY s.sales_rep ORDER BY s.sales_rep COLLATE utf8mb4_bin;''','sales_rep|customer_count|revenue_wan',[['顾问乙',1,20],['顾问甲',1,60]],'按 utf8mb4_bin 排序固定展示顺序；顾问甲卖了两辆车但只有一位客户。售价字段为万元，服务费用为元。','若要统计服务金额，先按合适粒度聚合，再连接；不要 SUM(DISTINCT 售价) 去重。')
case('ev_training_2','09 · 购车后三个月内保养','EXISTS / 日历边界','查询 2024 年购车，且购车当日及之后、不满三个日历月发生过保养的客户，姓名去重到客户 ID 粒度；按 customer_id 排序。','EXISTS 避免多个保养记录重复客户；日期使用半开区间。',
'''SELECT c.customer_id,c.name FROM customers c
WHERE EXISTS (
 SELECT 1 FROM sales s WHERE s.customer_id=c.customer_id
 AND s.sale_date>='2024-01-01' AND s.sale_date<'2025-01-01'
 AND EXISTS (
  SELECT 1 FROM service_records r WHERE r.vin=s.vin AND r.service_type='保养'
  AND r.service_date>=s.sale_date
  AND r.service_date<DATE_ADD(s.sale_date,INTERVAL 3 MONTH)
 )
) ORDER BY c.customer_id;''','customer_id|name',[[1,'张伟']],'V2 的保养恰好在满三个月当天，因此不纳入；这项业务边界已明确采用不含上界。','如果改成包含满三个月当天，DATE 字段使用 <=，李娜也会出现。')
case('ev_training_2','10 · 每车相邻服务间隔','LAG / 同日排序','输出 vin、service_id、previous_date、gap_days。按 VIN、服务日期、服务 ID 排序，同日两条服务间隔为 0，首条为 NULL。','先取 LAG(service_date)，外层 DATEDIFF 当前减上次。',
'''WITH compared AS (
 SELECT *,LAG(service_date) OVER(PARTITION BY vin ORDER BY service_date,service_id) AS previous_date
 FROM service_records
)
SELECT vin,service_id,previous_date,DATEDIFF(service_date,previous_date) AS gap_days
FROM compared ORDER BY vin,service_date,service_id;''','vin|service_id|previous_date|gap_days',[['V1',1,'NULL','NULL'],['V1',2,'2024-01-11',30],['V1',5,'2024-02-10',0],['V2',3,'NULL','NULL'],['V2',4,'2024-04-02',10]],'同日记录用 service_id 明确顺序；NULL 表示没有上次记录，不应替换成零天。','增加 LEAD 查看下一次服务时间。')
case('ev_training_2','11 · 从销售到首次售后','首次记录 / 分母口径','按每笔销售计算购车当日及之后的首次服务，求这些间隔的平均天数 avg_days，并返回有服务的销售数 serviced_sales。无服务销售不进入平均分母。','每笔销售先 MIN 服务日期；再 DATEDIFF，最后 AVG。',
'''WITH first_service AS (
 SELECT s.sale_id,s.sale_date,MIN(r.service_date) AS first_date
 FROM sales s LEFT JOIN service_records r
 ON r.vin=s.vin AND r.service_date>=s.sale_date
 GROUP BY s.sale_id,s.sale_date
)
SELECT COUNT(first_date) AS serviced_sales,
 ROUND(AVG(DATEDIFF(first_date,sale_date)),2) AS avg_days
FROM first_service;''','serviced_sales|avg_days',[[2,50.5]],'V1 为 10 天，V2 为 91 天（2024 年有闰日），平均 50.5 天；V3 无售后不能当作 0 天。此处按销售而非客户加权，样例每车只销售一次。','改成每客户等权平均时，应先求客户内平均，再对客户求平均。')
case('ev_training_2','12 · 不重复销售额的城市报表','先聚合再连接 / 一对多','输出销售城市 store_city、revenue_wan、service_cost_yuan。服务费用仅统计已售车辆的所有服务，每辆车只归属一个销售城市（本数据满足）；按城市排序。','销售与服务分别聚合到城市，再连接。',
'''WITH revenue AS (
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
ORDER BY a.store_city COLLATE utf8mb4_bin;''','store_city|revenue_wan|service_cost_yuan',[['上海',20,200],['北京',60,1300]],'V1 虽有三次服务，售价仍只算一次；两列保留原有单位，不直接相加。使用 utf8mb4_bin 固定城市展示顺序。','若车辆跨城市转售，先明确服务归属时段，不能直接按城市与 VIN 去重分摊。')

exec(compile((ROOT/'sql-training-support/expand-2.py').read_text(encoding='utf-8'),'expand-2.py','exec'))
lessons=[]
descs=[('把筛选与统计分开','先写清结果是一行一商品，还是一行一类别。',['WHERE 管明细，HAVING 管分组。','COUNT(*)、COUNT(列)、COUNT(DISTINCT 列) 的分母不同。','分页必须明确排序，日期筛选优先半开区间。'],"SELECT category_id,AVG(price) AS avg_price\nFROM products WHERE price>0\nGROUP BY category_id HAVING AVG(price)>100;"),('联表前先算行数','根据单表、多表笔记，把内连接、外连接、自连接和子查询放到业务中理解。',['外连接右表条件放 WHERE 可能丢掉无匹配行。','多个一对多表先聚合，不能盲目用 DISTINCT 修补。','NOT IN 的 NULL 陷阱与 NOT EXISTS 的语义要区分。'],"SELECT s.store_id,COUNT(e.employee_id) AS n\nFROM stores s LEFT JOIN employees e\nON e.store_id=s.store_id\nGROUP BY s.store_id;"),('函数服务于指标','覆盖数值、字符串、时间日期和 CASE 条件判断。',['LENGTH 算字节，CHAR_LENGTH 算字符。','DATEDIFF 与 TIMESTAMPDIFF 参数方向不同。','FORMAT 用于展示；平均、排序仍应保留数值。'],"SELECT ROUND(SUM(amount)/NULLIF(SUM(quantity),0),2)\nAS unit_revenue FROM sales;"),('先确定粒度，再开窗口','训练排名、前后行、分桶、累计和窗口范围。',['ROW_NUMBER 取行，DENSE_RANK 取并列档位。','LAG 是上一行，日历环比要先补齐月份。','逐行累计明确 ROWS 和稳定排序键。'],"SELECT sale_id,amount,\nSUM(amount) OVER(ORDER BY sale_date,sale_id\nROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)\nAS running_amount FROM sales;"),('用执行计划检验索引','索引笔记中的规则是起点，是否有效要结合实际执行计划。',['IS NULL、<> 不意味着索引必然失效。','普通索引列上的函数可能阻碍直接范围查找。','索引有空间与写入成本；备份要练习恢复。'],"EXPLAIN SELECT sale_id,amount FROM sales\nWHERE store_id=1 AND sale_date>='2024-01-01'\nAND sale_date<'2025-01-01';\n-- 候选联合索引：(store_id,sale_date)"),('用两个项目练口径','咖啡店练销售、数量和贡献；新能源汽车练客户、售后和时间间隔。',['明确记录数、去重客户数与商品数量。','车辆售价为万元，售后成本为元。','先写时间边界、并列规则与无匹配处理，再写 SQL。'],"-- 两组精简数据包含：\n-- 无销售门店、零业绩员工、缺失月份\n-- 未售车辆、无售后车辆、同日服务、边界保养\n-- 到业务实战下载数据，逐项核对预期结果。")]
for i,(title,desc,bullets,sql) in enumerate(descs):
    lessons.append([f'{i+1:02d} / '+sources[i],title,topics[i],desc,bullets,sql,'验收：先独立完成本章 10 题，再解释每个错误选项为什么错。'])

def js(x):return json.dumps(x,ensure_ascii=False).replace('<','\\u003c')
s=(ROOT/'1.html').read_text(encoding='utf-8')
s=re.sub(r'const BANK=.*?;\s*const KEY=',lambda m:'const BANK='+js(bank)+';\nconst KEY=',s,flags=re.S)
s=s.replace("'mysqlLearning.v2'","'mysqlLearning.chapter2.v1'")
s=s.replace('version:2,','version:2,chapter:2,').replace("raw.version!==2||","raw.version!==2||raw.chapter!==2||")
s=re.sub(r'const LESSONS=\[.*?\];',lambda m:'const LESSONS='+js(lessons)+';',s,flags=re.S)
s=re.sub(r'const DATA_SQL=.*?;\s*const CASES=.*?;\s*function renderLab',lambda m:'const DATA_SQL='+js(data)+';\nconst CASES='+js(cases)+';\nfunction renderLab',s,flags=re.S)
s=s.replace('i<8','i<12').replace('/ 8','/ 12').replace('8 个实战','12 个实战')
s=s.replace('SQL 进阶训练营 · 从会写到会分析','MySQL 专项进阶 · 第二册')
s=s.replace('SQL / LEARNING LAB','MYSQL / WORKBOOK 02')
s=s.replace('从写出 SQL，到理解数据。','第二册 · 查询、分析与业务实战')
s=s.replace('基础 → 查询 → 联表 → 窗口 → 性能与事务。先理解，再练习，最后用真实业务检验自己。','依据你的六份课堂笔记编写。60 道专项题 + 12 道 SQL 实战，从查询结果推导，到咖啡店与新能源汽车分析。')
s=s.replace('--green:#166b59;--mint:#e8f5ee','--green:#315b98;--mint:#edf3ff').replace('--nav:#102d35','--nav:#172b4b')
s=s.replace('多选题选完再提交。命令题仅做保守的参考写法匹配，不执行 SQL；未匹配不代表语义一定错误，请对照解析或到 MySQL 验证。','题库为单选和多选；多选必须全部选对。实战 SQL 在“业务实战”中独立编写和自查。本页离线运行，不连接数据库。')
s=s.replace('一套数据，八个业务问题','两套业务数据，十二个分析任务')
s=s.replace('电商订单数据包含 4 位客户、8 笔订单：已支付、退款、待支付、无订单客户与并列金额。先写 SQL 和预期结果，再展开参考解法。','根据两份综合实战笔记，保留表名与核心字段，另编小规模边界数据：咖啡店 6 题 + 新能源汽车 6 题。数据包含零销售、缺失月份、同日服务和三个月边界；不是笔记原始全量数据。先写 SQL，再核对预期表格。')
s=s.replace('脚本创建 sql_training_lab 数据库','脚本创建 coffee_training_2 与 ev_training_2 两个数据库')
s=s.replace('<p>${esc(c.task)}</p>','<p class="muted">练习库：<code>${esc(c.db)}</code> · 先执行 USE ${esc(c.db)};</p><p>${esc(c.task)}</p>')
s=s.replace("'USE sql_training_lab;\\n\\n'+CASES.map((c,i)=>'-- '+(i+1)+'. '+c.title+'\\n'+c.sql)","CASES.map((c,i)=>'USE '+c.db+';\\n-- '+(i+1)+'. '+c.title+'\\n'+c.sql)")
s=s.replace('sql-training-data.sql','sql-training-2-data.sql').replace('sql-training-solutions.sql','sql-training-2-solutions.sql').replace('sql-learning-progress.json','sql-learning-2-progress.json')
s=s.replace('清空新版','清空第二册').replace('新版记录已清空；原版题库记录不受影响。','第二册记录已清空；第一册记录不受影响。')
s=s.replace('已保留原版文件为 1.original.html。新版独立记录进度，避免旧版误判结果影响学习。','第二册已就绪：60 道专项题、12 道实战。进度独立保存，不影响 1.html。')
s=s.replace('能设计失败回滚与重试。','能解释报表的粒度、单位与时间边界。')
s=s.replace('本题库使用 DQL 表示查询。','本题库使用 DQL 表示查询。')
s=s.replace('正确率衡量当前参考匹配，不等于真实 SQL 熟练度。','正确率仅统计客观题；实战完成由你运行核对后自评。')
s=s.replace('然后再挑战更大的真实数据集。','参考笔记：单表查询.md、多表查询.md、MySQL函数.md、MySQL索引和函数.md、day08_数据分析综合实战1.md、day08_数据分析综合实战2.md。')
# Lesson-specific SQL uses the source notes or the named lab schemas, never silently mixes them.
s=s.replace('建议每天 30–45 分钟：','学习路线中的商品分类示例沿用单表笔记，其余示例参见实战对应库。建议每天 30–45 分钟：')
s=s.replace('60 道专项题 + 12 道 SQL 实战',f'{len(bank)} 道专项题 + {len(cases)} 道 SQL 实战')
s=s.replace('60 道专项题、12 道实战',f'{len(bank)} 道专项题、{len(cases)} 道实战')
s=s.replace('i<12',f'i<{len(cases)}').replace('/ 12',f'/ {len(cases)}').replace('12 个实战',f'{len(cases)} 个实战')
s=s.replace('两套业务数据，十二个分析任务','两套业务数据，二十四个分析任务')
s=s.replace('咖啡店 6 题 + 新能源汽车 6 题','咖啡店 12 题 + 新能源汽车 12 题')
s=s.replace('本章 10 题','本章 20 题')
s=s.replace('<option value="all">全部题目</option>','<option value="all">全部题目</option><option value="new">本次新增 60 题</option>')
s=s.replace("filter==='all'||filter==='unanswered'", "filter==='all'||filter==='new'&&q.id>=60||filter==='unanswered'")
s=s.replace('<span class="chip">#${q.id+1}</span>','<span class="chip">#${q.id+1}</span>${q.id>=60?\'<span class="chip">新增</span>\':\'\'}')
s=s.replace('<span>${esc(c.topic)}</span></div><h2>', '<span>${esc(c.topic)}</span>${i>=12?\'<span class="chip">新增</span>\':\'\'}</div><h2>')
(ROOT/'2.html').write_text(s,encoding='utf-8')
(ROOT/'sql-training-2-data.sql').write_text(data,encoding='utf-8')
(ROOT/'sql-training-2-solutions.sql').write_text('\n\n'.join('USE '+c['db']+';\n-- '+c['title']+'\n'+c['sql'] for c in cases),encoding='utf-8')
print(f'Built {len(bank)} questions / {len(cases)} cases: {ROOT/"2.html"}')
