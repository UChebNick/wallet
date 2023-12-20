from fastapi import FastAPI
from api.app import handlers
import asyncio
import uvicorn
app = FastAPI()
handler = handlers.handlers()



@app.get("/amount/send/")
async def send_handler(to_pub, from_priv, from_pub, amount):
    try:
        if to_pub == from_pub:
            return {"ok": False, "code": 400, "error": "from_pub = to_pub"}
        if type(to_pub) == str and type(from_priv) == str and type(amount) == str and type(from_pub) == str:
            return await handler.change_amount(to_pub=to_pub, from_priv=from_priv, from_pub=from_pub, amount=amount)
        else:
            return {"ok": False, "code": 400, "error": "invalid type"}
    except:
        return {"ok": False, "code": 520}


@app.get("/wallet/create/")
async def create_wallet(wallet_type: str):
    try:
        if type(wallet_type) == str:
            return await handler.create_wallet(wallet_type=wallet_type)
        else:
            return {"ok": False, "code": 400, "error": "invalid type"}
    except:
        return {"ok": False, "code": 520}


@app.get("/wallet/amount/")
async def check_wallet_amount(pub, priv):
    try:
        if type(pub) == str and type(priv):
            return await handler.check_amount(pub=pub, priv=priv)
        else:
            return {"ok": False, "code": 400, "error": "invalid type"}
    except:
        return {"ok": False, "code": 520}


@app.get("/wallet/transactions/")
async def check_transaction(priv):
    try:
        if type(priv) == str:
            return await handler.check_transaction(priv)
        else:
            return {"ok": False, "code": 400, "error": "invalid type"}
    except TabError:
        return {"ok": False, "code": 520}






if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)


