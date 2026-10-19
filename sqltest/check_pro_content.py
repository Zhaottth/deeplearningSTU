"""Cross-check authored expected rows with SQLite after explicit dialect adaptations.
This is a fixture/result check, not a MySQL execution or optimizer test.
"""
import json, sqlite3, re
from pathlib import Path
p=Path(__file__).parent
db=sqlite3.connect(':memory:')
db.create_function('CONCAT',-1,lambda *a: ''.join(map(str,a)))
db.create_function('FIND_IN_SET',2,lambda a,b: int(str(a) in b.split(',')))
ddl=(p/'sql-pro-data.sql').read_text(encoding='utf-8')
ddl=re.sub(r'CREATE DATABASE.*?;|USE sql_pro_lab;', '', ddl)
ddl=re.sub(r'DECIMAL\(12,2\)', 'REAL', ddl)
db.executescript(ddl)
cases=json.loads((p/'sql-pro-validation.json').read_text(encoding='utf-8'))
for c in cases:
    q=c['sql'].replace('100*','100.0*')
    q=q.replace("DATE_FORMAT(t,'%Y-%m')", "strftime('%Y-%m',t)")
    q=q.replace('d+INTERVAL 1 DAY',"DATE(d,'+1 day')")
    q=q.replace('DATE_SUB(dt,INTERVAL rn DAY)', "DATE(dt,'-' || rn || ' day')")
    for a,n,unit in [('prev',30,'MINUTE'),('u.signup_date',1,'DAY'),('u.signup_date',2,'DAY'),('v.event_at',1,'HOUR'),('f.paid_at',7,'DAY')]:
        func='DATE' if a=='u.signup_date' else 'DATETIME'
        q=q.replace(f'{a}+INTERVAL {n} {unit}',f"{func}({a},'+{n} {unit.lower()}')")
    got=[list(r) for r in db.execute(q)]
    assert got==c['rows'], (c['title'],got,c['rows'])
    print('PASS', c['title'])
# Prove empty-result quality checks detect intentionally bad fixtures.
db.execute('UPDATE items SET unit_price=61 WHERE order_id=101 AND sku=\'A\'')
assert list(db.execute(cases[19]['sql']))==[(101,100.0,101.0)]
db.execute("INSERT INTO refunds VALUES (4,103,'2025-02-02',1)")
assert list(db.execute(cases[21]['sql']))==[(103,200.0,201.0)]
print('PASS: 24 expected result sets and 2 negative fixtures (adapted SQLite).')
