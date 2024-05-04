import sqlite3
from api import loader
from datetime import datetime
from api import general_functions


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










class db:
    def __init__(self):
        self.sqlite_connection = sqlite3.connect('user.db')
        self.cur1 = self.sqlite_connection.cursor()
        self.sqlite_connection = sqlite3.connect('history.db')
        self.cur2 = self.sqlite_connection.cursor()
        self.now = datetime.now()



    async def execute_priv(self, priv: str, from_pub: str):
        sqlite_connection = sqlite3.connect('user.db')
        cur = sqlite_connection.cursor()
        cur.execute('SELECT amount FROM user_table WHERE priv = ? and pub = ?', (priv, from_pub))
        return cur.fetchall()

    async def execute_pub(self, pub: str):
        sqlite_connection = sqlite3.connect('user.db')
        cur = sqlite_connection.cursor()
        cur.execute('SELECT amount FROM user_table WHERE pub = ?', (pub,))
        return cur.fetchall()

    async def create_wallet(self, wallet_type: str):
        if wallet_type == "0.01":
            sqlite_connection = sqlite3.connect('user.db')
            cur = sqlite_connection.cursor()
            async def pub_code():
                while True:
                    pub = await general_functions.random_wallet_code()
                    priv = await general_functions.random_wallet_code()
                    print(pub)
                    print(await db.execute_pub(self, pub))
                    if await db.execute_pub(self, pub) == [] and await db.execute_priv(self, priv, pub) == []:

                        return pub, priv
                        break




            code = await pub_code()
            cur.execute('INSERT INTO user_table (pub, priv, amount) VALUES (?,?,?)', (code[0], code[1], 0))
            sqlite_connection.commit()
            cur.close()
            return code


    async def update_amount(self, to_pub: str, priv: str, from_pub: str, priv_amount:int, amount: int, gaz: int):
        if await db.execute_pub(self, to_pub) == []:
            return False
        now = datetime.now()
        a = []
        b = ""
        v = str(now.now()).split(" ")
        a += v[0].split("-")
        a += v[1].split(":")
        for i in a:
            b += f"{i}:"
        sqlite_connection = sqlite3.connect('user.db')
        cur = sqlite_connection.cursor()
        amount1 = (priv_amount - gaz - amount)
        cur.execute('UPDATE user_table SET amount = ? WHERE priv = ? and pub = ?', (amount1, priv, from_pub))
        sqlite_connection.commit()
        cur.close()
        sqlite_connection = sqlite3.connect('user.db')
        cur = sqlite_connection.cursor()
        cur.execute('UPDATE user_table SET amount = amount + ? WHERE pub = ?', (amount, to_pub))
        cur.execute('UPDATE user_table SET amount = amount + ? WHERE pub = ?', (gaz, loader.admin_wallet))
        sqlite_connection.commit()
        cur.close()
        sqlite_connection = sqlite3.connect('history.db')
        cur = sqlite_connection.cursor()
        cur.execute('INSERT INTO operations_history_table (__to, __from, amount, __time) VALUES (?,?,?,?)', (to_pub, from_pub, amount, b))
        sqlite_connection.commit()
        cur.close()
        return True


    async def check_transaction(self, pub_to, pub_from):
        sqlite_connection = sqlite3.connect('history.db')
        cur = sqlite_connection.cursor()
        cur.execute('SELECT * FROM operations_history_table WHERE __from = ? OR __to = ?', (pub_to, pub_from))
        return cur.fetchall()
