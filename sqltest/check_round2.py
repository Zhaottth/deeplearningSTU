"""Replay all 120 result fixtures independently of the content builder.
SQLite checks query results only; MySQL plans and locking must be tested in MySQL.
"""
import json, sqlite3
from pathlib import Path
rows=json.loads((Path(__file__).parent/'round2-result-fixtures.json').read_text(encoding='utf-8'))
assert len(rows)==120
for c in rows:
    db=sqlite3.connect(':memory:')
    db.executescript('CREATE TABLE t(id INT PRIMARY KEY,grp INT,v INT);CREATE TABLE parents(id INT);INSERT INTO parents VALUES(1),(2),(3);CREATE TABLE probes(x INT);INSERT INTO probes VALUES(5),(10),(20);CREATE TABLE copies(grp INT);INSERT INTO copies VALUES(1),(1),(2),(2),(2);')
    db.executemany('INSERT INTO t VALUES(?,?,?)',c['rows'])
    cur=db.execute(c['sql'])
    assert [h[0] for h in cur.description]==c['columns']
    assert [list(r) for r in cur.fetchall()]==c['expected'],(c['family'],c['fixture'])
    db.close()
print('PASS: 120 independently replayed SQLite result fixtures across 12 query families.')
