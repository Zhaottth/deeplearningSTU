"""Independently check fixture results in SQLite with explicit dialect adaptations.
This is a result cross-check, not a MySQL runtime validation.
"""
import runpy,sqlite3,re,datetime,calendar,json
from pathlib import Path
old_html=Path(__file__).resolve().parent.parent.joinpath('2.html').read_text(encoding='utf-8')
old_bank=json.loads(re.search(r'const BANK=(.*?);\s*const KEY=',old_html,re.S).group(1))
old_cases=json.loads(re.search(r'const CASES=(.*?);\s*function renderLab',old_html,re.S).group(1))
d=runpy.run_path(str(Path(__file__).with_name('build-2.py')))
assert old_bank==d['bank'][:len(old_bank)],'Existing question IDs/content changed'
assert old_cases==d['cases'][:len(old_cases)],'Existing case IDs/content changed'
assert len(d['bank'])==120 and len(d['cases'])==24
assert len({q['q'] for q in d['bank']})==120
def addmonths(day,n):
    x=datetime.date.fromisoformat(day);m=x.month-1+int(n);y=x.year+m//12;m=m%12+1
    return x.replace(year=y,month=m,day=min(x.day,calendar.monthrange(y,m)[1])).isoformat()
dbs={}
for name,ddl in [('coffee_training_2',d['coffee']),('ev_training_2',d['ev'])]:
    con=sqlite3.connect(':memory:');con.create_function('addmonths',2,addmonths)
    con.create_function('DATEDIFF',2,lambda a,b:(datetime.date.fromisoformat(a)-datetime.date.fromisoformat(b)).days if a and b else None)
    ddl=re.sub(r'CREATE DATABASE.*?;|USE .*?;','',ddl)
    con.executescript(ddl);dbs[name]=con
for c in d['cases']:
    sql=c['sql'].replace('COLLATE utf8mb4_bin','COLLATE BINARY').replace('/NULLIF','*1.0/NULLIF')
    sql=re.sub(r"CAST\(('.*?') AS DATE\)",r'\1',sql)
    sql=re.sub(r'DATE_ADD\(([^,]+),INTERVAL (\d+) MONTH\)',r'addmonths(\1,\2)',sql)
    got=[['NULL' if x is None else x for x in row] for row in dbs[c['db']].execute(sql)]
    assert got==c['rows'],(c['title'],got,c['rows'])
print('PASS: all 24 expected tables cross-checked using SQLite dialect adaptations; existing IDs/content unchanged; MySQL not installed.')
