


import string, random, asyncpg, asyncio, general_functions, loader

import asyncpg

async def create_history_db():
    conn = await asyncpg.connect(user='postgres', password='uchebnick', database='postgres', host='127.0.0.1')

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS transactions (
        "__to" CHAR(32),
        "__from" CHAR(32),
        amount INTEGER,
        "__time" TEXT
    )
    '''

    await conn.execute(create_table_query)
    await conn.close()


import asyncpg

async def create_wallet_db():
    conn = await asyncpg.connect(user='postgres', password='uchebnick', database='postgres', host='127.0.0.1')

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS wallet (
        pub CHAR(32),
        priv CHAR(32),
        amount INTEGER
    )
    '''

    await conn.execute(create_table_query)
    await conn.close()


asyncio.run(create_wallet_db())
asyncio.run(create_history_db())



import datetime
datetime = datetime.datetime

class db:
    def __init__(self):
        self.user = 'postgres'
        self.password = 'uchebnick'
        self.host = '127.0.0.1'
        self.database = 'postgres'


    async def execute_priv(self, priv: str, from_pub: str):
        conn = await asyncpg.connect(user=self.user, password=self.password, database=self.database, host=self.host)
        amount = await conn.fetch('SELECT amount FROM wallet WHERE priv = $1 and pub = $2', priv, from_pub)
        return [row['amount'] for row in amount]

    async def execute_pub(self, pub: str):
        conn = await asyncpg.connect(user=self.user, password=self.password, database=self.database, host=self.host)
        amount = await conn.fetch('SELECT amount FROM wallet WHERE pub = $1', pub)
        return [row['amount'] for row in amount]

    async def create_wallet(self, wallet_type: str):
        conn = await asyncpg.connect(user=self.user, password=self.password, database=self.database, host=self.host)
        if wallet_type == "0.01":
            async def pub_code():
                while True:
                    pub = await general_functions.random_wallet_code()
                    priv = await general_functions.random_wallet_code()
                    print(pub)
                    amount = await self.execute_pub(pub)
                    if not amount and not await self.execute_priv(priv, pub):
                        return pub, priv

            code = await pub_code()
            await conn.execute('INSERT INTO wallet (pub, priv, amount) VALUES ($1, $2, $3)', code[0], code[1], 1000)
            return code

    async def update_amount(self, to_pub: str, priv: str, from_pub: str, priv_amount: int, amount: int, gaz: int):
        conn = await asyncpg.connect(user=self.user, password=self.password, database=self.database, host=self.host)
        to_pub_amount = await self.execute_pub(to_pub)
        if not to_pub_amount:
            return False
        now = datetime.now()
        time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        amount1 = priv_amount - gaz - amount
        await conn.execute('UPDATE wallet SET amount = $1 WHERE priv = $2 and pub = $3', amount1, priv, from_pub)
        await conn.execute('UPDATE wallet SET amount = amount + $1 WHERE pub = $2', amount, to_pub)
        await conn.execute('UPDATE wallet SET amount = amount + $1 WHERE pub = $2', gaz, loader.admin_wallet)
        await conn.execute('INSERT INTO transactions ("to", "from", amount, "__time") VALUES ($1, $2, $3, $4)', to_pub, priv, amount, time_str)
        return True

    async def check_transaction(self, priv, pub):
        conn = await asyncpg.connect(user=self.user, password=self.password, database=self.database, host=self.host)
        results = await conn.fetch('SELECT * FROM transactions WHERE "__from" = $1 OR "__to" = $2', priv, pub)
        return [[row['__to'], row['__from'],  row['amount'], row['__time']] for row in results]