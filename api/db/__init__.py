import sqlite3


con1 = sqlite3.connect('user.db', check_same_thread=False)
cur1 = con1.cursor()
table = '''
    CREATE TABLE IF NOT EXISTS user_table (
        pub TEXT,
        priv TEXT,
        amount INTEGER
    )
    '''
cur1.executescript(table)

con2 = sqlite3.connect('history.db', check_same_thread=False)
cur2 = con2.cursor()
table1 = '''
    CREATE TABLE IF NOT EXISTS operations_history_table (
        __to TEXT,
        __from TEXT,
        amount INTEGER,
        __time TEXT
    )
    '''
cur2.executescript(table1)






