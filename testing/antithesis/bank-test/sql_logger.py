import fcntl
import os
import sys

_DRIVER = (
    os.path.basename(sys.argv[0])
    .replace("parallel_driver_", "")
    .replace("first_setup", "setup")
    .replace(".py", "")
)
_PID = os.getpid()
_LOG_PATH = "bank_test.sql"


def log_sql(sql, result="OK"):
    sql = sql.strip().rstrip(";") + ";"
    line = f"{sql} -- [{_DRIVER}:{_PID}] {result}\n"
    with open(_LOG_PATH, "a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(line)
