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

length = cur.execute("SELECT num_accts FROM initial_state").fetchone()[0]


def transaction():
    # check that sender and recipient are different
    sender = get_random() % length + 1
    recipient = get_random() % length + 1
    if sender != recipient:
        # get a random value to transfer between accounts
        value = get_random() % 1e9

        print(f"Sender ID: {sender} | Recipient ID: {recipient} | Txn Val: {value}")

        begin_sql = "BEGIN TRANSACTION"
        cur.execute(begin_sql)
        log_sql(begin_sql)

        # subtract value from balance of the sender account
        update_sender_sql = f"UPDATE accounts SET balance = balance - {value} WHERE account_id = {sender}"
        cur.execute(update_sender_sql)
        log_sql(update_sender_sql)

        # add value to balance of the recipient account
        update_recipient_sql = f"UPDATE accounts SET balance = balance + {value} WHERE account_id = {recipient}"
        cur.execute(update_recipient_sql)
        log_sql(update_recipient_sql)

        commit_sql = "COMMIT"
        cur.execute(commit_sql)
        log_sql(commit_sql)


# run up to 100 transactions
iterations = get_random() % 100
for i in range(iterations):
    transaction()
