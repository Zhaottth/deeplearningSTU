"""Append-only extension: keep the original 60 question and 12 case IDs stable."""
q(0,'score 为 NULL、0、80。AVG(IFNULL(score,0)) 与 AVG(score) 分别是？','约 26.67、40|40、40|约 26.67、80|0、40',0,'先补零会改变平均值分母：80/3 与 80/2。是否把缺失评分当零，必须由业务定义。')
q(0,'WHERE price>100 OR price<=100 能保留哪些价格？','所有行，包括 NULL|所有非 NULL 价格|只有正数|只有整数',1,'NULL 与数字比较为 UNKNOWN，两个 UNKNOWN 做 OR 仍是 UNKNOWN，WHERE 不保留。')
q(0,'类别为 1、1、NULL、NULL。GROUP BY category_id 通常产生几组？','1|2|3|4',1,'分组会把 NULL 分到同一组；这与 NULL=NULL 的比较结果不同。')
q(0,'价格为 10、10、20、NULL，COUNT(DISTINCT price) 为？','4|3|2|1',2,'忽略 NULL 后，对价格值去重，只剩 10 和 20。')
q(0,'需求是“至少有两件价格大于 100 的商品的类别”，正确方案？','先 WHERE price>100，再 GROUP BY category_id HAVING COUNT(*)>=2|先 GROUP BY 再 WHERE price>100|HAVING SUM(price)>200 即可|WHERE COUNT(*)>=2',0,'单件价格条件与合格商品数量条件是不同层级；总额超过 200 不代表有两件合格商品。')
q(0,'SELECT price*0.8 AS discount FROM products WHERE discount>100；本层没有 discount 原字段。问题是？','乘法不能产生别名|WHERE 不能引用该 SELECT 别名|别名必须用中文|小数不能比较',1,'使用 WHERE price*0.8>100，或外层查询筛选别名。ORDER BY 通常可以使用 SELECT 别名。')
q(0,'关于 WHERE price BETWEEN 100 AND 200，哪些正确？','包含 100|包含 200|NULL 不会被保留|等同 price>100 AND price<200',[0,1,2],'BETWEEN 包含两端；NULL 的比较仍为 UNKNOWN。')
q(0,'先按 amount DESC,id ASC 排序，结果 ID 为 8、2、5、1。LIMIT 1,2 返回哪些 ID？','8、2|2、5|5、1|只有 2',1,'偏移量从 0 开始；跳过第一行，再取两行。')
q(0,'SQL 找错：SELECT category_id,COUNT(*) FROM products GROUP BY category_id HAVING price>100。price 不依赖类别。应怎样改？','把 price>100 放 WHERE，位于 GROUP BY 前|把 HAVING 改成 ORDER BY|把 COUNT 改成 SUM 即可|关闭 ONLY_FULL_GROUP_BY 就能保证需求正确',0,'如果需求是先筛高价商品再统计，应该在明细阶段过滤；关闭模式不能修复逻辑。')
q(0,'两行 (category_id,price) 为 (1,10)、(1,20)。SELECT DISTINCT category_id,price 返回几行？','1|2|0|语法错误',1,'DISTINCT 对整个字段组合去重，两个价格不同，组合就不同。')

q(1,'A 的键为 1、2；B 的键为 1、1、3。A INNER JOIN B ON A.k=B.k 返回几行？','1|2|3|6',1,'A 的键 1 匹配 B 的两行；键 2 没有匹配。连接不会自动去重。')
q(1,'上题相同数据，A LEFT JOIN B ON A.k=B.k 返回几行？','2|3|4|6',1,'键 1 贡献两行，键 2 贡献一条 NULL 扩展行，总共三行。')
q(1,'LEFT JOIN 后要查无订单客户，orders.id 为非空主键。最合适的过滤？','WHERE o.id IS NULL|WHERE o.id=NULL|WHERE o.amount=0|WHERE c.id IS NULL',0,'右表非空主键变为 NULL 表明没有匹配；零金额订单仍然是订单。')
q(1,'标量子查询用在 price > (SELECT price FROM products)，子查询返回多行，会怎样？','自动取最大值|自动取第一行|报子查询返回多行的错误|自动转为 IN',2,'标量子查询必须至多一行一列；若要比较全表均价，明确写 AVG(price)。')
q(1,'price > (SELECT MAX(price) FROM empty_products)，子查询表为空，会怎样？','所有商品保留|没有商品通过此条件|等同 price>0|语法报错',1,'整体聚合 MAX 返回 NULL，比较结果为 UNKNOWN。')
q(1,'查询购买过拿铁的员工，仅需要员工名单。哪种方式可避免多笔购买重复员工？','相关 EXISTS 子查询|INNER JOIN 后从不去重|CROSS JOIN 全表|对员工姓名 SUM',0,'EXISTS 只判断是否存在至少一行匹配；同一员工有多次匹配也只保留一个外层员工行。')
q(1,'一对多连接后 SUM(DISTINCT amount) 能普遍修复金额膨胀吗？','能，它按订单 ID 去重|不能，不同订单的相同金额也会被合并|能，只要金额非空|只能用于 LEFT JOIN',1,'DISTINCT amount 去重的是数值，两个真实订单都是 100 时会错误地只算 100。应按业务主键控制粒度。')
q(1,'同表员工经理自连接时，为什么需要别名？','两个逻辑角色要分别引用|别名会自动创建索引|别名能自动去重|不使用别名必然查不到数据',0,'e 表示员工、m 表示经理，关联条件 e.manager_id=m.id，字段含义清楚且不歧义。')
q(1,'关于 UNION，哪些正确？','两侧列名不必相同|两侧列数必须相同|结果列名通常来自第一条 SELECT|UNION 会按业务主键而非整行自动去重',[0,1,2],'UNION 按所选整行去重，字段按位置对应。要排序应在整个集合查询外层明确指定。')
q(1,'统计类别与商品均价，若要展示完全没有商品的类别，应采用？','类别表 LEFT JOIN 按类别聚合的商品结果|只查 products GROUP BY category_id|商品 INNER JOIN 类别|WHERE AVG(price) IS NULL',0,'无商品类别不会出现在商品分组结果中，必须用完整类别表作为保留侧。')

q(2,"ROUND(2.675,2) 与 TRUNCATE(2.675,2)，使用 MySQL 精确数值字面量时分别是？",'2.68、2.67|2.67、2.67|2.68、2.68|2.6、2.6',0,'ROUND 舍入，TRUNCATE 截断。浮点近似值的边界舍入可能不同，本题明确使用精确字面量。')
q(2,"REPLACE('拿铁拿铁','拿铁','美式') 返回？",'美式拿铁|拿铁美式|美式美式|只返回美式',2,'REPLACE 替换所有匹配片段；它返回新字符串，不会直接更新原表。')
q(2,"CONCAT_WS('-', 'A', '', 'B') 返回？",'A-B|A--B|AB|NULL',1,'CONCAT_WS 跳过 NULL，但不会跳过空字符串，因此保留两个分隔符。')
q(2,"IFNULL('', '未知') 与 COALESCE(NULL,NULL,'已知') 的结果？",'未知、已知|空字符串、已知|NULL、NULL|空字符串、NULL',1,'空字符串不是 NULL；COALESCE 返回第一个非 NULL 参数。')
q(2,"DATE_ADD('2024-01-31',INTERVAL 1 MONTH) 返回？",'2024-02-29|2024-03-02|2024-02-31|NULL',0,'目标月没有 31 日时调整到月末；2024 年是闰年。日历月运算不等同加固定 30 天。')
q(2,"DATE_FORMAT 时间格式中的 %m、%i、%s 分别是什么？",'月、分、秒|分、月、秒|月、时、分|分、秒、时',0,'常用格式是 %Y-%m-%d %H:%i:%s。')
q(2,'CASE WHEN cost=0 THEN 免费 END 未写 ELSE，cost=300 时返回？','免费|0|NULL|报错',2,'没有匹配分支且未指定 ELSE，CASE 返回 NULL。这在条件 COUNT 中很有用。')
q(2,'已有一行 service_type=NULL。SUM(CASE WHEN service_type=维修 THEN 1 ELSE 0 END) 中该行贡献？','1|0|NULL|让整个聚合报错',1,'NULL 与维修比较为 UNKNOWN，不满足 WHEN，进入 ELSE 0。实际 SQL 中文字符串需加引号。')
q(2,'已完成数 0、总数 0。ROUND(done/NULLIF(total,0)*100,2) 应返回？','0|100|NULL|无穷大',2,'NULLIF(0,0) 返回 NULL，无定义的比例保留 NULL；是否展示为破折号由展示层决定。')
q(2,'注册日期含 2023-01 与 2024-01，按 MONTH(registration_date) 分组的潜在问题是？','不同年份的 1 月会合并|月份会变成日期|一定报错|会自动按年分开',0,'跨年分析应按 YEAR、MONTH 组合，或格式化为 %Y-%m。')

q(3,'收入降序 90、90、80、70。RANK<=3 与 DENSE_RANK<=3 分别保留几行？','3、4|3、3|4、3|2、3',0,'RANK 为 1,1,3,4，DENSE_RANK 为 1,1,2,3；“前 3 名次”与“前 3 档位”不同。')
q(3,'SUM(amount) OVER() 没有 PARTITION BY 和 ORDER BY，含义是？','对当前查询的全部输入行求总额，每行重复该值|语法错误|只计算当前行|按主键隐式累计',0,'空窗口把全部输入行作为一个分区，聚合覆盖整个分区。')
q(3,'按日期稳定排序后的金额为 10、20、30。ROWS BETWEEN 1 PRECEDING AND CURRENT ROW 的 SUM 依次是？','10、30、50|10、30、60|30、50、30|10、20、30',0,'每行窗口包含前一行与当前行；第一行只有自身。')
q(3,'要计算连续日历三天的平均收入，ROWS BETWEEN 2 PRECEDING AND CURRENT ROW 是否总正确？','总正确|只有每天一行且日期连续时，才对应三个自然日|等价过去 72 小时|会自动补日期',1,'ROWS 数的是行，不是时间。缺日期或每天多行都会改变含义。')
q(3,'LAG(amount,2,0) 在分区的第二行返回？','第一行金额|当前金额|0|第二行金额乘 2',2,'前两行的位置不存在，因此返回指定默认值 0；默认值只处理越界，不会替换真实行中的 NULL。')
q(3,'上一行 amount 恰为 NULL，LAG(amount,1,0) 返回？','0|NULL|当前金额|报错',1,'第三个参数仅在找不到前行时使用；已存在前行的 NULL 会原样返回。')
q(3,'PARTITION BY store_id ORDER BY amount DESC 中，哪项不会由该窗口自动保证？','店内排名|按金额计算的窗口顺序|最终输出按店号、金额排列|各店重新开始编号',2,'窗口 ORDER BY 规定计算顺序；最终展示顺序要写查询外层 ORDER BY。')
q(3,'NTILE(4) 的一个分区只有 2 行，分桶编号通常是？','1、2|1、4|4、4|必须报错',0,'行数少于桶数时，前面两个桶各有一行，后面为空；不会额外生成行。')
q(3,'在哪一层计算 SUM(revenue) OVER()，才能表示“筛选后城市的收入合计”？','在筛选条件生效后的那一层|一定在筛选之前|必须先 LIMIT 1|窗口不受过滤影响',0,'窗口看到的是所在层经 WHERE、分组等阶段处理后的输入。分母的作用域必须与业务口径一致。')
q(3,'哪些是合法、清晰的窗口计算组织方式？','CTE 先求日收入，外层 LAG 对比|CTE 先排名，外层筛 rank<=3|在同一表达式中直接 SUM(LAG(amount) OVER(...)) OVER(...) 嵌套窗口|窗口计算后外层再求平均',[0,1,3],'MySQL 不支持直接嵌套窗口函数；可通过 CTE 或派生表分层计算。')

q(4,'索引 (a,b,c)，条件 a=1 AND b>10 AND c=3。关于 c 的正确说法？','c 永远没有任何用途|c 未必能进一步缩小连续查找范围，但可能用于索引条件过滤或覆盖|整个索引必然失效|c 必须是主键',1,'范围条件后的列不应被简单说成“完全失效”；实际作用需要结合执行计划。')
q(4,'EXPLAIN 的 possible_keys 有索引但 key 为 NULL，可能原因？','优化器认为扫描成本更低|索引必然损坏|SQL 无法运行|possible_keys 就是实际使用的索引',0,'候选不代表最终选择，数据量、选择性与回表成本都影响选择。')
q(4,'EXPLAIN 的 rows 通常表示？','绝对精确的最终结果行数|估计需要检查的行数|表的字段数|已经执行后的耗时',1,'普通 EXPLAIN 是估计计划，不等于实际执行统计。')
q(4,'EXPLAIN Extra 中 Using filesort 是否一定表示把排序数据写到了磁盘？','一定|不一定，它表示额外排序，可能在内存完成|表示没有排序|表示 SQL 报错',1,'filesort 是 MySQL 排序算法术语，不能只看名称判断磁盘 I/O。')
q(4,'InnoDB 中二级索引叶子通常包含什么定位信息？','对应行的主键值|只有物理文件名|完整数据库备份|用户密码',0,'通过主键值可进一步访问聚簇索引中的行；覆盖查询可能避免这次回表。')
q(4,'单独给“性别”这样的低区分度列建索引，应该如何判断收益？','必然很高|结合分布、覆盖性和查询评估，不能仅凭列名判断|完全不允许建|一定比联合索引快',1,'低区分度经常降低单列过滤收益，但某些稀有值、覆盖查询或组合条件仍可能受益。')
q(4,"username 是 VARCHAR 且有索引，WHERE username=12345 的风险是什么？",'可能发生隐式类型转换，影响语义与索引利用|MySQL 必然把数字转成 5 个字符再匹配|一定语法错误|保证使用索引',0,'按列类型传入字符串参数，避免无意的数值比较与转换；同时用计划验证。')
q(4,'索引存在于 (store_id,sale_date)，仍新增 (store_id) 索引之前应考虑？','已有联合索引可能已满足前缀查询|每个 WHERE 字段必须独立索引|短索引无任何成本|一定删除联合索引',0,'不要机械增加重复索引；是否保留更窄索引要结合具体负载和大小评估。')
q(4,'哪些属于验证备份可用性的步骤？','在隔离环境恢复|核对表结构与关键记录数|只确认文件后缀是 .sql|检查导出和恢复错误日志',[0,1,3],'有文件不等于能恢复；还应根据需要验证编码、约束、视图等对象。')
q(4,'普通 CREATE TABLE ... AS SELECT ... 复制之后，接下来应检查？','主键、索引、约束是否按需求建立|一定已完整克隆原表全部属性|源表一定已删除|新表天然只读',0,'CTAS 主要从查询结果生成表和数据，不应视为完整结构克隆工具。')

q(5,'两店月收入 100、900，增长率 100%、0%。直接平均增长率 50% 能代表总收入增长率吗？','一定能|不能，缺少各店上期基数并应汇总后计算|总收入增长必为 100%|只需取最大增长率',1,'100% 增长的店上期为 50，另一店上期 900；整体增长为 (1000-950)/950，约 5.26%。')
q(5,'“维修车辆占比”的分子应是哪一个？','维修服务记录条数|发生过维修的去重 VIN 数|所有售后成本|维修记录数除以天数',1,'一车多次维修不应增加车辆数；分母还需定义为已售车辆、在保车辆或其他人群。')
q(5,'一位客户两次购车，等待首次服务 10 天、90 天；另一位客户一次购车等待 20 天。按客户等权平均是多少？','40 天|35 天|60 天|20 天',1,'先客户内平均：50、20；再对两位客户平均得到 35。按三笔销售平均则为 40。')
q(5,'某店 1 月没有销售。将其月收入补 0，与“该月数据尚未入库”是否一样？','一样|不一样，前者是真实零，后者是未知|未知必须写 0|缺数据应删除门店',1,'补零需要确认数据覆盖完整；未采集或未入库不能直接视为零业务。')
q(5,'“顾问负责客户数”按顾问分组去重后再相加，为什么可能大于全公司客户数？','同一个客户可能由多位顾问服务|COUNT DISTINCT 无效|SUM 一定报错|客户主键必然重复',0,'分组内去重不保证跨组互斥；全局去重指标不能总由组内去重数直接相加。')
q(5,'销售记录 quantity=3，amount=60。页面把 COUNT(*) 标成“销售件数”，问题是什么？','把记录数当作商品数量|COUNT(*) 不能查询销售表|amount 应该是 3|没有问题',0,'一条记录可含多件商品，应使用 SUM(quantity)；指标标题必须与公式对应。')
q(5,'想比较“2024 年售出的车”的后续服务，哪些口径必须明确？','售后观察截止日期|是否只统计购车后服务|维修与保养是否都算|可以把 2025 年购车全部算进去而不改标题',[0,1,2],'人群归属按销售年份，服务观察期另行定义；两者不能混用。')
q(5,'有 4 辆车，只有 2 辆发生维修，费用分别 100、300 元。平均每辆车维修成本（含未维修车）为？','200|100|400|50',1,'总成本 400 除以全部 4 辆车是 100；按有维修车辆平均则为 200。')
q(5,'销售表的门店城市与客户所在城市不同，分析销售城市业绩应使用？','sales.store_city|customers.city|任选一个|把两者拼接后按字符串金额汇总',0,'客户城市是客户属性，销售城市是交易发生地点；指标维度由业务问题决定。')
q(5,'维修次数为 0 的车型，在“平均每次维修成本”报表应怎样处理？','默认解释为免费维修|保留 NULL 或明确标注无维修|伪造一次 0 元维修|强制删除车型主数据',1,'没有维修与发生零元维修是不同情况；平均值的分母为 0 时没有定义。')

case('coffee_training_2','13 · 从未卖出的商品','NOT EXISTS / 完整产品集','查出从未产生任何销售记录的 product_id、product_name，按编号排序。','以 products 为外层，检查不存在关联销售。',
'''SELECT p.product_id,p.product_name FROM products p
WHERE NOT EXISTS (SELECT 1 FROM sales s WHERE s.product_id=p.product_id)
ORDER BY p.product_id;''','product_id|product_name',[[4,'可颂']],'无销售是没有匹配记录；不能仅检查 amount=0。','改成 2024 年 2 月未售商品，将日期条件放进子查询。')
case('coffee_training_2','14 · 高于本店平均交易额','相关子查询 / 比较基准','找出单条 amount 严格高于该门店所有销售记录平均 amount 的交易，输出 sale_id、store_id、amount，按交易编号排序。','关联内外层 store_id；这里平均的是销售记录金额，不是每件单价。',
'''SELECT s.sale_id,s.store_id,s.amount FROM sales s
WHERE s.amount>(SELECT AVG(x.amount) FROM sales x WHERE x.store_id=s.store_id)
ORDER BY s.sale_id;''','sale_id|store_id|amount',[[2,1,60],[3,1,60],[5,2,60]],'北京店均额 45，上海店 55；等于平均值的交易不保留。','加入窗口 AVG 写法，对照结果是否相同。')
case('coffee_training_2','15 · 每店最近一条销售','ROW_NUMBER / 同日决胜','每个有销售门店取最新记录；日期相同取 sale_id 最大的一条。返回 store_id、sale_id、sale_date、amount，按门店排序。','窗口按日期和 ID 双降序，外层筛 rn=1。',
'''WITH ranked AS (
 SELECT *,ROW_NUMBER() OVER(PARTITION BY store_id ORDER BY sale_date DESC,sale_id DESC) AS rn
 FROM sales
)
SELECT store_id,sale_id,sale_date,amount FROM ranked WHERE rn=1 ORDER BY store_id;''','store_id|sale_id|sale_date|amount',[[1,4,'2024-02-01',20],[2,6,'2024-03-01',50]],'MAX(sale_date) 再回连在同日多行时可能返回多条；ROW_NUMBER 明确一条。','只看 1 月，北京店最新是 sale_id=3，上海店是 5。')
case('coffee_training_2','16 · 每店收入占全链比例','汇总 / 窗口分母','返回全部门店 store_id、revenue、share_pct；无销售门店收入与占比均为 0。占比保留两位小数，按编号排序。全链无收入时比例为 NULL。','先各店汇总，外层 SUM(revenue) OVER() 取得统一分母。',
'''WITH totals AS (
 SELECT st.store_id,COALESCE(SUM(s.amount),0) AS revenue
 FROM stores st LEFT JOIN sales s ON s.store_id=st.store_id GROUP BY st.store_id
)
SELECT store_id,revenue,ROUND(revenue/NULLIF(SUM(revenue) OVER(),0)*100,2) AS share_pct
FROM totals ORDER BY store_id;''','store_id|revenue|share_pct',[[1,180,62.07],[2,110,37.93],[3,0,0]],'分母为 290；如果先过滤门店再算窗口，分母会变成所选门店合计。','先算全链分母再筛北京店，验证占比仍为 62.07%。')
case('coffee_training_2','17 · 类别收入横向展示','条件聚合 / 零值','每店一行输出 store_id、coffee_revenue、pastry_revenue，含零销售门店；按编号排序。分类值为“咖啡”“糕点”。','关联商品后，用 SUM(CASE WHEN ... THEN amount ELSE 0 END)。',
'''SELECT st.store_id,
 SUM(CASE WHEN p.category='咖啡' THEN s.amount ELSE 0 END) AS coffee_revenue,
 SUM(CASE WHEN p.category='糕点' THEN s.amount ELSE 0 END) AS pastry_revenue
FROM stores st LEFT JOIN sales s ON s.store_id=st.store_id
LEFT JOIN products p ON p.product_id=s.product_id
GROUP BY st.store_id ORDER BY st.store_id;''','store_id|coffee_revenue|pastry_revenue',[[1,180,0],[2,60,50],[3,0,0]],'不要用 COUNT(CASE ... ELSE 0 END) 计算次数，更不能把次数当金额。','增加各类别售出数量列，比较数量与金额的差异。')
case('coffee_training_2','18 · 最近三笔移动平均','ROWS / 明细保留','按每店 sale_date、sale_id 升序，求当前及前两笔交易金额的平均值 avg_last3，保留两位小数。输出 store_id、sale_id、amount、avg_last3，按同样顺序展示。','ROWS BETWEEN 2 PRECEDING AND CURRENT ROW；起始不足三条按实际条数平均。',
'''SELECT store_id,sale_id,amount,
 ROUND(AVG(amount) OVER(PARTITION BY store_id ORDER BY sale_date,sale_id
 ROWS BETWEEN 2 PRECEDING AND CURRENT ROW),2) AS avg_last3
FROM sales ORDER BY store_id,sale_date,sale_id;''','store_id|sale_id|amount|avg_last3',[[1,1,40,40],[1,2,60,50],[1,3,60,53.33],[1,4,20,46.67],[2,5,60,60],[2,6,50,55]],'这是最近三笔记录，不是最近三天；第一笔窗口只有自己。','改成日粒度并补齐日期，再计算三日移动平均。')
case('ev_training_2','19 · 车型内的售价档位','DENSE_RANK / 并列','为全部车辆按车型分区，按售价降序计算 price_rank。返回 vin、model、sale_price、price_rank，按 VIN 排序。','排名窗口只按售价排序，不加入 VIN；外层再按 VIN 展示。',
'''SELECT vin,model,sale_price,
 DENSE_RANK() OVER(PARTITION BY model ORDER BY sale_price DESC) AS price_rank
FROM vehicles ORDER BY vin;''','vin|model|sale_price|price_rank',[['V1','Model S',30,1],['V2','iX3',20,1],['V3','Model S',30,1],['V4','NIO ET7',40,1]],'同车型同价并列为 1；窗口并列规则与输出顺序分别指定。','将 V3 售价改为 31 后，它排名 1，V1 排名 2；在副本库验证。')
case('ev_training_2','20 · 车型维修成本与覆盖','条件聚合 / 分母','按车型输出 model、repair_events、repaired_vehicles、avg_repair_cost；包含无维修车型，平均每次维修成本为 NULL。按二进制车型名排序，成本单位元。','COUNT 条件分支不写 ELSE 0；车辆数用条件 DISTINCT。',
'''SELECT v.model,
 COUNT(CASE WHEN r.service_type='维修' THEN r.service_id END) AS repair_events,
 COUNT(DISTINCT CASE WHEN r.service_type='维修' THEN v.vin END) AS repaired_vehicles,
 ROUND(AVG(CASE WHEN r.service_type='维修' THEN r.cost END),2) AS avg_repair_cost
FROM vehicles v LEFT JOIN service_records r ON r.vin=v.vin
GROUP BY v.model ORDER BY v.model COLLATE utf8mb4_bin;''','model|repair_events|repaired_vehicles|avg_repair_cost',[['Model S',1,1,1000],['NIO ET7',0,0,'NULL'],['iX3',0,0,'NULL']],'免费软件升级不进入维修的次数、车辆数或均值分母。','新增同车第二次维修，维修次数增加，但维修车辆数不增加。')
case('ev_training_2','21 · 标记首次服务','ROW_NUMBER / CASE','输出 vin、service_id、is_first，首次服务标记 1，其余 0；每车按 service_date、service_id 确定顺序，最终也按此顺序排列。','内层排名，外层 CASE；每个 VIN 单独重启序号。',
'''WITH ranked AS (
 SELECT *,ROW_NUMBER() OVER(PARTITION BY vin ORDER BY service_date,service_id) AS rn
 FROM service_records
)
SELECT vin,service_id,CASE WHEN rn=1 THEN 1 ELSE 0 END AS is_first
FROM ranked ORDER BY vin,service_date,service_id;''','vin|service_id|is_first',[['V1',1,1],['V1',2,0],['V1',5,0],['V2',3,1],['V2',4,0]],'每车只有一条首次；同日多条通过 service_id 打破并列。','如果业务要求“首次服务日全部记录”，应先取最早日期，而不是强制一条。')
case('ev_training_2','22 · 每车服务成本累计','SUM 窗口 / 同日记录','输出 vin、service_id、cost、running_cost，累计到当前服务记录，按 VIN、日期、服务 ID 排序；费用单位元。','显式 ROWS，日期相同再按服务 ID，保证逐条累计。',
'''SELECT vin,service_id,cost,
 SUM(cost) OVER(PARTITION BY vin ORDER BY service_date,service_id
 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_cost
FROM service_records ORDER BY vin,service_date,service_id;''','vin|service_id|cost|running_cost',[['V1',1,300,300],['V1',2,1000,1300],['V1',5,0,1300],['V2',3,200,200],['V2',4,0,200]],'零元服务保留明细但不增加累计费用；不同车辆累计独立。','要求当日全部累计值相同，应先按车辆与日期汇总。')
case('ev_training_2','23 · 多次购车客户','GROUP BY / HAVING','查询至少有两条销售记录的客户 customer_id、name、purchase_count、revenue_wan，按客户编号排序。每条销售记录视为一笔购车。','先连接客户、销售和车辆，再按客户分组，HAVING COUNT(*)>=2。',
'''SELECT c.customer_id,c.name,COUNT(*) AS purchase_count,SUM(v.sale_price) AS revenue_wan
FROM customers c JOIN sales s ON s.customer_id=c.customer_id
JOIN vehicles v ON v.vin=s.vin
GROUP BY c.customer_id,c.name HAVING COUNT(*)>=2 ORDER BY c.customer_id;''','customer_id|name|purchase_count|revenue_wan',[[1,'张伟',2,60]],'客户张伟有两笔销售，分别对应 V1 和 V3；不要连接售后明细导致购车次数放大。','若一条销售可撤销，先定义有效销售条件再聚合。')
case('ev_training_2','24 · 已售但从未维修的车辆','NOT EXISTS / 人群定义','输出已售车辆 vin、model，包括做过保养或升级但从未维修的车辆，按 VIN 排序。未售车辆不返回。','同时要求存在销售且不存在维修服务，不是不存在任何服务。',
'''SELECT v.vin,v.model FROM vehicles v
WHERE EXISTS (SELECT 1 FROM sales s WHERE s.vin=v.vin)
AND NOT EXISTS (
 SELECT 1 FROM service_records r WHERE r.vin=v.vin AND r.service_type='维修'
) ORDER BY v.vin;''','vin|model',[['V2','iX3'],['V3','Model S']],'V2 做过保养与升级但没有维修；V3 没有任何售后也符合；V4 未售，不在人群中。','改成已售且从未进行任何售后，结果只应剩 V3。')
