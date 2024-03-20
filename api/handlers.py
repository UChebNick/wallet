import loader, db
import math


class handlers:
    def __init__(self):
        self.d = db.db()
        self.wallets = {"0.01"}



    async def change_amount(self, to_pub: str, from_priv: str, from_pub: str, amount: str):
        priv_amount = await self.d.execute_priv(from_pub=from_pub, priv=from_priv)

        amount = int(amount)
        gaz = math.ceil(amount * loader.gaz_percent)
        priv_amount = int(priv_amount[0])
        if priv_amount > gaz + amount:
            if amount > 0:
                async def ret(to_pub: str, from_priv: str, from_pub: str, amount: int, priv_amount: int):
                    try:
                        if await self.d.update_amount(to_pub, from_priv, from_pub, priv_amount, amount, gaz):
                            pass
                        else:
                            return {"ok": False, "code": 400, "error": "invalid to_pub wallet code"}

                    except:
                        return {"ok": False, "code": 520}
                    return {"ok": True, "code": 200}
                return await ret(to_pub, from_priv, from_pub, amount, priv_amount)
            else:
                return {"ok": False, "code": 400, "error": "invalid amount"}
        else:
            return {"ok": False, "code": 400, "error": "not enough amount"}


    async def create_wallet(self, wallet_type: str):
        if wallet_type in self.wallets:
            async def create(wallet_type: str):
                try:
                    code = await self.d.create_wallet(wallet_type)
                except:
                    return {"ok": False, "code": 520}
                return {"ok": True, "code": 200, "pub": code[0], "priv": code[1]}
        else:
            return {"ok": False, "code": 400, "error": "invalid wallet"}
        return await create(wallet_type)




    async def check_amount(self, pub: str, priv: str):
        async def check(pub, priv):
            try:
                amount = await self.d.execute_priv(priv, pub)
                if amount == []:
                    return {"ok": False, "code": 400, "error": "there is no such wallet"}

            except:
                return {"ok": False, "code": 520}
            return {"ok": True, "code": 200, "amount": amount[0]}

        return await check(pub, priv)


    async def check_transaction(self, priv: str, pub: str):
        async def check():
            try:
                __list = await self.d.check_transaction(priv, pub)
            except:
                return {"ok": False, "code": 520}
            return {"ok": True, "code": 200, "transaction": __list}
        return await check()











