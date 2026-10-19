"""Local content builder; uses only the existing workbook and authored content."""
from pathlib import Path
import json, re

ROOT = Path(__file__).parent
path = ROOT / '2.html'
s = path.read_text(encoding='utf-8')
assert 'SQL_PRO_EXPANSION' not in s, 'Expansion already installed'
def js(x): return json.dumps(x, ensure_ascii=False).replace('</', '<\\/')

# Each line: question | four choices | correct choice (1-based) | explanation.
groups = {
'关系语义与反例': '''一张订单有两件商品、三次支付回调，直接同时连接两张明细表会得到几行？|2|3|5|6|4|两个一对多关系相乘为六行；分别归并到订单粒度，再连接。DISTINCT 金额会误删同额订单。
SUM(DISTINCT amount) 能作为连接膨胀的通用修复吗？|能，永远正确|不能，同额不同业务事实会被合并|只要金额非空就能|只要加索引就能|2|去重值不等于去重事实。用两笔金额相等的独立订单即可构造反例。
要求买过全部必修商品的用户，最贴切的逻辑是？|购买数大于零|不存在一件必修商品是该用户没买过的|商品名包含全部|用户数等于商品数|2|这是关系除法，可用双重 NOT EXISTS。必修集合为空时所有候选用户满足，须确认业务是否接受。
EXISTS 子查询 SELECT NULL 与 SELECT 1 有什么语义区别？|前者永远假|前者忽略空行|存在性判断相同|后者必定更快|3|EXISTS 关注是否存在行，而不是投影值；不能仅凭常量推断速度。
需要找两份快照的差异，为什么只比较 COUNT(*) 不够？|COUNT 不允许用于快照|同样行数可以有完全不同的键和值|COUNT 自动去重|COUNT 一定溢出|2|至少比较缺失键、新增键和匹配键的值；同时约定 NULL 比较语义。
在 MySQL 中，a 与 b 都为 NULL 时，a <=> b 的值是？|NULL|0|1|报错|3|NULL 安全等号把两个 NULL 判为相等，适合比对可空字段；普通等号返回 UNKNOWN。
统计从未下单用户时，哪种测试数据最能暴露 NOT IN 的陷阱？|订单金额相同|订单中的 user_id 包含 NULL|用户名很长|用户 ID 连续|2|NOT IN 的集合包含 NULL 会让不匹配值变为 UNKNOWN。若字段约束非空，则此特定陷阱不存在。
外连接后 COUNT(*)=1，能认定该用户有一笔订单吗？|能|不能，可能只有一行 NULL 扩展行|只能在周末认定|加 DISTINCT 就能|2|统计右侧非空主键才能区分无匹配行；用零订单用户验证。''',
'窗口与序列难题': '''按时间求逐笔累计且时间可能重复，应怎样写？|仅 ORDER BY 时间，省略 frame|ORDER BY 时间,唯一ID 并显式 ROWS|使用 GROUP BY 金额|删除重复时间|2|稳定排序键与 ROWS 一起明确逐笔边界；默认 RANGE 会把同值 peers 纳入。
LAST_VALUE 要得到分区最后一条，关键是什么？|只写 DESC|COUNT(*)|把 frame 终点扩展到 UNBOUNDED FOLLOWING|把 NULL 转零|3|LAST_VALUE 受当前窗口 frame 影响；常见默认 frame 只到当前 peer 组。
每天多次登录，求连续登录天数的第一步是什么？|先按用户和日期去重|按原始事件 ROW_NUMBER|删除周末|先 LIMIT 7|1|连续天数以日期为粒度；重复登录会破坏日期减序号形成的分组键。
30 分钟无行为开启新会话，间隔恰好 30 分钟是否新会话？|必定是|必定不是|由业务对大于还是大于等于的约定决定|由主键决定|3|先固定边界，再用 LAG 标记新会话，最后累计标记生成会话号。
各部门最高三个不同薪资档位并保留并列，用哪个函数？|ROW_NUMBER|DENSE_RANK|NTILE(3)|COUNT|2|DENSE_RANK 的前三级对应三个不同薪资值；ROW_NUMBER 限制行数，RANK 可能跳号。
按天补零后做 ROWS BETWEEN 6 PRECEDING AND CURRENT ROW，得到什么？|七笔订单合计|连续七个日历日合计，但开头可能不足七天|自然周合计|最近六天不含今天|2|必须先得到每天恰好一行，且补齐日期；要完整窗口需提供报告开始前六天的数据。
需要一月份每日七日均值，为什么不能先只取一月份原始记录？|窗口不能跨年|一月前六天会缺少十二月上下文|AVG 不支持日期|只能用存储过程|2|先取足够历史并计算窗口，最后在外层筛展示日期。
把唯一订单 ID 放进 DENSE_RANK 的 ORDER BY 金额后，会怎样？|仍按金额并列|相同金额的不同订单不再并列|全部排名为一|自动去重|2|窗口排序的整组值决定 peers；用于显示的稳定顺序可放到最外层 ORDER BY。''',
'增长分析与时间口径': '''D1 留存应优先明确什么？|SQL 长度|队列日期、时区、活跃定义和分母|索引名称|图表颜色|2|先定义注册日还是首活日、自然日还是 24 小时，以及可观察窗口，再写 SQL。
昨天注册用户的 D7 留存应如何报告？|全部算流失|全部算留存|标为尚未成熟，不进入已成熟 D7 分母|按今天活跃猜测|3|观察窗未结束不能当作失败，否则会系统性低估留存。
漏斗要求浏览后加购再支付，只判断三个事件都出现是否够？|够|不够，还需顺序、时间窗和主体口径|事件去重就够|按事件名称排序就够|2|乱序事件也可能都出现；还需决定跨会话转化和多次进入漏斗如何归属。
月增长率中上月收入为零，最合理的默认处理是什么？|无穷大字符串直接参与平均|NULL 并单独标识无基期|固定 100%|固定 0%|2|除零没有通常意义上的增长率，NULLIF 可保护分母，但展示和汇总策略仍需明确。
汇总转化率应该如何做？|平均每天转化率|总转化人数除以口径一致的总分母|选最大转化率|总收入除天数|2|简单平均会隐含每天等权；跨日去重用户指标还不能直接相加，需回到目标粒度。
订单在一月支付、二月退款，现金流口径怎么分期？|全部归一月|一月记流入、二月记流出|忽略退款|全部归二月|2|现金流按资金事件发生日；订单生命周期净额则可回溯订单期，两者不能混用。
时间查询优先使用 [开始,结束) 有什么好处？|保证使用索引|相邻区间无重叠，避免小数秒上界漏洞|自动转换时区|自动补齐日期|2|半开区间便于拼接，包含开始排除结束；索引与时区仍需要另外处理。
UTC 存储、台北自然日统计，应先明确什么？|服务器显示语言|台北日界线对应的 UTC 时间边界|只截取字符串前十位|把所有时间加一天|2|用业务时区确定区间，再比较原列；不要假定连接会话时区总是正确。''',
'索引设计与执行计划': '''查询 WHERE tenant_id=? AND created_at>=? ORDER BY created_at,id，优先评估哪个索引？|(created_at,tenant_id)|(tenant_id,created_at,id)|(id,tenant_id)|(amount)|2|等值前缀之后支持时间范围与排序；是否最终采用仍需根据实际数据与执行计划验证。
覆盖索引的主要价值是？|永远零 I/O|可从索引取得所需列，减少访问表记录|取消事务锁|强制所有查询最快|2|覆盖减少额外访问，但索引越宽写入、缓存和空间成本越高。
执行计划估计一行、实际十万行，下一步优先检查什么？|立刻强制索引|统计信息、数据倾斜及谓词相关性|删库|把 LIMIT 改大|2|估计偏差可能让连接顺序和访问路径不合适；先复现实测，再提出可验证改动。
为什么小样本上索引快不代表线上快？|线上不支持索引|数据规模、分布、缓存和并发不同|索引只在本机生效|主键永远更慢|2|基准必须说明行数、选择性、冷热缓存、并发和重复次数，至少比较延迟分布。
深 OFFSET 分页常见代价是什么？|只读返回的二十行|仍需处理被跳过的大量记录|必定锁全表|必定无法排序|2|可评估基于稳定复合排序键的游标分页；它改变随机跳页能力，需与产品需求一致。
EXPLAIN ANALYZE SELECT 的关键注意点是什么？|仅解析，不执行|实际执行查询，应控制数据和代价|会自动建索引|只能分析空表|2|MySQL 8.0.18+ 支持该能力；本练习只使用 SELECT，并在可控环境测量。
Using filesort 能直接认定性能差吗？|能|不能，应看待排序行数、耗时和整体代价|它意味着磁盘损坏|它表示没有 WHERE|2|名称不代表一定落盘；小结果集排序往往合理，不能靠某个 Extra 标签打分。
给所有字段分别建索引为什么通常不是专业方案？|MySQL 最多一个索引|写入维护成本高，且未必匹配组合访问路径|普通索引不存值|索引不占空间|2|按实际查询族设计少量有价值的索引，测量读收益和写放大，再去除冗余。''',
'事务与并发控制': '''两个事务先读余额再各自写回计算值，主要风险是什么？|SQL 不能加法|丢失更新|主键自动重复|自动串行化|2|用带条件的原子 UPDATE 或在事务中锁定读取，并校验受影响行数；明确不足余额时的回滚。
扣库存更稳健的基本语句是？|UPDATE stock SET qty=qty-1|UPDATE stock SET qty=qty-1 WHERE sku_id=? AND qty>=1|先 SELECT 后无条件 UPDATE|DELETE FROM stock|2|在匹配目标行的同时检查库存，受影响行数为一才表示成功；订单写入须纳入同一事务。
事务收到死锁错误后应如何处理？|只重发最后一条语句即可永远正确|回滚/确认回滚后，以有界重试重新执行整个业务事务|永久关闭锁|忽略错误返回成功|2|重试需幂等、退避和上限；不能把失败前内存计算值当作仍然有效。
所有业务按账户 ID 升序锁两行，主要帮助是什么？|消除所有死锁|降低锁顺序不一致造成的死锁概率|取消隔离级别|保证无超时|2|统一加锁顺序是降低风险的手段，不能承诺所有访问路径都不再死锁。
SELECT ... FOR UPDATE 在自动提交的单条语句后，还能保护下一条 UPDATE 吗？|能，永久锁住|不能，锁的保护需要覆盖业务事务|只有 VARCHAR 能|只看索引名称|2|在显式事务中读取并更新，提交前保持必要锁；避免持锁期间进行网络调用。
InnoDB 可重复读下普通一致性读与锁定读可以混为一种快照吗？|可以|不可以，锁定读与一致性快照读语义不同|只有空表相同|锁定读不返回数据|2|不要把可重复读理解为所有语句永远看到同一版本；设计双会话步骤验证具体读取行为。
长事务为何会拖累系统？|事务名太长|可能延长锁持有并阻碍旧版本清理|会删除所有索引|导致 DECIMAL 变 FLOAT|2|缩短事务，定位开始时间和持锁语句；业务接口等待时间也应算入事务持续时间。
支付请求超时后重试，怎样避免重复入账？|相信网络只投递一次|唯一业务幂等键与账务事务共同约束|每次生成新的随机业务键|先睡一秒|2|唯一键保证同一业务请求不重复落库；相同键但不同金额应拒绝或报冲突。''',
'建模约束与金额': '''保存财务金额通常优先选择什么？|FLOAT|DECIMAL 并明确精度、币种与舍入规则|VARCHAR 随意存|DOUBLE 永远精确|2|二进制浮点不能精确表示所有十进制小数；还需确定行级还是汇总后舍入。
为什么订单明细要保存成交单价快照？|减少列数|历史金额不能随商品当前价格变动|商品表不能 JOIN|为了不用主键|2|交易事实记录当时价格、税和折扣；当前商品维度不是历史账单的可靠来源。
约束用户邮箱唯一时，还需要考虑什么？|只考虑长度|NULL、大小写、排序规则以及业务规范化|表的颜色|主键是否连续|2|唯一索引与排序规则共同影响相等性；MySQL 唯一索引允许多个 NULL，不等于唯一非空业务标识。
CHECK(amount>0) 是否单独排除了 NULL？|是|否，还需 NOT NULL|只对负数允许 NULL|自动补零|2|CHECK 接受 TRUE 或 UNKNOWN；若不允许缺值，要显式 NOT NULL。
保存多币种金额后直接 SUM(amount) 的问题是什么？|SUM 不支持 DECIMAL|不同币种不能直接相加|只要保留两位就正确|只有负数才有问题|2|按币种分别汇总，或明确汇率来源、时点和舍入规则后转换。
软删除表用 UNIQUE(email,deleted_at) 能确保只有一个未删除邮箱吗？|能|不能，NULL 组合可能允许多个活跃行|只有邮箱短时能|加 ORDER BY 就能|2|可设计仅活跃行产生规范邮箱、已删除产生 NULL 的生成列，再在该列上建唯一索引，需验证版本和规则。
外键存在是否就意味着业务流程合法？|是|否，外键主要保证引用存在，不能替代状态迁移规则|外键禁止事务|外键会检查所有支付金额|2|已取消订单能否发货等跨字段、跨状态规则需另行设计并发安全的校验。
多租户订单关联明细时最重要的约束之一是什么？|按姓名关联|确保 tenant_id 与业务键共同隔离，防止跨租户关联|删除所有外键|租户名越长越好|2|全局唯一 ID 也不能替代授权检查；复合键或约束可进一步防止错误跨租户引用。''',
'数据管道与质量': '''增量按 updated_at > 上次最大时间推进，最典型的遗漏是什么？|所有未来记录|相同时间戳边界或晚到更新|所有非空值|所有主键|2|用复合游标、重叠窗口和幂等合并；仅加 >= 会带来重复，需要去重策略。
同一批数据重跑后结果不变，称为什么？|随机性|幂等性|笛卡尔积|串行扫描|2|原始数据和口径相同的前提下，重跑不重复入账、不重复累加，是管道可靠性的核心要求。
CDC 删除事件若被忽略，会怎样？|目标表更准确|目标表可能永久保留已删除记录|自动触发目标删除|只影响排序|2|增量同步应明确插入、更新、删除、乱序、重复投递和断点恢复。
SCD Type 2 的有效期通常采用什么边界？|两端包含且允许重叠|左闭右开并保证同一业务键不重叠|所有版本都无结束时间|只存当前值|2|事实时间匹配 valid_from<=t AND t<valid_to；当前开放区间需约定表示方法。
维表晚到但事实已到，应该怎样设计？|永久丢弃事实|隔离/未知维度占位并提供后续回补机制|随便关联一位用户|改掉事实时间|2|选择取决于时效和准确性要求，必须保留可追溯键、补偿机制和监控。
对账只比较总金额是否足够？|足够|不够，正负误差可能抵消|只要保留小数就够|只需比较最大值|2|分键比较、计数、缺失、重复、逐笔差额与总额共同验证；总额一致不意味着明细一致。
抽样数据完全正确，能证明全量没有重复键吗？|能|不能，仍需全量约束或检查|抽十行即可|抽样自动去重|2|唯一约束可在写入时强制不变量；离线检测可 GROUP BY key HAVING COUNT(*)>1。
修复脏数据前最应该先交付什么？|直接全表 UPDATE|受影响键清单、修复规则和回滚/恢复方案|删除日志|禁用所有校验|2|先用 SELECT 预览和统计范围，保存审计证据，分批执行并复核；这是工程题的验收内容。''',
'递归与复杂查询': '''递归 CTE 查询组织树，为什么要考虑环？|树一定没有环|脏数据可能让递归无法按预期终止|WITH 不支持条件|主键会自动打破环|2|约束深度、记录访问路径并检测重复节点；递归上限是保护措施，不是正确性证明。
递归 CTE 拼接越来越长的路径，锚点列应该注意什么？|永远写空字符串即可|显式 CAST 到足够宽的字符类型|必须是 INT|不允许别名|2|递归列类型由非递归部分推导；太窄可能触发数据过长错误。
区间合并时只比较当前开始与上一行结束，何时可能错？|区间互不相交|之前存在一个覆盖多行的长区间|按开始排序时永远正确|所有区间长度为一|2|应与之前所有结束值的运行最大值比较；嵌套区间会击穿简单 LAG(end)。
求中位数时偶数行应取什么？|最小值|中间两项的平均，按约定处理 NULL|随便取一个|最大值|2|先过滤 NULL，确定排序与总行数；取中心位置再 AVG，空集结果需约定。
MySQL 8 中筛选窗口函数结果的通用写法是什么？|同层 WHERE rn=1|CTE 或派生表外层 WHERE rn=1|GROUP BY rn 永远可用|必须创建永久表|2|窗口结果在同层 WHERE 中尚未可用；不要照搬其他方言的 QUALIFY。
JSON 中缺失字段和 SQL NULL 应如何处理？|一律转换空字符串|区分缺失、JSON null、SQL NULL 和类型不符|都自动是零|只看 JSON 长度|2|显式定义抽取路径、期望类型及错误处理；保留脏数据以便排查。
递归生成一百年日历适合不加限制直接运行吗？|适合|不适合，应考虑递归限制并优先评估持久日历表|日期不能生成|只要 UNION 去重即可|2|小范围教学可用递归；大范围生产日历宜预建并索引，包含业务日和节假日属性。
查询有结果但排序未写 ORDER BY，能依赖主键升序吗？|能|不能，结果顺序没有保证|只要 LIMIT 就能|加 WHERE 就能|2|访问路径、并行和版本变化都可能改变顺序；验收应区分有序与无序结果。''',
'安全发布与恢复': '''防 SQL 注入的首选是什么？|用字符串拼接并删除空格|参数化值并对白名单标识符做验证|给表改名|隐藏按钮|2|值使用绑定参数；动态列名和排序方向通常不能作为普通值绑定，应白名单映射。
应用只需读报表，应授予什么权限？|全局 ALL|所需对象的最小读取权限|DROP 权限|管理员账号共享|2|区分迁移、应用、分析和备份身份；日志与导出也需要数据访问边界。
备份文件存在，是否意味着可恢复？|是|否，要在隔离环境恢复并核验数据与时间目标|文件大就行|压缩成功就行|2|记录恢复步骤、耗时、完整性和业务抽查；恢复演练比文件存在更能证明能力。
RPO 和 RTO 分别关注什么？|查询数和索引数|可接受数据损失窗口和恢复时间目标|用户名和密码|锁数和连接数|2|由业务容忍度驱动备份、日志保留、复制与恢复方案，不能仅报备份频率。
增加非空列上线，合理流程是什么？|立刻加 NOT NULL 且不看旧数据|兼容写入、分批回填、验证后收紧约束|先删旧表|强制所有连接中断|2|根据版本、DDL 算法与表规模验证锁和重建成本；应用的新旧版本需要短期兼容。
只读副本刚写完就读不到数据，首先考虑什么？|主键自动丢失|复制延迟与读写一致性策略|SELECT 必须提交|所有副本永久坏掉|2|写后读可路由主库或使用可验证的复制进度策略；不能假设副本即时可见。
在线 DDL 是否必定完全不阻塞业务？|是|否，仍需考虑元数据锁及算法限制|只影响 SELECT 名称|永远不耗磁盘|2|长事务可能阻碍元数据锁获取；在接近生产的环境测量，并准备停止或回退策略。
慢查询优化发布的验收应包含什么？|只看 SQL 更短|结果等价、延迟分布、资源和写入影响、回退方案|只看索引已创建|只看单次最快值|2|性能改动也可能改变结果或写入成本；记录基线、对照实验和可回退步骤。''',
'专业审题与排障': '''题目要求用户数，第一件事是什么？|COUNT(*)|明确用户标识、去重范围、时间窗和排除规则|按名字去重|选择最快函数|2|同名不等于同人；指标定义先于实现，避免返回看似正确的数字。
两段 SQL 在当前十行样例上一致，可以认定等价吗？|可以|不可以，需要考虑约束并构造 NULL、重复和空集等反例|加 LIMIT 就可以|输出列名相同即可|2|样例只能提供证据；对复杂查询要在假设下推理，并做有针对性的边界验证。
SQL 执行很慢，第一步最好是？|立刻重启数据库|确认慢的范围、时间、查询参数与等待类型|删除索引|升级所有机器|2|区分 CPU、I/O、锁等待、连接池和客户端传输；不同瓶颈需要不同方案。
性能测试只记录平均耗时的问题是？|平均没有数学意义|会掩盖尾延迟和偶发等待|平均总是最大值|不能记录平均|2|同时记录样本数、p50/p95、错误率和吞吐；不要把不同负载下的均值直接比较。
加索引后结果相同但写入慢了，怎么判断是否成功？|只看读查询|按读写负载和业务目标综合评估|索引总是成功|立即删除所有索引|2|索引优化是有成本的取舍，需要测量总体收益和资源预算。
题目未定义并列第一是否只取一行，应怎样处理？|随机返回一行|先明确并列规则，再选择排名函数|默认删除并列|按名字最短取|2|专业能力包括识别需求歧义；可在交付中明确采用的规则并提供另一种版本。
一个可复现 SQL 缺陷报告至少要包括什么？|截图标题|DDL、最小数据、SQL、预期与实际、版本和会话设置|仅一句慢了|账号密码|2|不要放敏感凭据；最小可复现样例能区分数据问题、口径问题和引擎行为。
完成训练后最有说服力的能力证据是什么？|刷题截图|可复现项目、边界测试、执行计划对照和并发实验记录|背出关键词数量|SQL 行数最多|2|专业水平来自正确性、性能、可靠性和解释能力；题量只是训练手段。'''
}
new_bank=[]
for topic, lines in groups.items():
    for line in lines.splitlines():
        q,*rest=line.split('|'); opts=rest[:4]; ans=int(rest[4])-1
        # Rotate answer positions so this is not an answer-position memorization drill.
        rotate=len(new_bank)%4
        opts=opts[rotate:]+opts[:rotate]
        new_bank.append(dict(topic=topic,type='s',q=q.replace('<','&lt;').replace('>','&gt;'),o=opts,a=[(ans-rotate)%4],e=rest[5]))
assert len(new_bank)==80

data='''-- SQL 专业训练：独立练习库。首次运行；不包含 DROP / TRUNCATE。
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
'''
labs=[]
def lab(title,topic,task,hint,sql,cols,rows,explain,extra):
    labs.append(dict(db='sql_pro_lab',title=f'{25+len(labs)} · {title}',topic=topic,task=task,hint=hint,sql=sql,cols=cols.split(','),rows=rows,explain=explain,extra=extra))
lab('订单生命周期净额','预聚合 / 对账','按订单输出所有 paid 订单的 gross、refunded、net，退款取数据中全部时间；按 id 排序。','退款先按订单汇总，再 LEFT JOIN。',
'''WITH r AS (SELECT order_id,SUM(amount) refunded FROM refunds GROUP BY order_id)
SELECT o.id,o.amount gross,COALESCE(r.refunded,0) refunded,o.amount-COALESCE(r.refunded,0) net
FROM orders o LEFT JOIN r ON r.order_id=o.id WHERE o.status='paid' ORDER BY o.id;''',
'id,gross,refunded,net',[[101,100,50,50],[102,100,0,100],[103,200,200,0],[105,300,0,300],[106,80,0,80],[107,100,0,100],[108,120,0,120]],'取消单 104 被排除；103 的二月退款仍计入生命周期净额。','将退款限定到一月底，说明 103 净额为何变成 200。')
lab('明细与退款同时关联','扇出 / 金额不变量','每笔 paid 订单输出件数 qty 与退款 refunded；不允许直接将两个明细连接后求和。','两个子表各归并到订单粒度。',
'''WITH i AS (SELECT order_id,SUM(qty) qty FROM items GROUP BY order_id),
r AS (SELECT order_id,SUM(amount) refunded FROM refunds GROUP BY order_id)
SELECT o.id,COALESCE(i.qty,0) qty,COALESCE(r.refunded,0) refunded
FROM orders o LEFT JOIN i ON i.order_id=o.id LEFT JOIN r ON r.order_id=o.id
WHERE o.status='paid' ORDER BY o.id;''','id,qty,refunded',[[101,3,50],[102,1,0],[103,2,200],[105,3,0],[106,1,0],[107,1,0],[108,1,0]],'101 有两行商品和两行退款，直接连接会有四行；qty 与退款都会被重复。','写出错误查询，记录 101 的错误结果 6 件、100 元，解释为什么 DISTINCT 不是通用修复。')
lab('每人最近两笔有效订单','Top N / 确定顺序','仅 paid，按 paid_at DESC,id DESC 选每用户最近两笔；输出按 user_id、rn 排序。','ROW_NUMBER 在过滤后的有效订单上计算。',
'''WITH x AS (SELECT user_id,id,ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY paid_at DESC,id DESC) rn
FROM orders WHERE status='paid') SELECT user_id,id,rn FROM x WHERE rn<=2 ORDER BY user_id,rn;''','user_id,id,rn',[[1,107,1],[1,102,2],[2,105,1],[2,103,2],[3,106,1],[4,108,1]],'只有一笔的用户保留一笔；无订单用户不返回。','新增同一秒两笔订单，确认 ID 决胜；另写保留并列时间的版本。')
lab('收入占比之后再筛用户','窗口分母 / 筛选位置','先按 paid 订单毛额计算所有购买用户的收入占比，最后仅展示用户 1；百分比保留两位。','窗口在筛选用户之前计算。',
'''WITH a AS (SELECT user_id,SUM(amount) revenue FROM orders WHERE status='paid' GROUP BY user_id),
b AS (SELECT user_id,revenue,ROUND(100*revenue/NULLIF(SUM(revenue) OVER(),0),2) pct FROM a)
SELECT * FROM b WHERE user_id=1;''','user_id,revenue,pct',[[1,300,30]],'paid 毛额总计 1000；提前筛 user_id 会错误地得到 100%。','改为生命周期净额，用户 1 占比应为 33.33%。')
lab('日历补零与逐日累计','递归 CTE / 空日期','输出 1 月 1–7 日 daily_gross、running_gross，paid 毛额、无订单日补零。','日历 LEFT JOIN 日汇总，再 SUM 窗口。',
'''WITH RECURSIVE cal AS (SELECT DATE('2025-01-01') d UNION ALL SELECT d+INTERVAL 1 DAY FROM cal WHERE d<'2025-01-07'),
a AS (SELECT DATE(paid_at) d,SUM(amount) v FROM orders WHERE status='paid' GROUP BY DATE(paid_at))
SELECT c.d,COALESCE(a.v,0) daily_gross,SUM(COALESCE(a.v,0)) OVER(ORDER BY c.d ROWS UNBOUNDED PRECEDING) running_gross
FROM cal c LEFT JOIN a ON a.d=c.d ORDER BY c.d;''','d,daily_gross,running_gross',[[f'2025-01-0{i}',v,r] for i,v,r in [(1,100,100),(2,300,400),(3,0,400),(4,300,700),(5,180,880),(6,0,880),(7,120,1000)]],'1 月 3 日只有取消单，收入为零；日历是报表行的来源。','把订单全部筛空，仍应得到七行零收入。')
lab('三日滚动均值','日粒度 / 窗口长度','1 月 1–7 日，按补零收入求当前及前两日均值；起始不足三天按实际天数平均，保留两位。','复用日历和日聚合，AVG 的 ROWS frame 为 2 PRECEDING。',
'''WITH RECURSIVE cal AS (SELECT DATE('2025-01-01') d UNION ALL SELECT d+INTERVAL 1 DAY FROM cal WHERE d<'2025-01-07'),
a AS (SELECT DATE(paid_at) d,SUM(amount) v FROM orders WHERE status='paid' GROUP BY DATE(paid_at))
SELECT c.d,ROUND(AVG(COALESCE(a.v,0)) OVER(ORDER BY c.d ROWS BETWEEN 2 PRECEDING AND CURRENT ROW),2) avg3
FROM cal c LEFT JOIN a ON a.d=c.d ORDER BY c.d;''','d,avg3',[[f'2025-01-0{i}',v] for i,v in enumerate([100,200,133.33,200,160,160,100],1)],'1 月 3 日均值为 (100+300+0)/3；这不是最近三笔交易。','改成要求完整三天才输出均值，前两天应为 NULL。')
lab('最长连续活跃天数','Gaps and islands','任意事件算活跃；先去重用户日，输出有活跃用户的最长连续天数。','日期减 ROW_NUMBER 形成岛屿键，先统计各岛再取 MAX。',
'''WITH d AS (SELECT DISTINCT user_id,DATE(event_at) dt FROM events),
n AS (SELECT user_id,dt,ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY dt) rn FROM d),
g AS (SELECT user_id,DATE_SUB(dt,INTERVAL rn DAY) grp FROM n),
c AS (SELECT user_id,grp,COUNT(*) days FROM g GROUP BY user_id,grp)
SELECT user_id,MAX(days) longest FROM c GROUP BY user_id ORDER BY user_id;''','user_id,longest',[[1,3],[2,1],[3,2],[4,1]],'用户 1 第一天的多次事件只算一天；用户 2 缺少 1 月 2 日。','补入用户 2 在 1 月 2 日的一个事件，其最长连续应从 1 变 3。')
lab('行为会话切分','LAG / 累计标记','仅用户 1，间隔严格大于 30 分钟开新会话，恰好 30 分钟仍同会话；按时间和 id 输出会话号。','先 LAG，再标记，再累计；直接比较时间保留秒级精度。',
'''WITH p AS (SELECT id,event_at,LAG(event_at) OVER(ORDER BY event_at,id) prev FROM events WHERE user_id=1),
f AS (SELECT *,CASE WHEN prev IS NULL OR event_at>prev+INTERVAL 30 MINUTE THEN 1 ELSE 0 END fresh FROM p)
SELECT id,SUM(fresh) OVER(ORDER BY event_at,id ROWS UNBOUNDED PRECEDING) session_no FROM f ORDER BY event_at,id;''','id,session_no',[[1,1],[2,1],[3,1],[4,2],[5,3],[6,4]],'08:10 到 08:40 正好三十分钟仍在同会话；09:11 与上次相隔三十一分钟。','加入间隔 30 分 1 秒的数据；说明按分钟截断差值会出现什么误判。')
lab('注册队列 D1 留存','Cohort / 去重分母','截至 1 月 7 日（含），按 signup_date 输出注册人数、次日任意活跃人数和百分比；包含零留存队列。','先 EXISTS 生成每用户是否 D1，再按注册日期聚合。',
'''WITH x AS (SELECT u.*,EXISTS(SELECT 1 FROM events e WHERE e.user_id=u.id
AND e.event_at>=u.signup_date+INTERVAL 1 DAY AND e.event_at<u.signup_date+INTERVAL 2 DAY) kept
FROM users u WHERE u.signup_date<='2025-01-06')
SELECT signup_date,COUNT(*) users,SUM(kept) retained,ROUND(100*SUM(kept)/COUNT(*),2) pct
FROM x GROUP BY signup_date ORDER BY signup_date;''','signup_date,users,retained,pct',[['2025-01-01',2,1,50],['2025-01-02',1,1,100],['2025-01-03',1,0,0],['2025-01-05',1,0,0]],'采用注册自然日加一天，不是注册后 24 小时；样例队列均已成熟。','新增 1 月 7 日注册用户，确认不会被算作 D1 流失。')
lab('严格顺序漏斗','存在性 / 事件顺序','找出存在 view→cart→pay 严格递增时间链、且首尾不超过一小时的用户；允许跨会话，用户只输出一次。','相关 EXISTS 避免多个事件链导致重复用户。',
'''SELECT u.id FROM users u WHERE EXISTS (
SELECT 1 FROM events v JOIN events c ON c.user_id=v.user_id AND c.kind='cart' AND c.event_at>v.event_at
JOIN events p ON p.user_id=v.user_id AND p.kind='pay' AND p.event_at>c.event_at
WHERE v.user_id=u.id AND v.kind='view' AND p.event_at<=v.event_at+INTERVAL 1 HOUR) ORDER BY u.id;''','id',[[1]],'用户 2 的 pay 发生在 view 之前，而且没有 cart，不是有效转化。','设计重复浏览和重复支付样例，证明结果仍然每人一行。')
lab('现金流与订单净额分开','UNION ALL / 时间归属','按月统计 paid 订单资金流入减退款流出；退款按退款日期，按月输出 net_cash。','把退款取负数，用 UNION ALL 合并事件流水。',
'''WITH flow AS (SELECT paid_at t,amount v FROM orders WHERE status='paid'
UNION ALL SELECT r.refunded_at,-r.amount FROM refunds r JOIN orders o ON o.id=r.order_id WHERE o.status='paid')
SELECT DATE_FORMAT(t,'%Y-%m') month,SUM(v) net_cash FROM flow GROUP BY DATE_FORMAT(t,'%Y-%m') ORDER BY month;''','month,net_cash',[['2025-01',950],['2025-02',-200]],'全周期现金流合计 750；一月现金净流入 950，不等于一月订单最终净额 750。','增加取消订单退款的脏数据，说明要隔离还是纳入冲正，先定义口径。')
lab('首次购买后七天复购','首笔 / 有界时间窗','以 paid_at,id 确定首笔 paid；输出首笔之后且不晚于首笔时间加七天的其它有效订单数，含未买用户。','ROW_NUMBER 找首笔，再 LEFT JOIN 用户和后续订单。',
'''WITH x AS (SELECT *,ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY paid_at,id) rn FROM orders WHERE status='paid'),
f AS (SELECT * FROM x WHERE rn=1)
SELECT u.id,COUNT(o.id) repurchases FROM users u LEFT JOIN f ON f.user_id=u.id
LEFT JOIN orders o ON o.user_id=u.id AND o.status='paid'
AND (o.paid_at>f.paid_at OR (o.paid_at=f.paid_at AND o.id>f.id))
AND o.paid_at<=f.paid_at+INTERVAL 7 DAY GROUP BY u.id ORDER BY u.id;''','id,repurchases',[[1,2],[2,1],[3,0],[4,0],[5,0]],'同一时刻以 ID 决胜先后，七天上界包含；这是订单复购次数，不是复购用户率。','增加恰好七天及七天一秒的订单，分别应计入和排除。')
lab('有效订单金额中位数','窗口位置 / 偶数边界','计算全部 paid 订单的中位数，NULL 不适用（金额非空）。','排序编号和总行数，取 FLOOR((n+1)/2)、FLOOR((n+2)/2)。',
'''WITH x AS (SELECT amount,ROW_NUMBER() OVER(ORDER BY amount,id) rn,COUNT(*) OVER() n FROM orders WHERE status='paid')
SELECT AVG(amount) median_amount FROM x WHERE rn IN (FLOOR((n+1)/2),FLOOR((n+2)/2));''','median_amount',[[100]],'排序后为 80、100、100、100、120、200、300，中位数是第 4 项。','在副本中排除 108 后六项中位数仍为 100，再构造中间两项不相等的偶数样例。')
lab('前两档金额保留并列','DENSE_RANK / 档位','每用户取最高两个金额档位的所有 paid 订单，按 user_id、id 输出。','窗口仅按 amount 降序，不能加入 id。',
'''WITH x AS (SELECT user_id,id,amount,DENSE_RANK() OVER(PARTITION BY user_id ORDER BY amount DESC) dr FROM orders WHERE status='paid')
SELECT user_id,id,amount,dr FROM x WHERE dr<=2 ORDER BY user_id,id;''','user_id,id,amount,dr',[[1,101,100,1],[1,102,100,1],[1,107,100,1],[2,103,200,2],[2,105,300,1],[3,106,80,1],[4,108,120,1]],'用户 1 三笔都属于第一档，不能只返回两笔。','新增用户 2 第三档订单，应被排除；新增并列第二档，应被保留。')
lab('复合游标分页','Keyset / 稳定排序','paid 订单按 paid_at DESC,id DESC 排序，已读到 107（2025-01-05 09:00:00），取后面三条。','降序下一页使用小于，时间相等时比较 ID。',
'''SELECT id,paid_at FROM orders WHERE status='paid' AND
(paid_at<'2025-01-05 09:00:00' OR (paid_at='2025-01-05 09:00:00' AND id<107))
ORDER BY paid_at DESC,id DESC LIMIT 3;''','id,paid_at',[[106,'2025-01-05 09:00:00'],[105,'2025-01-04 11:00:00'],[103,'2025-01-02 10:00:00']],'只比较时间会漏掉与 107 同秒的 106。候选索引为 (status,paid_at,id)，需实测。','并发插入最新订单后继续翻页；解释游标分页仍不等于固定快照。')
lab('买过全部目标商品','关系除法 / 双重不存在','找出 paid 订单中买过 A 和 B 的用户，目标集合由 CTE 明确；按用户排序。','不存在一件目标商品未被该用户购买。',
'''WITH target AS (SELECT 'A' sku UNION ALL SELECT 'B')
SELECT u.id FROM users u WHERE NOT EXISTS (SELECT 1 FROM target t WHERE NOT EXISTS (
SELECT 1 FROM orders o JOIN items i ON i.order_id=o.id
WHERE o.user_id=u.id AND o.status='paid' AND i.sku=t.sku)) ORDER BY u.id;''','id',[[1],[2]],'多次购买同一商品不能代替买齐目标集合；取消订单不算。','把目标集合改为空集，结果应是全部用户；讨论产品是否接受空集真。')
lab('买 A 但从未买 B','半连接 / 反连接','按 paid 订单定义购买，找出买过 A 且从未买 B 的用户。','一个 EXISTS 加一个 NOT EXISTS。',
'''SELECT u.id FROM users u WHERE EXISTS (SELECT 1 FROM orders o JOIN items i ON i.order_id=o.id
WHERE o.user_id=u.id AND o.status='paid' AND i.sku='A')
AND NOT EXISTS (SELECT 1 FROM orders o JOIN items i ON i.order_id=o.id
WHERE o.user_id=u.id AND o.status='paid' AND i.sku='B') ORDER BY u.id;''','id',[[4]],'用户 1、2 都同时买过 A 和 B；用户 5 什么也没买，不符合买过 A。','用 GROUP BY 条件聚合实现同一查询，并用反例核对。')
lab('组织树路径','递归 / 路径宽度','从 CEO(id=1) 递归列出下属，含根，输出 id、depth、ID 路径，按 id 排序；限制最多 20 层并检测路径重复。','锚点 CAST 足够宽，FIND_IN_SET 防止当前路径重复节点。',
'''WITH RECURSIVE org AS (
SELECT id,0 depth,CAST(id AS CHAR(1000)) path FROM employees WHERE id=1
UNION ALL SELECT e.id,o.depth+1,CONCAT(o.path,',',e.id) FROM employees e JOIN org o ON e.manager_id=o.id
WHERE o.depth<20 AND FIND_IN_SET(e.id,o.path)=0)
SELECT id,depth,path FROM org ORDER BY id;''','id,depth,path',[[1,0,'1'],[2,1,'1,2'],[3,1,'1,3'],[4,2,'1,2,4']],'深度限制是保护，不证明数据无环；从根遍历也不能发现不连接根的环状分量。','另写检测全图孤立节点与环的方案，不要将未遍历到解释为不存在。')
lab('区间合并的嵌套陷阱','运行最大值 / 分岛','给定闭区间 [1,10]、[2,3]、[9,12]、[15,16]，重叠或端点相等就合并，输出合并区间。','比较 start 与所有前驱 end 的最大值，而非 LAG(end)。',
'''WITH a AS (SELECT 1 s,10 e UNION ALL SELECT 2,3 UNION ALL SELECT 9,12 UNION ALL SELECT 15,16),
p AS (SELECT *,MAX(e) OVER(ORDER BY s,e ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) prev_max FROM a),
f AS (SELECT *,CASE WHEN prev_max IS NULL OR s>prev_max THEN 1 ELSE 0 END fresh FROM p),
g AS (SELECT *,SUM(fresh) OVER(ORDER BY s,e ROWS UNBOUNDED PRECEDING) grp FROM f)
SELECT MIN(s) start_at,MAX(e) end_at FROM g GROUP BY grp ORDER BY start_at;''','start_at,end_at',[[1,12],[15,16]],'第三个区间虽然不与紧前面的 [2,3] 重叠，但与 [1,10] 重叠。','增加完全重复区间与零长度区间；如果相邻整数也应合并，调整条件并重测。')
lab('订单与明细对账','数据质量 / 异常检测','paid 订单金额应等于明细 qty*unit_price 合计，找出异常 id、header_total、line_total；无明细也算异常。','LEFT JOIN 聚合；区别没有明细和明细金额恰好为零。',
'''SELECT o.id,o.amount header_total,SUM(i.qty*i.unit_price) line_total FROM orders o LEFT JOIN items i ON i.order_id=o.id
WHERE o.status='paid' GROUP BY o.id,o.amount HAVING COUNT(i.order_id)=0 OR o.amount<>SUM(i.qty*i.unit_price) ORDER BY o.id;''','id,header_total,line_total',[],'当前数据应零行。零行也必须通过故意污染数据验证检测有效。','事务内将订单 101 的 A 单价改为 61，应报 101、100、101，随后 ROLLBACK。')
lab('截至指定日的用户价值','As-of / 退款截止','截至 1 月 4 日结束，输出所有用户的 paid 订单数与净额；订单和退款都必须早于 1 月 5 日。','退款和订单独立应用截止点，避免使用未来退款。',
'''WITH r AS (SELECT order_id,SUM(amount) v FROM refunds WHERE refunded_at<'2025-01-05' GROUP BY order_id),
a AS (SELECT o.user_id,COUNT(*) n,SUM(o.amount-COALESCE(r.v,0)) net FROM orders o LEFT JOIN r ON r.order_id=o.id
WHERE o.status='paid' AND o.paid_at<'2025-01-05' GROUP BY o.user_id)
SELECT u.id,COALESCE(a.n,0) orders_count,COALESCE(a.net,0) net FROM users u LEFT JOIN a ON a.user_id=u.id ORDER BY u.id;''','id,orders_count,net',[[1,2,150],[2,2,500],[3,0,0],[4,0,0],[5,0,0]],'用户全集按题意使用当前 users，所以 1 月 5 日注册的用户 5 也输出零；2 月退款不可提前扣减。','若报告要求只展示截至当日已注册用户，再过滤 signup_date<2025-01-05。')
lab('退款风险检查','约束之外 / 总额守恒','找出 paid 订单累计退款超过订单金额的记录；输出 id、amount、refunded。','外键和单条正金额 CHECK 不能限制跨行退款总和。',
'''SELECT o.id,o.amount,SUM(r.amount) refunded FROM orders o JOIN refunds r ON r.order_id=o.id
WHERE o.status='paid' GROUP BY o.id,o.amount HAVING SUM(r.amount)>o.amount ORDER BY o.id;''','id,amount,refunded',[],'订单 103 全额退款不是超额；检测条件严格大于。','事务内给 103 增加 1 元退款，应报 103、200、201；并设计并发退款防超额方案。')
lab('商品用户渗透率','去重粒度 / 共同分母','按有有效销售的 sku，输出购买用户数和占全部 paid 购买用户的百分比，按 sku 排序。','分子按 sku 去重用户，分母按全体去重用户。',
'''WITH b AS (SELECT DISTINCT o.user_id,i.sku FROM orders o JOIN items i ON i.order_id=o.id WHERE o.status='paid'),
den AS (SELECT COUNT(DISTINCT user_id) n FROM orders WHERE status='paid')
SELECT b.sku,COUNT(*) buyers,ROUND(100*COUNT(*)/NULLIF(den.n,0),2) pct FROM b CROSS JOIN den GROUP BY b.sku,den.n ORDER BY b.sku;''','sku,buyers,pct',[['A',3,75],['B',2,50],['C',1,25]],'用户可买多个商品，各商品渗透率相加超过 100% 正常；无商品明细的 paid 用户仍属于分母。','改成全部注册用户分母，比例应为 60%、40%、20%。')
lab('累计贡献达到 80%','Pareto / 阈值跨越','按每用户 paid 毛额降序、user_id 升序，取累计贡献首次达到或超过 80% 所需的最少前缀用户。','保留加入当前用户之前累计额还小于总额 80% 的行。',
'''WITH a AS (SELECT user_id,SUM(amount) v FROM orders WHERE status='paid' GROUP BY user_id),
b AS (SELECT *,SUM(v) OVER() total,SUM(v) OVER(ORDER BY v DESC,user_id ROWS UNBOUNDED PRECEDING) running FROM a)
SELECT user_id,v,running,ROUND(100*running/NULLIF(total,0),2) cumulative_pct FROM b WHERE running-v<0.8*total ORDER BY v DESC,user_id;''','user_id,v,running,cumulative_pct',[[2,500,500,50],[1,300,800,80]],'不能简单筛 running<=阈值，否则在一步跨过阈值时会漏掉必需的最后一个用户。仅适用于本题非负收入。','把用户 1 金额调为 350，验证跨过阈值的该用户仍被保留；讨论负净额为何会破坏前缀直觉。')
assert len(labs)==24

projects=[
('P1 · 电商经营报表交付','分析工程 / 4–6 小时','用新数据交付一份可复现经营日报，包含毛额、现金净流入、生命周期净额、用户转化和 D1 留存。',
 ['提交五项指标的分子、分母、粒度、时区、截止时间和退款归属说明。','提交 SQL、预期表格、至少八组边界数据（空集、重复、并列、零分母、跨月退款、晚到、无明细、未成熟队列）。','总 paid 毛额=1000、全周期退款=250、净额=750；逐单核对而非只核总额。','用分层 CTE 标出每层粒度，说明连接前后的行数变化。'],
 '参考路线：先订单与退款各自聚合，再派生现金流与生命周期口径；留存从 users 驱动。不同粒度的报表分别输出，不把所有明细一次性联表。'),
('P2 · 百万行性能实验','索引 / 4–8 小时','自行生成至少十万行、挑战一百万行 paid/cancelled 订单，模拟少数大客户和时间热点，优化时间区间查询与分页。',
 ['交付确定随机种子或确定性生成 SQL、行数、分布与机器环境；不要把八行样例的速度当结论。','比较无额外索引、(status,paid_at,id) 与适配用户查询的 (user_id,paid_at,id)；每次仅变更一个因素。','MySQL 8.0.18+ 使用 EXPLAIN ANALYZE SELECT，记录估计/实际行数、loops 与热点算子。','至少二十次重复测量，报告 p50/p95、返回行数、索引大小和批量插入开销；检查结果等价。'],
 '参考路线：先跑基线，再加候选索引；对低选择性全量查询允许优化器选择扫描。记录缓存条件，比较 OFFSET 50000 与复合游标的访问量，解释随机跳页能力的差异。'),
('P3 · 库存扣减与幂等下单','双会话实验 / 3–5 小时','设计 stock、order_request 两表，实现库存=1 时两个并发请求最多成功一次，同请求重试不重复扣库存。',
 ['DDL 要有 sku 主键、非负库存约束和请求唯一键；定义相同请求键不同商品的冲突策略。','在一个事务内建立请求幂等记录、条件 UPDATE 库存并创建订单；失败时整笔回滚。','写出 A/B 双会话逐步时间表，记录谁等待、提交结果、受影响行数和最终库存。','覆盖不同请求竞争、相同请求重放、事务中断和死锁有界重试；库存不能负，成功订单不能多于初始库存。'],
 '参考协议：BEGIN → 插入唯一请求键 → UPDATE stock SET qty=qty-1 WHERE sku_id=? AND qty>=1 → 检查 affected_rows=1 → 写订单/成功状态 → COMMIT。扣减失败回滚；重复键需读取已提交业务结果并校验请求载荷。不要仅用先查是否存在保证幂等。'),
('P4 · 转账、死锁与重试','事务 / 3–5 小时','构建两个账户各 100 元的转账实验，双会话反向转账，证明余额守恒并复现一次死锁。',
 ['先用相反顺序 FOR UPDATE 锁两账户，记录一个事务收到死锁错误以及另一事务的结果。','改成按账户 ID 升序锁定，检查余额充足后在同一事务中更新双方及唯一 transfer_id 流水。','验证成功转账总余额=200，失败转账不留单边扣款；支持重复请求不重复入账。','提交超时与死锁分别处理的策略：明确回滚、整笔有界重试、退避和幂等；不能只重发最后一句。'],
 '参考路线：流水唯一业务键提供去重，固定锁顺序降低死锁概率，原子事务维持守恒。网络超时属于结果未知，要通过业务键查询结果，不能直接假定失败。'),
('P5 · 可重跑的增量同步','数据管道 / 4–6 小时','设计 source_events → warehouse_events 增量同步，覆盖重复投递、同时间戳、晚到、更新和删除。',
 ['明确源是否具有可靠变更序号；没有时说明重叠窗口的能力边界，不能宣称永不遗漏任意晚到。','保存业务键与源版本，在事务中落数据与断点；同一输入连续跑两遍结果一致。','故障注入：写入一半中断再重跑、旧版本晚到、新版本删除、同秒两条更新。','提交全量与增量对账：缺失键、多余键、值差异、重复键；不仅核对总行数。'],
 '参考路线：有序 CDC 可使用变更位置和版本幂等合并，删除用 tombstone；普通 updated_at 扫描需复合边界、回看和定期全量核对。旧版本不能覆盖新版本。'),
('P6 · 历史维度与时间关联','SCD2 / 3–5 小时','新增用户城市历史维表，用户 1 在 1 月 3 日从北京迁往上海，计算每笔订单发生时的城市收入。',
 ['使用 [valid_from,valid_to) 定义有效区间，当前版本可为空上界；以订单时间关联。','用户 1 的 101、102 应归北京，107 归上海；边界时刻只匹配一个版本。','写检查 SQL：同一用户版本重叠、重复当前版本、事实无匹配、多重匹配。','模拟晚到的历史修正，展示受影响事实范围及重算策略，不能只修改当前城市。'],
 '参考连接条件：o.user_id=h.user_id AND o.paid_at>=h.valid_from AND (o.paid_at<h.valid_to OR h.valid_to IS NULL)。对每笔订单检查 COUNT(匹配版本)=1，NULL 城市与没有匹配记录应分开。'),
('P7 · 迁移与恢复演练','数据库工程 / 4–6 小时','在独立练习库给订单新增业务请求编号并最终强制唯一非空；设计兼容上线与恢复流程。',
 ['先提交旧数据重复/缺失检查、兼容写入方案、可重启回填与核验 SQL，再收紧约束。','解释当前 MySQL 版本下计划使用的 DDL 算法、可能的元数据锁、额外空间和失败处理；未知的需实测。','备份到独立介质或目录，再恢复到全新练习库，核对表结构、行数与逐键差异。','记录恢复耗时与可恢复时间点，说明 RPO/RTO；删列后不能靠回滚 DDL 恢复数据。'],
 '参考路线：扩展 → 新旧版本兼容 → 分批回填 → 验证 → 收紧约束 → 清理旧路径。恢复以实际演练为准；演练只作用于你新建的练习库。'),
('P8 · SQL 生产故障复盘','综合答辩 / 3–5 小时','任选一次报表金额翻倍、接口偶发超时或副本读不到刚写入数据，构造最小复现并提交故障报告。',
 ['报告包括症状、时间线、影响范围、假设、排除证据、根因和恢复动作。','提交 DDL、数据、SQL、版本与会话参数；不得只交截图或“加索引解决”。','建立修复前后对照，证明结果正确及性能达标，并写回退步骤和监控条件。','口头解释三个取舍：一致性与延迟、索引与写入、实时性与数据完整性；指出尚未解决的边界。'],
 '参考路线：金额翻倍从连接基数取证；超时先区分锁等待、扫描与客户端传输；读后写可见性检查复制延迟与路由。每个结论需要能重复的实验，避免只凭经验归因。')]

# Preserve objective IDs and old case IDs so existing browser records remain valid.
s=s.replace("const KEY=",'// SQL_PRO_EXPANSION\nBANK.push(...'+js(new_bank)+');\nconst KEY=',1)
s=s.replace('for(let i=0;i<24;i++)','for(let i=0;i<'+str(24+len(labs))+';i++)')
s=s.replace('const DATA_SQL=', 'let DATA_SQL=',1)
append='\nDATA_SQL += '+js('\n\n'+data)+';\nCASES.push(...'+js(labs)+');\n'
s=s.replace('function renderLab(){',append+'function renderLab(){',1)
s=s.replace('q.id>=60','q.id>=120')
s=s.replace('本次新增 60 题','专业拓展 80 题')
s=s.replace('120 道专项题 + 24 道 SQL 实战，从查询结果推导，到咖啡店与新能源汽车分析。','200 道专项题 + 48 道 SQL 实战 + 8 个工程挑战。从结果正确，到性能、并发、建模与恢复。')
s=s.replace('依据你的六份课堂笔记编写。','独立拓展的专业训练路线。')
s=s.replace('第二册 · 查询、分析与业务实战','SQL 专业训练营 · 第二册')
s=s.replace('<title>MySQL 专项进阶 · 第二册</title>','<title>SQL 专业训练营 · 200 题 / 48 实战 / 8 工程挑战</title>')
s=s.replace('MYSQL / WORKBOOK 02','MYSQL / PROFESSIONAL WORKBOOK')
s=s.replace('MySQL 8.0.16+','MySQL 8.0.18+')
s=s.replace('两套业务数据，二十四个分析任务','三套业务数据，四十八个分析任务')
s=s.replace('根据两份综合实战笔记，保留表名与核心字段，另编小规模边界数据：咖啡店 12 题 + 新能源汽车 12 题。数据包含零销售、缺失月份、同日服务和三个月边界；不是笔记原始全量数据。先写 SQL，再核对预期表格。','保留原有 24 题，新增电商专业实战 24 题（第 25–48 题）。覆盖留存、漏斗、连续活跃、会话切分、退款对账、递归、游标分页与区间合并。每题都有提示、解法、预期结果和反例加练。先写 SQL，再展开答案。')
s=s.replace('coffee_training_2 与 ev_training_2 两个数据库','coffee_training_2、ev_training_2、sql_pro_lab 三个数据库')
s=s.replace('不会自动删表。','不会自动删表；首次初始化后请勿在同库重复运行。新专业数据也可单独下载。')
s=s.replace('<button id="solutions">','<button id="prodata">只下载新电商数据 .sql</button> <button id="solutions">')
s=s.replace("$('#solutions').onclick=", "$('#prodata').onclick=()=>download('sql-pro-data.sql',"+js(data)+",'text/plain');$('#solutions').onclick=")
s=s.replace('实战 ${i+1} / 24','实战 ${i+1} / ${CASES.length}')
s=s.replace("${i>=12?'<span class=\"chip\">新增</span>':''}","${i>=24?'<span class=\"chip\">专业拓展</span>':''}")
s=s.replace('${Object.values(state.cases).filter(Boolean).length} / 24','${Object.values(state.cases).filter(Boolean).length} / ${CASES.length}')
s=s.replace('毕业检查：不看答案写完 24 个实战；解释 NULL、并列、无匹配、数据重复；用自己的 MySQL 查看执行计划；能解释报表的粒度、单位与时间边界。参考笔记：单表查询.md、多表查询.md、MySQL函数.md、MySQL索引和函数.md、day08_数据分析综合实战1.md、day08_数据分析综合实战2.md。','毕业检查：独立完成 48 个实战，至少完成 4 个工程挑战。查询必须通过反例测试，优化必须有执行计划和测量证据，事务必须有双会话复现，备份必须成功恢复。客观题正确率与工程能力分开评价。')
s=s.replace('120 道专项题、24 道实战','200 道专项题、48 道实战、8 个工程挑战')
s=s.replace('本页离线运行，不连接数据库。','本页离线运行，不连接数据库。新增专业题从 #121 开始；实战从 #25 开始。')
# Remove stale references from old authored text without consulting their source documents.
s=re.sub(r'\\u003cbr>\\u003cspan class=\\"muted\\">依据：.*?\\u003c/span>', '', s)
start=s.index('const LESSONS=')
end=s.index('document.querySelectorAll(\'[data-practice]\')',start)
phases=[
 ('01 / 结果正确','关系语义与反例','先完成原有基础题，再做 #121–128。重点是 NULL、空集、外连接、重复和关系除法。','交付一个能击穿错误 SQL 的最小反例。'),
 ('02 / 复杂分析','窗口与序列难题','完成窗口题与新实战 27–34、37–43。先标明每层粒度，再考虑窗口和递归。','不看答案写出连续活跃、会话切分、补零窗口与中位数。'),
 ('03 / 指标可信','增长分析与时间口径','完成留存、漏斗、现金流、截至日价值和渗透率，解释成熟队列与退款归期。','同一批数据解释毛额 1000、生命周期净额 750、一月现金流 950。'),
 ('04 / 查询够快','索引设计与执行计划','做索引题和 P2：构造数据倾斜，测量执行计划与尾延迟。','提交可重现的优化前后对照，不以 SQL 长短或索引命中作为结论。'),
 ('05 / 并发可靠','事务与并发控制','做事务题与 P3/P4。用两个 MySQL 会话观察锁、死锁、超时和重试。','库存不为负、余额守恒、同一业务请求最多记账一次。'),
 ('06 / 数据可维护','建模约束与金额','做建模题与 P5/P6：从约束、历史维度到增量同步。','数据重跑不重复，历史关联无重叠，晚到和删除有处理方案。'),
 ('07 / 能够上线','安全发布与恢复','完成安全题与 P7/P8。训练兼容迁移、最小权限、恢复和故障报告。','恢复到新库并核验；报告每项结论的实验依据。'),
 ('08 / 专业答辩','专业审题与排障','重做错题；随机抽取实战重写，至少交付四个工程挑战，其中包含性能、事务与恢复。','能解释正确性、边界、代价和取舍，才视为通过。')]
roadmap="const PHASES="+js(phases)+";\n"
roadmap+="""$('#learn').innerHTML='<div class="notice"><strong>训练目标：能独立交付可信 SQL 工作。</strong>建议按 8 个阶段推进，每阶段 3–7 天，工程挑战按实际实验耗时调整。刷完题不自动等于专家；用可复现实验和交付物验收。已有基础可直接筛选“专业拓展 80 题”。</div><div class="roadmap">'+PHASES.map(([step,t,desc,goal])=>`<article class="lesson"><div class="step">${esc(step)}</div><h2>${esc(t)}</h2><p>${esc(desc)}</p><p class="muted">验收：${esc(goal)}</p><button data-practice="${esc(t)}">进入专题 →</button></article>`).join('')+'</div><div class="panel" style="margin-top:18px"><h2>每道实战都按五步完成</h2><ol><li>用一句话定义输出粒度、范围和边界。</li><li>先独立写 SQL 并手算小样本。</li><li>在 MySQL 中运行，逐行比较预期结果；空结果不是免验。</li><li>加入至少两个反例，再验证修复前后。</li><li>解释执行计划和备选方案，将错因记在草稿中。</li></ol><p>自评分开看：正确性 40 分、边界测试 25 分、性能证据 20 分、解释与复现 15 分。错账、重复扣款或不可恢复属于关键缺陷，不能靠其他分数抵消。</p></div>';
"""
s=s[:start]+roadmap+s[end:]
s=s.replace('<button data-tab="review">','<button data-tab="engineering">工程挑战</button><button data-tab="review">')
s=s.replace('<section id="review" hidden>', '<section id="engineering" hidden></section><section id="review" hidden>')
s=s.replace("['learn','quiz','lab','review']","['learn','quiz','lab','engineering','review']")
s=s.replace("if(t==='lab')renderLab();","if(t==='lab')renderLab();if(t==='engineering')renderEngineering();")
s=s.replace('seconds:0});','seconds:0,projects:{}});')
s=s.replace('out.seconds=Number.isFinite',"if(raw.projects&&typeof raw.projects==='object')for(let i=0;i<8;i++){const p=raw.projects[i];if(p&&typeof p.note==='string'&&p.note.length<=20000)out.projects[i]={note:p.note,checks:Array.isArray(p.checks)?p.checks.filter(v=>Number.isInteger(v)&&v>=0&&v<4):[]};}\n out.seconds=Number.isFinite")
s=s.replace("if(tab==='review')renderReview();","if(tab==='review')renderReview();if(tab==='engineering')renderEngineering();")
s=s.replace('renderLab();renderReview();status(', 'renderLab();renderReview();renderEngineering();status(')
engineering='''
const PROJECTS=PROJECT_DATA;
function renderEngineering(){
 $('#engineering').innerHTML='<div class="notice">工程题没有唯一标准答案。下面给出协议或参考路线，你需要提交实验记录和可复现证据。此处的勾选仅代表自评，页面不会验证数据库状态。建议每个项目新建独立练习库。</div>'+PROJECTS.map(([title,tag,task,checks,guide],i)=>{
 const p=state.projects[i]||{note:'',checks:[]};
 return `<article class="case"><span class="chip">${esc(tag)}</span><h2>${esc(title)}</h2><p>${esc(task)}</p><h3>验收清单</h3>${checks.map((c,k)=>`<label class="opt"><input type="checkbox" data-project="${i}" data-criterion="${k}" ${p.checks.includes(k)?'checked':''}><span>${esc(c)}</span></label>`).join('')}<textarea data-project-note="${i}" aria-label="${esc(title)} 实验记录" placeholder="记录 DDL、SQL、会话时间线、测量结果、反例与结论…">${esc(p.note)}</textarea><details><summary>参考路线 / 设计要点</summary><p>${esc(guide)}</p></details></article>`;
 }).join('');
 $('#engineering').querySelectorAll('[data-project-note]').forEach(el=>el.oninput=()=>{const id=el.dataset.projectNote;state.projects[id]??={note:'',checks:[]};state.projects[id].note=el.value;save();});
 $('#engineering').querySelectorAll('[data-project]').forEach(el=>el.onchange=()=>{const id=el.dataset.project;state.projects[id]??={note:'',checks:[]};state.projects[id].checks=[...$('#engineering').querySelectorAll(`[data-project="${id}"]:checked`)].map(x=>+x.dataset.criterion);save();});
}
'''.replace('PROJECT_DATA',js(projects))
s=s.replace('setInterval(()=>{',engineering+'\nsetInterval(()=>{',1)
s=s.replace(' · 实战自评完成 ${', ' · 工程自评达标 ${Object.values(state.projects).filter(p=>new Set(p.checks).size===4).length} / 8 · 实战自评完成 ${')
s=s.replace('.tabs{display:flex;gap:6px}', '.tabs{display:flex;gap:6px;overflow-x:auto}')
s=s.replace('.sidebar{align-self:start;position:sticky;top:16px}', '.sidebar{align-self:start;position:sticky;top:16px;max-height:calc(100vh - 32px);overflow:auto}')
s=s.replace('.sidebar{position:static}', '.sidebar{position:static;max-height:none}')
path.write_text(s,encoding='utf-8')
(ROOT/'sql-pro-data.sql').write_text(data,encoding='utf-8')
(ROOT/'sql-pro-solutions.sql').write_text('USE sql_pro_lab;\n\n'+'\n\n'.join('-- '+c['title']+'\n-- '+c['task']+'\n'+c['sql'] for c in labs),encoding='utf-8')
(ROOT/'sql-pro-validation.json').write_text(js(labs),encoding='utf-8')
print(f'Added {len(new_bank)} questions, {len(labs)} labs, {len(projects)} projects.')
