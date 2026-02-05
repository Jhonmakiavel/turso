#!/usr/bin/env -S python3 -u

import turso
from antithesis.random import get_random
from sql_logger import log_sql

try:
    con = turso.connect("bank_test.db")
except Exception as e:
    print(f"Error connecting to database: {e}")
    exit(0)

cur = con.cursor()

# drop accounts table if it exists and create a new table
drop_accounts_sql = "DROP TABLE IF EXISTS accounts"
cur.execute(drop_accounts_sql)
log_sql(drop_accounts_sql)

create_accounts_sql = "CREATE TABLE accounts (account_id INTEGER PRIMARY KEY AUTOINCREMENT, balance REAL NOT NULL DEFAULT 0.0)"
cur.execute(create_accounts_sql)
log_sql(create_accounts_sql)

# randomly create up to 100 accounts with a balance up to 1e9
total = 0
num_accts = get_random() % 100 + 1
for i in range(num_accts):
    bal = get_random() % 1e9
    total += bal
    insert_sql = f"INSERT INTO accounts (balance) VALUES ({bal})"
    cur.execute(insert_sql)
    log_sql(insert_sql)

# drop initial_state table if it exists and create a new table
drop_init_sql = "DROP TABLE IF EXISTS initial_state"
cur.execute(drop_init_sql)
log_sql(drop_init_sql)

create_init_sql = "CREATE TABLE initial_state (num_accts INTEGER, total REAL)"
cur.execute(create_init_sql)
log_sql(create_init_sql)

# store initial state in the table
insert_init_sql = f"INSERT INTO initial_state (num_accts, total) VALUES ({num_accts}, {total})"
cur.execute(insert_init_sql)
log_sql(insert_init_sql)

con.commit()
