"""Append 120 executable result drills + 80 authored concurrency/performance questions.
No network or reference inputs. Stable existing IDs and storage key are preserved.
"""
import html
import json
import sqlite3
from pathlib import Path

ROOT=Path(__file__).parent
path=ROOT/'2.html'
s=path.read_text(encoding='utf-8')
assert '// SQL_ROUND_TWO' not in s, 'Already expanded'
def js(v): return json.dumps(v,ensure_ascii=False).replace('</','<\\/')
fixtures=[
 ('空表',[]),
 ('单行缺值',[(1,1,None)]),
 ('全部缺值',[(1,1,None),(2,1,None),(3,2,None)]),
 ('同组同值',[(1,1,10),(2,1,10),(3,1,20)]),
 ('缺值与不同分组',[(1,1,10),(2,1,None),(3,2,20),(4,2,20)]),
 ('零值与负数',[(1,1,0),(2,1,-10),(3,2,10),(4,3,0)]),
 ('ID 顺序不同于金额顺序',[(1,1,30),(2,1,10),(3,1,20),(4,2,40)]),
 ('多组并列',[(1,1,20),(2,1,20),(3,2,20),(4,2,20),(5,3,10)]),
 ('多个缺值与重复',[(1,1,None),(2,1,10),(3,1,10),(4,2,None),(5,2,30),(6,2,10)]),
 ('不等大小分组',[(1,1,5),(2,2,10),(3,2,15),(4,2,20),(5,2,25),(6,3,100)])
]
# All statements below use syntax common to MySQL 8.0 and SQLite's window engine.
families=[
 ('NULL 与聚合结果','SELECT COUNT(*) rows_n,COUNT(v) known_n,SUM(v) total,ROUND(AVG(v),2) mean_v FROM t;',
  'COUNT(*) 计所有行，COUNT(v) 只计非 NULL；SUM 和 AVG 忽略 NULL。没有非空值时 SUM/AVG 为 NULL，不是零。',
  ['SELECT COUNT(*) rows_n,COUNT(*) known_n,SUM(v) total,ROUND(AVG(v),2) mean_v FROM t;',
   'SELECT COUNT(*) rows_n,COUNT(v) known_n,COALESCE(SUM(v),0) total,COALESCE(ROUND(AVG(v),2),0) mean_v FROM t;',
   'SELECT COUNT(*) rows_n,COUNT(v) known_n,SUM(v) total,ROUND(SUM(v)*1.0/NULLIF(COUNT(*),0),2) mean_v FROM t;']),
 ('条件计数诊断','SELECT COUNT(CASE WHEN v>=10 THEN 1 ELSE 0 END) a,COUNT(CASE WHEN v>=10 THEN 1 END) b FROM t;',
  'a 的 CASE 在不满足条件时返回非空的 0，所以仍被 COUNT 计入；b 没有 ELSE，不满足时返回 NULL。a 是总行数，b 才是符合条件的行数。',
  ['SELECT COUNT(CASE WHEN v>=10 THEN 1 END) a,COUNT(*) b FROM t;',
   'SELECT COUNT(CASE WHEN v>=10 THEN 1 END) a,COUNT(CASE WHEN v>=10 THEN 1 END) b FROM t;']),
 ('外连接保留零匹配','SELECT p.id,COUNT(t.id) n FROM parents p LEFT JOIN t ON t.grp=p.id AND t.v>=10 GROUP BY p.id ORDER BY p.id;',
  '父表固定有 1、2、3。条件在 ON 中只限制匹配，仍保留所有父行；COUNT(t.id) 不计无匹配产生的 NULL 扩展行。',
  ['SELECT p.id,COUNT(*) n FROM parents p LEFT JOIN t ON t.grp=p.id AND t.v>=10 GROUP BY p.id ORDER BY p.id;',
   'SELECT p.id,COUNT(t.id) n FROM parents p LEFT JOIN t ON t.grp=p.id WHERE t.v>=10 GROUP BY p.id ORDER BY p.id;',
   'SELECT p.id,COUNT(t.id) n FROM parents p LEFT JOIN t ON t.grp=p.id GROUP BY p.id ORDER BY p.id;']),
 ('NOT IN 三值逻辑','SELECT x FROM probes WHERE x NOT IN (SELECT v FROM t) ORDER BY x;',
  '候选值固定是 5、10、20。子查询有 NULL 时，不相等比较可能成为 UNKNOWN，WHERE 不保留；空子查询时三个候选值全部保留。',
  ['SELECT x FROM probes WHERE NOT EXISTS (SELECT 1 FROM t WHERE t.v=probes.x) ORDER BY x;',
   'SELECT x FROM probes WHERE x IN (SELECT v FROM t) ORDER BY x;',
   'SELECT x FROM probes ORDER BY x;']),
 ('一对多连接膨胀','SELECT COUNT(*) joined_n,SUM(t.v) joined_sum FROM t JOIN copies c ON c.grp=t.grp;',
  'copies 对组 1 有两行、组 2 有三行、组 3 没有行。内连接逐对匹配；组 1 的值被加两次，组 2 被加三次，组 3 被排除。NULL 仍不进入 SUM。',
  ['SELECT COUNT(*) joined_n,SUM(v) joined_sum FROM t;',
   'SELECT COUNT(DISTINCT t.id) joined_n,SUM(DISTINCT t.v) joined_sum FROM t JOIN copies c ON c.grp=t.grp;',
   'SELECT COUNT(*) joined_n,SUM(t.v) joined_sum FROM t LEFT JOIN copies c ON c.grp=t.grp;']),
 ('Top N 与并列决胜','WITH r AS (SELECT id,grp,v,ROW_NUMBER() OVER(PARTITION BY grp ORDER BY v DESC,id) rn FROM t WHERE v IS NOT NULL) SELECT grp,id,v FROM r WHERE rn<=2 ORDER BY grp,id;',
  '先排除 NULL，再按组内 v 降序、id 升序编号，每组最多两行。最终展示按 grp,id，与选取时的金额顺序不同。并列金额也只能占两个名额。',
  ['WITH r AS (SELECT id,grp,v,DENSE_RANK() OVER(PARTITION BY grp ORDER BY v DESC) rn FROM t WHERE v IS NOT NULL) SELECT grp,id,v FROM r WHERE rn<=2 ORDER BY grp,id;',
   'WITH r AS (SELECT id,grp,v,ROW_NUMBER() OVER(ORDER BY v DESC,id) rn FROM t WHERE v IS NOT NULL) SELECT grp,id,v FROM r WHERE rn<=2 ORDER BY grp,id;',
   'SELECT grp,id,v FROM t WHERE v IS NOT NULL ORDER BY grp,id;']),
 ('排名跳号推导','SELECT id,RANK() OVER(ORDER BY v DESC) r,DENSE_RANK() OVER(ORDER BY v DESC) d FROM t WHERE v IS NOT NULL ORDER BY id;',
  '这里没有 PARTITION，所有非空值一起排名。RANK 的下一名等于前面行数加一，DENSE_RANK 则每遇到一个不同金额只增加一；展示顺序最后按 id。',
  ['SELECT id,ROW_NUMBER() OVER(ORDER BY v DESC,id) r,DENSE_RANK() OVER(ORDER BY v DESC) d FROM t WHERE v IS NOT NULL ORDER BY id;',
   'SELECT id,RANK() OVER(PARTITION BY grp ORDER BY v DESC) r,DENSE_RANK() OVER(PARTITION BY grp ORDER BY v DESC) d FROM t WHERE v IS NOT NULL ORDER BY id;']),
 ('ROWS 与 RANGE 对照','SELECT id,SUM(v) OVER(ORDER BY v,id ROWS UNBOUNDED PRECEDING) row_sum,SUM(v) OVER(ORDER BY v RANGE UNBOUNDED PRECEDING) peer_sum FROM t WHERE v IS NOT NULL ORDER BY id;',
  'row_sum 按金额和 id 逐行累计；peer_sum 的排序只有金额，当前窗口同时包含全部同额 peers，所以同额记录共享累计值。负数、零值同样按排序进入窗口。',
  ['SELECT id,SUM(v) OVER(ORDER BY id ROWS UNBOUNDED PRECEDING) row_sum,SUM(v) OVER(ORDER BY id ROWS UNBOUNDED PRECEDING) peer_sum FROM t WHERE v IS NOT NULL ORDER BY id;',
   'SELECT id,SUM(v) OVER(ORDER BY v,id ROWS UNBOUNDED PRECEDING) row_sum,SUM(v) OVER(ORDER BY v,id ROWS UNBOUNDED PRECEDING) peer_sum FROM t WHERE v IS NOT NULL ORDER BY id;']),
 ('LAG 与过滤层级','WITH w AS (SELECT id,v,LAG(v) OVER(ORDER BY id) prev FROM t) SELECT id,v,prev FROM w WHERE v>=10 ORDER BY id;',
  '先在所有行上按 id 取前一行 v，再由外层筛当前行 v>=10。前一行可以是 NULL 或小于 10；LAG 不是上一条符合外层筛选条件的记录。',
  ['SELECT id,v,LAG(v) OVER(ORDER BY id) prev FROM t WHERE v>=10 ORDER BY id;',
   'WITH w AS (SELECT id,v,LEAD(v) OVER(ORDER BY id) prev FROM t) SELECT id,v,prev FROM w WHERE v>=10 ORDER BY id;']),
 ('HAVING 与行级筛选','SELECT grp,COUNT(*) n,SUM(v) total FROM t GROUP BY grp HAVING COUNT(*)>=2 ORDER BY grp;',
  '先按 grp 分组，再保留至少两行的分组。COUNT(*) 包括 v 为 NULL 的行；如果整组都缺值，其 SUM 为 NULL。没有出现过的组不会凭空产生。',
  ['SELECT grp,COUNT(v) n,SUM(v) total FROM t GROUP BY grp HAVING COUNT(v)>=2 ORDER BY grp;',
   'SELECT grp,COUNT(*) n,SUM(v) total FROM t WHERE v>=10 GROUP BY grp HAVING COUNT(*)>=2 ORDER BY grp;',
   'SELECT grp,COUNT(*) n,SUM(v) total FROM t GROUP BY grp ORDER BY grp;']),
 ('全称条件与空集','SELECT p.id FROM parents p WHERE NOT EXISTS (SELECT 1 FROM probes x WHERE NOT EXISTS (SELECT 1 FROM t WHERE t.grp=p.id AND t.v=x.x)) ORDER BY p.id;',
  '要求父组同时包含 5、10、20 三个目标值：不存在一个目标值在该组缺席。重复购买同值不能补足缺失目标；NULL 不等于任何目标。目标集合非空，空 t 不满足。',
  ['SELECT p.id FROM parents p WHERE EXISTS (SELECT 1 FROM t WHERE t.grp=p.id AND t.v IN (5,10,20)) ORDER BY p.id;',
   'SELECT grp id FROM t GROUP BY grp HAVING COUNT(*)>=3 ORDER BY grp;',
   'SELECT p.id FROM parents p WHERE NOT EXISTS (SELECT 1 FROM t WHERE t.grp=p.id) ORDER BY p.id;']),
 ('中位数边界推导','WITH r AS (SELECT v,ROW_NUMBER() OVER(ORDER BY v,id) rn,COUNT(*) OVER() n FROM t WHERE v IS NOT NULL) SELECT AVG(v) median_v FROM r WHERE rn IN (FLOOR((n+1)/2.0),FLOOR((n+2)/2.0));',
  '先排除 NULL，按 v,id 排序。奇数个值取正中一个，偶数个值取中间两个的平均；空集整体 AVG 仍返回一行 NULL。中位数不能用所有值的均值代替。',
  ['SELECT AVG(v) median_v FROM t;', 'SELECT MAX(v) median_v FROM t;', 'SELECT MIN(v) median_v FROM t;'])
]

def display(rows):
    if not rows: return '0 行（空结果集）'
    def cell(v):
        if v is None:return 'NULL'
        if isinstance(v,float):return format(v,'.10g')
        return str(v)
    return '；'.join('('+', '.join(map(cell,r))+')' for r in rows)

new=[]
verified=[]
for fi,(family,sql,reason,wrong_sqls) in enumerate(families):
    for di,(name,rows) in enumerate(fixtures):
        # Ensure the division family includes true and false all-target cases.
        if fi==10 and di in (6,7,9):
            rows=[(1,1,5),(2,1,10),(3,1,20)]+([(4,2,5),(5,2,10),(6,2,20)] if di==7 else [(4,2,10)])
            if di==9: rows+=[(5,3,None),(6,3,5)]
        db=sqlite3.connect(':memory:')
        db.executescript('CREATE TABLE t(id INT PRIMARY KEY,grp INT,v INT);CREATE TABLE parents(id INT);INSERT INTO parents VALUES(1),(2),(3);CREATE TABLE probes(x INT);INSERT INTO probes VALUES(5),(10),(20);CREATE TABLE copies(grp INT);INSERT INTO copies VALUES(1),(1),(2),(2),(2);')
        db.executemany('INSERT INTO t VALUES(?,?,?)',rows)
        cur=db.execute(sql);cols=[c[0] for c in cur.description];expected=cur.fetchall();answer=display(expected)
        candidates=[]
        for wrong in wrong_sqls:
            v=display(db.execute(wrong).fetchall())
            if v!=answer and v not in candidates:candidates.append(v)
        # Non-equivalent concrete alternatives for edge cases where two wrong algorithms coincide.
        alternatives=[[(0,)*len(cols)],[(None,)*len(cols)],[(1,)*len(cols)],[],[(2,)*len(cols)]]
        if expected:
            altered=[list(r) for r in expected]
            altered[0][-1]=0 if altered[0][-1] is None else altered[0][-1]+1
            alternatives.insert(0,altered)
        for rows_alt in alternatives:
            v=display(rows_alt)
            if v!=answer and v not in candidates:candidates.append(v)
        assert len(candidates)>=3
        options=[answer]+candidates[:3]
        rotation=(fi+di)%4
        options=options[rotation:]+options[:rotation]
        values=display(rows)
        context='表 t(id,grp,v) 的全部数据为：'+values+'。id 为非空唯一键，v 可空。'
        if fi in (2,10):context+='parents(id) 固定包含 1、2、3。'
        if fi in (3,10):context+='probes(x) 固定包含 5、10、20。'
        if fi==4:context+='copies(grp) 的全部五行是 1、1、2、2、2。'
        prompt=f'推导 {fi+1:02d}-{di+1:02d} · {family} / {name}。'+context+'下面查询返回什么？列顺序：'+', '.join(cols)+'。'
        q=html.escape(prompt)+'<pre>'+html.escape(sql)+'</pre>'
        nonnull=[r[2] for r in rows if r[2] is not None]
        checkpoint=f'本例输入 {len(rows)} 行，其中 v 非空 {len(nonnull)} 行。'
        if fi in (6,7,11):checkpoint+='非空金额升序为 '+str(sorted(nonnull))+'。'
        explanation=html.escape(checkpoint+reason)+'<br><strong>逐行核对结果：</strong><code>'+html.escape(answer)+'</code><br>常见误区：把行数当非空值数、改变筛选层级，或忽略题干指定的排序和空集语义。只按本题 SQL 计算，不按想象中的业务意图修正它。'
        new.append(dict(topic='推导 / '+family,type='s',q=q,o=options,a=[(-rotation)%4],e=explanation,batch='reasoning'))
        verified.append(dict(family=family,fixture=name,rows=rows,sql=sql,expected=expected,columns=cols))
        db.close()
assert len(new)==120

# Each scenario has five distinct decisions about the same stated conditions.
# Text format: question | correct | distractor | distractor | distractor | explanation.
scenarios=[
('并发 / 原子更新','C01 · 最后一件库存','InnoDB；stock(sku_id PRIMARY KEY,qty)，sku=1 库存为 1。A、B 使用独立连接，事务里执行条件扣减，并按受影响行数决定是否创建订单。', '''A 执行 UPDATE stock SET qty=qty-1 WHERE sku_id=1 AND qty>=1，尚未提交；B 执行相同语句，通常怎样？|B 等待 A 持有的冲突行锁|B 立即读旧版本并也扣成功|B 必定立即死锁|B 自动跳过该行|对同一记录的更新需要互斥锁。B 可能等待，不等于发生死锁；等待还受超时等因素影响。
A 成功扣减并 COMMIT 后，B 继续执行；没有其他写入且未超时，B 的受影响行数是？|0|1|2|NULL|B 获得锁后根据可用于更新的记录检查 qty>=1；此时库存为 0，不匹配条件，不能仅凭之前看到 1 就认定成功。
若 A 扣减后 ROLLBACK，B 未超时且继续执行，受影响行数通常是？|1|0|2|无法执行条件 UPDATE|回滚恢复库存为 1，B 获得锁后能满足条件。事务回滚与提交导致的后续结果不同。
扣减影响 0 行后还创建订单并提交，哪条业务不变量被破坏？|成功订单必须有对应成功库存扣减|主键必须连续|所有 SELECT 都要加锁|事务必须只含一条 SQL|条件 UPDATE 本身无法替应用决定失败路径。应用必须检查受影响行数，并让库存与订单处于同一原子事务。
如果一张订单要扣两个 SKU，第二个 SKU 不足，正确处理是什么？|回滚整个下单事务，撤销第一个 SKU 的扣减|保留第一件扣减并返回失败|只修改客户端库存|忽略第二件库存|多行条件扣减的业务原子性依赖整个事务；失败时不能留下部分成功。按固定 SKU 顺序加锁还能降低死锁风险。'''),
('并发 / 乐观锁','C02 · 版本号竞争','账户表 account(id PRIMARY KEY,balance,version)，初始 balance=100、version=7。A、B 均读取了版本 7，更新均采用 WHERE id=1 AND version=7。', '''A 先把余额改为 80 并 version=version+1，提交后 B 用旧版本写 70，B 应如何判断？|受影响 0 行表示发生并发冲突，不能报成功|0 行表示已经成功|强制把 version 改回 7|删除账户重建|版本字段作为比较并交换条件，防止旧状态覆盖新状态；0 行也可能是记录不存在，应用可按需求进一步区分。
B 冲突后要继续扣 30，合理的重试是什么？|重新读取最新余额和版本，重新校验后再有界重试|沿用 balance=100 的计算直接写 70|把 WHERE version 条件去掉|重试直到服务器崩溃|重试的是业务操作，不是盲目重放旧的最终值。重新计算后从 80 扣 30 应得 50。
所有写路径中只有一部分会递增 version，会有什么问题？|未维护版本的写入可能绕过冲突检测|乐观锁会自动捕获所有更新|只影响排序|主键会替代版本变化|协议必须被所有相关写入路径遵守；后台脚本、修复任务也需要纳入，否则 version 无法可靠代表状态变更。
把版本号替换成秒级 updated_at 作比较，有什么风险？|同秒多次更新可能无法区分版本|时间字段无法建索引|一定出现死锁|任何时间戳都比整数可靠|时间精度不足会发生同值覆盖，且时间还可能受写入来源影响。版本号单调递增更容易明确协议。
热点账户冲突率极高时，乐观锁是否总优于锁定读？|不是；大量重试可能放大负载，应比较两种协议|是，因为不可能加锁|是，因为 SQL 更短|否，因为乐观锁不能用于数据库|乐观更新本身仍要获取写锁。高冲突下应衡量重试率、等待时间与吞吐，必要时考虑排队或缩小热点。'''),
('并发 / 死锁诊断','C03 · 两账户互锁','A、B 在显式事务中，A 已锁 account.id=1，B 已锁 account.id=2，均未提交。以下以 InnoDB 开启死锁检测为前提。', '''A 请求 id=2，随后 B 请求 id=1，形成什么？|等待图存在环，构成死锁|普通单向等待，无环|快照读自动解决|仅发生脏读|A 等 B 释放 2，B 等 A 释放 1。必须打断一个事务才可能继续，不能靠双方一直等待自行完成。
死锁检测选中 A 为牺牲者后，应用应以什么为重试单位？|A 的完整业务事务|A 最后一条失败语句且假定之前写入保留|整个数据库|所有在线请求|InnoDB 死锁牺牲者事务被回滚。重试完整业务事务，并确保幂等、有上限和退避。
是否能保证较晚开始的事务一定是牺牲者？|不能依赖这个规则|一定能|只要连接 ID 大就能|主键较小的一方必胜|牺牲者选择不是业务可依赖的先来后到协议；代码应允许任何参与方失败并正确恢复。
两个流程均改成先锁较小账户 ID，再锁较大 ID，主要效果是什么？|避免这组相反锁顺序形成的环，但不能证明全系统无死锁|取消所有行锁|取消事务隔离|保证不会等待|一致的锁顺序能消除该特定模式；其它索引、表、外键或访问路径仍可能形成新的锁环。
复盘这次死锁最有用的证据是什么？|参与事务语句、已持有/等待锁、访问索引和时间线|只看平均 CPU|只看 SQL 字符数|只看表名长短|需要还原等待图，判断索引访问与业务顺序；单句“有死锁”不足以支持优化方案。'''),
('并发 / 隔离与快照','C04 · 一致性读与当前写','InnoDB REPEATABLE READ；A START TRANSACTION 后执行普通 SELECT，首次一致性读建立快照，读到 balance=100。B 随后把余额改为 120 并提交。', '''A 再次执行同样的普通一致性 SELECT，且 A 自己没有写该行，读到什么？|100|120|NULL|必定报死锁|相同事务的普通一致性读使用已建立的读视图，因此看不到 B 后提交的版本。题目限定没有 A 自身写入。
A 改执行 SELECT ... FOR UPDATE，在没有其它冲突事务时，读取行为是？|读取并锁定当前可用记录，能读到 120|永远读取原快照的 100|不返回数据|自动结束 A 事务|锁定读与普通快照读不是同一读取规则。不要把 RR 误解为所有 SQL 永远只操作旧快照。
A 直接执行 UPDATE account SET balance=balance+10 WHERE id=1，结果应按什么计算？|按当前可更新值 120 计算为 130|强制按快照 100 算为 110|因为快照存在所以更新被禁止|自动增加两次|更新不把普通 SELECT 的旧值隐式代入。若应用写死 balance=110 则是另一种协议，可能覆盖并发变化。
如果改为 READ COMMITTED，A 每次普通 SELECT 的快照关系是什么？|每条一致性读通常获得新的读视图，可看到已提交的新变化|全事务必须使用第一份快照|允许看到任意未提交数据|取消所有写锁|RC 的普通读视图按语句变化；这不等于脏读，也不意味着写操作没有锁。
仅 START TRANSACTION 后尚未做一致性读，能断言快照就在 START 时刻建立吗？|不能；普通 RR 一般到首次一致性读才建立，显式 WITH CONSISTENT SNAPSHOT 另论|能，所有 START 都立即建立|不能，因为 RR 没有快照|只有更新才建立|区分事务开始时刻和读视图创建时刻；实验必须写清是否使用 WITH CONSISTENT SNAPSHOT。'''),
('并发 / 范围锁','C05 · 唯一查找与范围查找','InnoDB RR，t(id PRIMARY KEY,v)，已有 id=10、20、30，事务使用显式锁定读。这里只讨论题目指定访问路径，不推广为所有执行计划。', '''用完整主键等值条件锁定已存在 id=20，与范围查找相比，有什么典型特征？|可只锁匹配索引记录，不必按一般范围扫描那样锁周围间隙|必定锁整张表|从不加锁|自动锁住所有未来 ID|唯一索引完整等值命中现存行可采用记录锁；不要把非唯一条件或唯一键不存在的情形混为一谈。
SELECT ... WHERE id>=10 AND id<30 FOR UPDATE 为什么可能阻塞插入 id=15？|RR 范围锁定读可能涉及 next-key/gap 锁，保护扫描范围|因为 15 与 10 主键重复|普通 MVCC 版本一定阻塞插入|由于 ORDER BY 缺失|范围内的新记录会影响锁定查询条件，next-key 机制用于限制相关间隙插入；精确锁范围须结合计划观察。
锁定查询 WHERE id=15，当前不存在，能据此认定没有任何锁吗？|不能；不存在的键也可能涉及间隙锁|能，不存在行就绝对不加锁|只能产生表级写锁|必定创建 id=15|未命中记录不代表没有保护查找位置的锁。需要关注访问索引、隔离级别和查询类型。
两事务都持有同一间隙的 gap 锁，是否本身就必定互斥？|不是；间隙锁的主要目的在于阻止插入，彼此可兼容|是，任何锁都互斥|是，因为两事务不能访问同表|不是，因为 gap 锁只是注释|间隙锁有不同于普通记录排他锁的兼容性；不能用“都是 X 字样所以一定互斥”替代锁语义分析。
把隔离级别降到 RC，能宣称再也没有任何 gap 锁吗？|不能，外键检查和重复键检查等仍有相关例外|能，任何情况都没有|能，并且所有死锁消失|不能，因为 RC 等于串行化|RC 通常减少搜索与扫描中的间隙锁，但不是消除全部相关锁，也不是通用的死锁修复。'''),
('并发 / 幂等与未知结果','C06 · 支付重试','支付服务用 request_id 作为业务唯一键；账务落库与请求成功结果在同一事务中。客户端发起请求后网络超时。', '''仅凭网络超时能判断数据库事务失败吗？|不能，事务可能已提交但响应丢失|能，超时必然回滚|能，TCP 失败会撤销历史提交|不能，因为事务永远不会失败|客户端结果未知不同于数据库失败。应使用稳定业务键查询已提交结果，不能把超时直接当未发生。
重试同一支付时，request_id 应怎样使用？|沿用同一业务键，并校验请求载荷一致|每次重新生成新键|只取当前秒数|省略请求键提高性能|稳定键让数据库识别同一业务操作；新键会把重试变成新的独立支付。
相同 request_id 却携带不同金额，服务应怎样做？|报告载荷冲突，不把旧结果当新金额的成功|接受并覆盖旧支付|把两次金额相加|只看 request_id 返回成功而忽略金额差异|幂等语义要求同一业务请求的内容一致。保存或可核验关键载荷，避免错误复用键。
先 SELECT 确认 request_id 不存在，再 INSERT，但没有唯一约束，够不够？|不够，两个事务可能同时查无后都插入|够，SELECT 自动保留唯一性|够，只要网络延迟小|够，隔离级别不重要|检查与写入之间存在竞争窗口。唯一约束提供最终仲裁，应用需处理重复键与已存在结果。
请求记录提交成功后再在另一个事务扣余额，会留下什么风险？|请求显示成功但扣款尚未完成或失败|保证更强原子性|自动形成分布式事务|重复键会替代余额扣减|同库可原子提交的账务与成功状态应一起完成；跨系统流程需明确定义状态机与补偿，不能假装两个提交是一个。'''),
('并发 / 队列与锁超时','C07 · 工作者抢任务','InnoDB 多工作者从 tasks 中领取 ready 任务，支持的 MySQL 版本中使用 FOR UPDATE SKIP LOCKED，领取和状态修改在同一短事务。', '''SKIP LOCKED 的结果集有什么特点？|跳过当前被冲突锁阻塞的记录，可能不是完整视图|等待每一条记录直到全取到|自动获取最新全部任务|保证公平且无饥饿|跳锁适合可重试的任务队列，不适合要求完整一致视图的财务汇总。顺序与公平需要另行设计。
领取事务提交后在事务外执行外部任务，应额外设计什么？|租约、失败回收和任务执行幂等|永久持锁直到外部系统响应|只依赖连接不断开|不允许任务失败|领取成功不等于业务执行成功。工作者可能在提交后崩溃，需要可回收状态和防重复副作用。
NOWAIT 遇到冲突锁的用途是什么？|尽快返回获取锁失败，而不是等待锁释放|跳过所有数据库错误|让锁永不释放|自动重试到成功|NOWAIT 是等待策略，不改变业务正确性。应用应区分可重试锁失败与其它错误。
在默认 innodb_rollback_on_timeout=OFF 下，锁等待超时后如何处理多语句业务最稳妥？|显式回滚整个业务事务，再决定是否完整重试|假定整个事务已自动回滚并继续提交|只返回成功|关闭所有唯一约束|默认锁等待超时通常回滚当前语句而非整个事务，之前语句可能仍在事务内；应明确清理事务状态。
领取任务时只有一个大范围无选择性的索引访问，会有什么并发风险？|扫描和持锁范围可能增大，争用上升|因为有 SKIP LOCKED 所以代价恒定|只影响前端样式|任务会自动按主键平均分配|领取查询也需要合适过滤与索引；跳锁不能替代访问路径优化。测量扫描量、领取延迟与失败回收。'''),
('并发 / 跨行不变量','C08 · 两位值班医生','on_call(doctor_id PRIMARY KEY,is_on)，A、B 两位医生初始都在岗。规则：至少一人留岗；每人先普通 SELECT COUNT(*) 确认有两人，再各自把自己的行改为离岗。', '''两个事务都读到两人，各改不同的行并提交，可能怎样？|两人都离岗，违反至少一人在岗|因为改不同的行，所以业务规则一定安全|唯一主键自动阻止离岗|COUNT 自动锁住整组|不同行没有直接写写冲突，并不保证跨行谓词不变量。检查和更新需要能串行化该业务决定的协议。
只给各自那一行增加 version 字段，能可靠解决这次冲突吗？|不能；两方修改不同版本行，都可能校验成功|能，任何乐观锁都保护整个表|能，因为 COUNT 是聚合|不能，因为版本字段只能是字符串|行级版本只能检测该行变化；跨行不变量需要共享冲突点或锁定完整相关集合。
一种容易解释的串行化方案是什么？|先锁同一个排班控制行，再重新检查和修改在岗状态|各自先读旧快照再无条件写|随机睡眠后直接提交|先清空排班表|共享控制行让同一班次的修改互斥；所有改变该不变量的写路径都必须遵循协议，检查也应读到正确当前状态。
如果事务内持有控制行锁期间调用耗时外部 API，会怎样？|延长串行区间，可能显著增加等待和超时|锁会自动暂停等待|不会影响其它请求|数据库会自动把网络调用移出事务|应缩短持锁区间，将可前置的计算移出事务；跨系统结果需要明确协议，不能靠长事务包住所有网络行为。
验收这个修复，最关键的实验是什么？|双会话按固定屏障同时尝试离岗，检查最终至少一人在岗及失败路径|单线程执行一次 SELECT|只检查索引是否存在|只验证页面能点击|并发缺陷需可控交错时间线和不变量断言；单线程成功不能证明修复并发竞争。'''),
('性能 / 联合索引','P01 · 租户订单列表','查询 WHERE tenant_id=? AND status=? AND created_at>=? ORDER BY created_at,id LIMIT 20；假设 tenant_id、status 都是等值，id 唯一，InnoDB。', '''以下哪个候选最直接匹配该查询的过滤与排序顺序？|(tenant_id,status,created_at,id)|(created_at,tenant_id,status)|(amount,id)|(status,amount,tenant_id)|等值前缀之后放时间与排序决胜键，便于按范围读取有序记录。候选合理不代表对所有分布都最优，仍需计划与测量。
如果去掉 status 条件，原索引还能保证直接按 created_at 全局有序读取吗？|不能一般保证；不同 status 段内有序不等于所有段合并有序|能，索引包含时间就一定有序|能，因为 LIMIT 20|不能，因为复合索引完全不可用|中间的 status 未固定，时间顺序被不同状态分段。可能需要排序或不同索引；不可由“包含列”推出“满足排序”。
范围查询选择返回该租户 95% 的订单，是否必须强制索引？|不应仅凭规则强制，应比较扫描及回表总代价|必须，索引永远快|必须，扫描永远错误|不需要，因为 WHERE 不影响计划|高命中率、非覆盖查询可能产生大量回表，顺序扫描也可能合理。用实际基数与资源消耗判断。
把 SELECT * 改为仅返回索引覆盖的字段，可能改善什么？|减少访问聚簇记录及传输的成本|消除所有排序和锁|保证零磁盘读取|自动缩小所有已有索引|覆盖可减少额外访问，列裁剪也减少结果传输，但不代表没有 I/O、没有并发成本。
若业务最常见的是按单用户查询，却只按租户建索引，应该怎样评估？|用真实查询族和选择性评估增加或调整用户维度的索引|无条件给每列各建索引|只看表总行数|只把索引改短名称|索引应服务实际访问模式；一个租户内用户很多时，仅租户过滤可能扫描大量无关订单。还要衡量写放大。'''),
('性能 / 分页扫描量','P02 · OFFSET 与游标','按 created_at DESC,id DESC 稳定排序。计划从有序索引扫描，无其它过滤残余；每页 20 条，本题忽略缓存和额外算子成本。', '''LIMIT 100000,20 至少需要从排序流越过/取得多少条候选记录？|100020 条|20 条|100000/20 条|恒定 1 条|OFFSET 的语义要求跳过前 100000 条再返回 20 条；并不意味着只处理返回行。实际访问量可能因其它条件更高。
游标最后一条是 (时间T,ID=500)，降序下一页谓词是什么？|created_at<T OR (created_at=T AND id<500)|created_at>T OR id>500|created_at<=T，不比较 ID|id<>500|复合字典序比较必须与排序方向一致。只比较时间会漏掉同秒其它记录，使用 <= 还可能重复上一页。
游标分页是否天然提供跨请求固定快照？|不是；并发更新排序键或删除仍可影响翻页|是，游标等于事务快照|是，因为主键唯一|不是，因为游标不能用于 SQL|游标定位与快照一致性是不同概念；若需稳定导出，应固定范围、版本或使用适当快照策略。
要求直接跳到第 5000 页且没有任何游标缓存，游标方案的局限是什么？|不能凭页码直接知道该页起始排序键|会自动生成所有游标|只要 LIMIT 就知道位置|可以不用排序|随机跳页与顺序翻页需求不同。可考虑分页锚点、限制深页或改变产品交互，而非宣称游标万能。
相比 OFFSET，评估游标优化最关键的证据是什么？|结果边界正确且实际扫描量/延迟随深度的变化改善|SQL 字符更少|用了 OR 就更快|索引名包含 cursor|同样排序、同样业务范围下比较扫描与耗时，还要测试并列时间，避免以漏数据换速度。'''),
('性能 / 执行计划推理','P03 · 嵌套循环放大','某 SELECT 的实测计划显示外层输出 10000 行，内层节点每次循环平均检查 40 行，共循环 10000 次。以下数字仅指该节点，不含其它工作。', '''内层累计检查的记录量约是多少？|400000|40000|10040|40|每次平均 40 行乘以 10000 次循环得到 40 万；不要只看单次 rows 忽略 loops。
优化后内层每次只查 1 行，外层仍 10000 行，内层记录量降为？|10000|1|100|400000|访问次数仍然一万，只是每次范围缩小。不能把每次一行误报为整个查询只有一次访问。
优化器预估外层 10 行，实际 10000 行，这提示什么？|需要检查选择性估计、统计信息及数据倾斜|已经证明数据库有语法错误|必须删除所有索引|必定是客户端显示问题|低估外层基数可能使重复内层访问的成本被严重低估；先检查谓词分布与统计信息是否反映实际情况。
把各节点显示耗时全部相加当成总耗时，有什么风险？|节点可能包含子节点时间，直接相加会重复计算|总耗时永远等于节点时间之和|所有时间单位都是字节|节点时间没有任何价值|执行计划计时有包含关系与不同统计口径，需按工具语义解读；总体耗时以根节点及实际测量为对照。
若真正瓶颈是外层产生太多无用行，除了优化内层索引，还应考虑什么？|尽早减少语义允许过滤的外层行，或改变连接/预聚合方案|把列名改短|增加无关索引|强制所有连接为笛卡尔积|优化访问次数与优化单次访问都重要。任何过滤下推或预聚合必须保留外连接、重复与分组的原始语义。'''),
('性能 / 可搜索谓词','P04 · 日期与表达式','orders(created_at DATETIME,amount DECIMAL)，created_at 上有普通 B-tree 索引。业务查某个自然日，所有时间已统一到同一业务时区。', '''哪种写法最便于普通 created_at 索引直接做日范围查找？|created_at>='2025-03-01' AND created_at<'2025-03-02'|DATE(created_at)='2025-03-01'|YEAR(created_at)=2025|CAST(created_at AS CHAR) LIKE '%03-01%'|对原始列使用半开范围可以表达完整日期边界；对列包函数的写法不应直接假设仍是相同的普通索引范围访问。
上界写成 <= '2025-03-01 23:59:59'，当列支持微秒时有什么漏洞？|漏掉该秒之后到次日零点前的小数秒记录|多包含第二天全部记录|只会重复主键|索引会自动补足遗漏|23:59:59.500000 晚于给定上界但仍属当天。次日零点的排他上界更稳健。
必须按表达式筛选时，除了改写为原列范围，还有什么可评估？|适配版本的函数索引或生成列索引，并确认表达式匹配|禁止所有函数|给任意无关列建索引|强制删掉 WHERE|表达式索引有版本、类型与表达式匹配限制，且增加维护成本；需用计划确认实际访问方式。
字符串业务编号列与数值参数比较，隐式转换需要关注什么？|可能影响比较语义及索引访问，应使用匹配类型的参数|一定更快|自动保留所有前导零语义|必定报语法错|隐式转换可能改变例如前导零的相等判断，也可能影响索引范围；参数类型应与业务字段定义一致。
看到 WHERE 中有函数，就说整个查询所有索引失效，是否准确？|不准确，其它条件或表达式索引仍可能提供访问路径|准确，任何函数都会禁用全表索引|准确，SELECT 函数也会禁用索引|不准确，因为函数总能用普通索引|需分别分析访问谓词、残余过滤和排序条件；不要用单一语法特征替代执行计划。'''),
('性能 / 预聚合与扇出','P05 · 报表越连越慢','一个客户有 100 张订单和 20 张优惠券。按 customer_id 把两个子表同时连接，再按客户汇总订单金额；假设两表记录均匹配。', '''聚合前该客户产生多少行？|2000|120|100|20|两个独立一对多关系相乘，100×20=2000。执行更慢与金额重复来自同一连接基数问题。
订单金额直接 SUM 后会出现什么？|每笔订单金额被加 20 次|金额正确只是慢|每笔被加 100 次|订单金额自动被去重|同一订单与该客户的 20 张券分别组合，因此重复 20 次；先修复语义再谈性能。
只需要订单收入与券数量，优先评估哪种改写？|两个子表分别按客户聚合，再连接客户级结果|SUM(DISTINCT 订单金额) 作为通用修复|对最终金额 LIMIT 1|把金额转换字符串|两边先压缩到每客户一行，避免交叉放大；同额不同订单应保留，所以 SUM DISTINCT 不可靠。
先聚合方案在哪种变化下需要重新设计？|指标要求只统计与某张券有直接关联的特定订单|只是客户名字改了|表名改短|SQL 增加注释|预聚合必须保留后续需要的关联粒度。若订单与券存在逐笔关系，粗化到客户级可能丢掉语义。
验证这次性能改写最应包含什么样例？|零订单、零券、重复金额及多订单多券客户|仅一单一券客户|仅随机用户名|仅空字符串字段|简单一对一数据不会暴露扇出与外连接丢行；先逐行对账，再在大数据下比较中间行数和耗时。'''),
('性能 / 测量与容量','P06 · 延迟分布和容量','对同一查询、同一数据快照进行 100 次测量：99 次为 10ms，1 次为 1010ms。分位数在本题采用最近秩法：第 ceil(p*n) 个有序样本。', '''平均耗时是多少？|20ms|10ms|1010ms|100ms|(99×10+1010)/100=20ms。少数慢请求会拉高均值，但均值仍掩盖极端慢请求的严重程度。
按题目给定最近秩法，p99 是多少？|10ms|20ms|1010ms|500ms|第 ceil(0.99×100)=99 个有序样本仍为 10ms，第 100 个才是 1010ms。报告分位数必须说明定义与样本量。
为什么不能只报 p99=10ms 就宣布没有尾部问题？|本样本存在一次 1010ms，p99 未覆盖最慢的那一个样本|因为 p99 不允许使用|因为均值永远等于最大值|因为只要有索引就没有尾延迟|应同时报告样本数、最大值、错误率和负载，扩大样本并调查异常来源，而不是选择有利指标。
系统稳定平均每秒完成 200 个请求，平均每个请求在系统停留 0.05 秒，按 Little 定律平均在途请求数约为？|10|4000|0.00025|200|在稳定系统且边界口径一致时 L=λW=200×0.05=10。它不是建议连接池必须设置为 10，还需考虑等待和峰值。
把连接池从 50 加到 500 后延迟反而上升，合理解释是什么？|更多并发可能增加资源竞争与排队，吞吐不会无限线性增长|连接池越大越不可能变慢|数据库会把多余请求自动免费完成|这只能是图表错误|需测量 CPU、I/O、锁等待和并发上限；连接数是控制负载的手段，不是越多越快。'''),
('性能 / 写放大与批处理','P07 · 写入代价','InnoDB 订单表写入频繁，已有主键和多个二级索引，准备给报表新增索引并提高批量导入速度。', '''新增一个较宽二级索引最直接增加哪些成本？|索引空间、缓存占用和相关写入维护|只增加 SELECT 字符数|会自动减少全部日志量|没有成本，索引是虚拟注释|每次相关插入或更新需要维护索引结构，增加 I/O 与日志等工作；读优化必须连同写负载评估。
为什么较宽主键可能放大 InnoDB 二级索引成本？|二级索引记录包含主键值用于定位聚簇记录|二级索引只保存整张表副本|主键永远不存数据|宽主键会禁止索引|主键宽度会传播到二级索引记录，影响空间与缓存。选择主键还需综合唯一性、稳定性和插入分布。
批量导入从每行一次提交改成每 1000 行一事务，主要可能节省什么？|每行提交的固定开销，但事务尺寸和失败范围会变大|所有行级写入工作|所有唯一键检查|任何索引更新|批量提交可摊薄提交开销，但大事务占用资源更久。批大小需通过吞吐、延迟和回滚成本测量。
一百万行全部放在单个事务，是否一定最快且最可靠？|不是，长事务、日志压力和回滚代价可能恶化|是，提交次数越少必定最好|是，事务没有大小影响|不是，因为 SQL 不能批量写|需要在原子性需求、资源预算、恢复能力之间取舍，采用可重启批次并验证幂等性。
删除疑似冗余索引前，最关键的是？|检查查询与约束依赖，并在代表性负载下验证退化与回退|仅看两个索引的首列相同|直接删除所有慢查询没出现的索引|只看索引名字相似|前缀相似不代表覆盖、排序、唯一性与访问成本都相同。低频关键查询也可能依赖该索引。'''),
('性能 / 计划与生产排障','P08 · 同一 SQL 突然变慢','某报表之前很快，今天同一 SQL 延迟上升。数据持续增长，存在倾斜租户，同时有长事务和部署变更。', '''第一步更应收集什么？|实际参数、慢的时间范围、等待类型与计划变化|立即强制某个索引|立即重启所有实例|把 SELECT 改成小写|同一 SQL 模板的不同参数可能命中完全不同数据量。先区分锁等待、CPU、I/O、计划变化和客户端传输。
对小租户测试很快就推出大租户也快，错在哪里？|忽略参数选择性和数据倾斜|因为租户字段不能查询|因为小表不支持索引|因为所有租户本应同样大|代表性参数应包含热点与极端分布；均匀随机数据不足以模拟真实热点。
更新统计信息后就必定能修复所有计划问题吗？|不能，分布相关性、成本模型和访问路径限制仍可能存在|能，统计信息等于最优计划证明|能，索引无需再考虑|不能，因为统计信息永不影响优化器|统计信息是诊断和改进手段，不是万能修复；更新后仍应比较计划、实际行数和整体性能。
长事务持有表的元数据锁，新 DDL 等待，为什么正常请求也可能受影响？|元数据锁等待队列可能使后续相关访问排队，应检查阻塞链|DDL 等待绝不会影响其他连接|因为所有表都被删除|只有管理员能执行 SELECT|需要检查持锁事务和等待链，区分元数据锁与普通行锁。不要只盯着慢 SELECT 自身的执行计划。
优化上线验收哪一组最完整？|结果等价、代表性参数延迟/资源对照、写入影响及回退条件|只验证 SQL 不报错|只验证用了新索引|只展示最快一次结果|优化是可测量的行为改变，既要守住正确性，也要覆盖真实负载与失败回退；避免把偶然缓存命中当成稳定收益。''')
]

for topic,title,context,lines in scenarios:
    entries=lines.splitlines()
    assert len(entries)==5,(title,len(entries))
    for i,line in enumerate(entries):
        stem,correct,w1,w2,w3,explain=line.split('|')
        opts=[correct,w1,w2,w3];rotate=(len(new)*7+1)%4
        opts=opts[rotate:]+opts[:rotate]
        new.append(dict(topic=topic,type='s',q=html.escape(f'{title} · 问题 {i+1}。{context} {stem}'),o=opts,a=[(-rotate)%4],
                        e=html.escape(explain)+'<br><strong>复盘要求：</strong>'+html.escape('把题目中的事务开始、SQL、等待、提交/回滚按顺序写出，再解释改变其中一步会怎样。' if topic.startswith('并发') else '列出输入规模、访问路径和需要测量的指标；说明结论依赖哪些条件，不能把候选优化当成无条件保证。'),batch='concurrency' if topic.startswith('并发') else 'performance'))
assert len(new)==200
assert len([q for q in new if q['batch']=='concurrency'])==40
assert len([q for q in new if q['batch']=='performance'])==40
assert all(len(set(q['o']))==4 and len(q['e'])>60 for q in new)
s=s.replace("const KEY=",'// SQL_ROUND_TWO\nBANK.push(...'+js(new)+');\nconst KEY=',1)
s=s.replace('200 道','400 道').replace('200 题 / 48','400 题 / 48')
s=s.replace('<option value="new">专业拓展 80 题</option>', '<option value="latest">本轮新增 200 题</option><option value="reasoning">结果推导 120 题</option><option value="systems">并发与性能 80 题</option><option value="concurrency">并发专题 40 题</option><option value="performance">性能专题 40 题</option><option value="new">上一轮拓展 80 题</option>')
s=s.replace("filter==='new'&&q.id>=120", "filter==='new'&&q.id>=120&&q.id<200||filter==='latest'&&q.id>=200||filter==='reasoning'&&q.batch==='reasoning'||filter==='systems'&&['concurrency','performance'].includes(q.batch)||filter==='concurrency'&&q.batch==='concurrency'||filter==='performance'&&q.batch==='performance'")
s=s.replace("${q.id>=120?'<span class=\"chip\">新增</span>':''}","${q.id>=200?'<span class=\"chip\">本轮新增</span>':q.id>=120?'<span class=\"chip\">专业拓展</span>':''}")
s=s.replace('新增专业题从 #121 开始；实战从 #25 开始。','本轮 #201–320 为结果推导，#321–360 为并发，#361–400 为性能。每题提交后可见讲解；实战拓展从 #25 开始。')
s=s.replace('已有基础可直接筛选“专业拓展 80 题”。','新增训练：#201–320 是 12 类查询 × 10 组边界数据，覆盖空表、NULL、并列和不等大小分组；#321–360 是 8 组并发情境 × 5 个问题；#361–400 是 8 组性能情境 × 5 个问题。每题均有推导或讲解。已有基础可直接筛选“本轮新增 200 题”。')
s=s.replace('400 道专项题 + 48 道 SQL 实战 + 8 个工程挑战。','400 道专项题 + 48 道 SQL 实战 + 8 个工程挑战。本轮新增 120 道结果推导 + 80 道并发与性能，逐题讲解。')
path.write_text(s,encoding='utf-8')
(ROOT/'round2-result-fixtures.json').write_text(js(verified),encoding='utf-8')
print('Added 120 result drills + 40 concurrency + 40 performance = 200 questions. Total 400.')
print('All 120 result answers executed against explicit SQLite fixtures; no MySQL server validation claimed.')
