"""Explicit, reviewable question-to-knowledge mapping. No keyword-count inflation."""
from pathlib import Path
import json,re

ROOT=Path(__file__).parent
CATALOG='''
聚合|COUNT 与 NULL 计数|1,7,10,13,29,51,56,61,64,88,116,128,201-220
聚合|SUM / AVG 与空集分母|1,7,52,58,61,118,120,201-210
聚合|DISTINCT 与组合去重|5,64,70,115
聚合|WHERE / HAVING 与逻辑阶段|2,8,65,66,69,291-300
聚合|GROUP BY 与函数依赖|9,63,78
聚合|CASE 分支与条件聚合|28,29,87,88,211-220
查询|布尔优先级与区间条件|3,62,67
查询|LIKE 通配符与转义|6,45
查询|稳定排序与 LIMIT|4,68,184,366-370
关联|连接基数与笛卡尔积|11,71,72,121,241-250
关联|外连接条件位置与保留行|12,13,60,73,80,128,221-230
关联|多个一对多预聚合与去重误区|14,54,77,122,241-250,381-385
关联|EXISTS 与半连接|76,124,127
关联|NOT IN 与三值逻辑|15,127,231-240
关联|相关子查询与比较基准|16
关联|标量子查询的零行与多行|74,75
关联|UNION / UNION ALL|17,79
关联|自连接与层级关系|18
关联|模拟完整外连接|19
关联|关系除法与全称条件|123,301-310
函数|数值舍入与截断|21,30,81
函数|字符数与字节数|22
函数|字符串拼接与 NULL|23,83
函数|子串与替换|24,82
函数|COALESCE / IFNULL / NULLIF|61,84,89,140
函数|NULL 安全相等比较|126
日期|日期格式化与跨年分组|25,86,90
日期|DATEDIFF 与自然日差|26
日期|TIMESTAMPDIFF 与完整单位|27
日期|月份加减与月底边界|57,85
日期|半开区间与小数秒|143,376,377
日期|时区与自然日口径|144
窗口|ROW_NUMBER 与 Top N 决胜|32,129,251-260
窗口|RANK / DENSE_RANK 并列档位|31,33,91,133,136,198,261-270
窗口|窗口结果的外层筛选|34,100,135,181,281-290
窗口|ROWS / RANGE 与 peers|35,93,129,271-280
窗口|PARTITION 与全局窗口分母|36,59,92,97,99
窗口|LAG / LEAD 与偏移缺值|37,95,96,281-290
窗口|NTILE 分桶|38,98
窗口|LAST_VALUE 与窗口终点|40,130
窗口|日历补齐与移动窗口|39,94,134,135
窗口|中位数与奇偶边界|180,311-320
窗口|连续活跃与分岛|131
窗口|会话切分与时间阈值|132
递归|非递归 CTE 与派生表|100,181
递归|递归终止、环与类型|177,178,183
递归|重叠区间与运行最大值|179
分析|指标粒度与去重人群|51,55,56,112,115,116,119,193
分析|加权平均与聚合比率|52,111,113,118,120,141
分析|金额快照、退款与时点|53,117,142,162
分析|留存队列与观察窗成熟|137,138
分析|漏斗事件顺序与时间窗|139
分析|缺失数据、补零与未知|114
索引|联合索引等值、范围与排序|42,101,145,361,362,363,365
索引|SARGable、表达式和隐式转换|43,44,45,107,376-380
索引|覆盖索引与回表|50,105,146,364
索引|索引成本与冗余判断|41,106,108,152,197,391,392,395
索引|OFFSET 与复合游标分页|4,68,149,366-370
计划|估计基数、统计与倾斜|46,102,103,147,373,396-398
计划|EXPLAIN ANALYZE 与 loops|47,150,371,372,374,375
计划|filesort 与排序代价|104,151
测量|基准环境、分位数和尾延迟|47,148,196,386-388,400
测量|连接池、排队与容量|389,390
测量|批处理与长事务成本|159,393,394
并发|条件 UPDATE 与业务原子性|153,154,321-325
并发|版本号乐观锁|326-330
并发|死锁图、锁顺序与重试|155,156,331-335
并发|RR / RC 快照与锁定读|157,158,336-340
并发|记录锁、间隙锁与 next-key|341-345
并发|幂等键与未知提交结果|160,346-350
并发|SKIP LOCKED、NOWAIT 与队列|351-353,355
并发|锁等待超时与事务回滚范围|354
并发|跨行不变量与写偏斜|356-360
并发|元数据锁与 DDL 阻塞|191,399
建模|DECIMAL、币种与舍入口径|30,55,161,165
建模|唯一约束、NULL 与软删除|48,163,166
建模|外键与引用完整性|20,167
建模|NOT NULL 与 CHECK|164
建模|多租户隔离与复合键|168
管道|增量水位与晚到记录|169
管道|可重跑、源版本与幂等合并|170
管道|CDC 删除与墓碑|171
管道|SCD2 与历史时间关联|172
管道|维度晚到与回补|173
质量|对账、反例与数据修复|125,174-176,194,199
JSON|JSON 缺失、null 与类型|182
安全|参数绑定与动态标识符|185
安全|最小权限与身份分离|186
运维|备份恢复与 RPO / RTO|49,109,187,188
运维|兼容迁移与回填|189
运维|复制延迟与写后读|190
运维|优化上线与故障证据|192,195,200,396,400
DDL/DML|INSERT 列映射与默认值|
DDL/DML|UPDATE 范围与旧新值验证|
DDL/DML|DELETE / TRUNCATE / DROP|
DDL/DML|DDL 隐式提交与原子 DDL|
DDL/DML|CTAS / LIKE 结构复制|20,110
事务|BEGIN / COMMIT / ROLLBACK 与自动提交|157
事务|SAVEPOINT 局部回滚|
对象|普通视图与可更新性|
对象|存储过程、函数与参数|
对象|触发器与隐藏写入|
模型|范式、候选键与更新异常|
模型|字符集、排序规则与相等性|163
JSON|JSON 路径与抽取|
JSON|JSON_TABLE 数组展开|
高级|分区裁剪与分区键|
高级|全文检索与 B-tree 区别|
高级|集合差与集合交的兼容写法|
高级|GROUP_CONCAT 与截断|
高级|窗口百分位与分布函数|
'''

def parse_ids(text):
    out=[]
    for token in filter(None,text.split(',')):
        if '-' in token:
            a,b=map(int,token.split('-'));out.extend(range(a,b+1))
        else:out.append(int(token))
    return sorted(set(out))

def read_bank():
    bank=[]
    for line in (ROOT/'2.html').read_text(encoding='utf-8').splitlines():
        if line.startswith('const BANK='):bank+=json.loads(line[len('const BANK='):-1])
        elif line.startswith('BANK.push(...'):bank+=json.loads(line[len('BANK.push(...'):-2])
    return bank

catalog=[dict(id=f'K{i+1:03}',area=a,name=n,original=parse_ids(refs)) for i,(a,n,refs) in enumerate(line.split('|') for line in CATALOG.strip().splitlines())]

if __name__=='__main__':
    bank=read_bank()
    mapped={i for k in catalog for i in k['original']}
    gaps=[k for k in catalog if len(k['original'])<3]
    print('Baseline questions: 400; current:',len(bank),'Knowledge points:',len(catalog),'Original gaps:',len(gaps),'Original absent:',sum(not k['original'] for k in catalog),'Required additions:',sum(3-len(k['original']) for k in gaps))
    print('Unmapped original question IDs:',sorted(set(range(1,401))-mapped))
    report_path=ROOT/'sql-knowledge-coverage.json'
    if report_path.exists():
        report=json.loads(report_path.read_text(encoding='utf-8'))
        points=report['points']
        assert len(points)==len(catalog)
        assert all(len(set(k['questions']))>=3 for k in points)
        assert {i for k in points for i in k['questions']}==set(range(1,len(bank)+1))
        assert all(bank[i-1].get('e','').strip() for k in points for i in k['questions'])
        print('PASS: current remaining gaps = 0; all questions mapped and explained.')
    else:
        for k in gaps:print(k['id'],k['name'],'existing=',k['original'],'need=',3-len(k['original']))
