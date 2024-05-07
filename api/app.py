from fastapi import FastAPI, Depends
import handlers
from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware

import uvicorn

app = FastAPI()
handler = handlers.handlers()





@app.get("/amount/send/")
async def send_handler(request: Request, to_pub, from_priv, from_pub, amount):

    try:
        if to_pub == from_pub:
            return JSONResponse({"ok": False, "code": 400, "error": "from_pub = to_pub"}, status_code=400)
        if type(to_pub) == str and type(from_priv) == str and type(amount) == str and type(from_pub) == str:
            return JSONResponse(await handler.change_amount(to_pub=to_pub, from_priv=from_priv, from_pub=from_pub, amount=amount))
        else:
            return JSONResponse({"ok": False, "code": 415, "error": "invalid type"}, status_code=415)
    except:
        return JSONResponse({"ok": False, "code": 520}, status_code=520)


@app.get("/wallet/create/")
async def create_wallet(request: Request, wallet_type: str):
    try:
        if type(wallet_type) == str:
            j = await handler.create_wallet(wallet_type=wallet_type)
            return JSONResponse(j, status_code=j['code'])
        else:
            return JSONResponse({"ok": False, "code": 415, "error": "invalid type"}, status_code=415)
    except:
        return JSONResponse({"ok": False, "code": 520}, status_code=520)


@app.get("/wallet/amount/")
async def check_wallet_amount(request: Request, pub, priv):
    try:
        if type(pub) == str and type(priv):
            j = await handler.check_amount(pub=pub, priv=priv)
            return JSONResponse(j, status_code=j['code'])
        else:
            return JSONResponse({"ok": False, "code": 415, "error": "invalid type"}, status_code=415)
    except :
        return JSONResponse({"ok": False, "code": 520}, status_code=520)


@app.get("/wallet/transactions/")
async def check_transaction(request: Request, pub_to, pub_from):
    try:
        if type(pub_to) == str:
            j = await handler.check_transaction(pub_to, pub_from)
            return JSONResponse(j, status_code=j['code'])
        else:
            return JSONResponse({"ok": False, "code": 415, "error": "invalid type"}, status_code=415)
    except TabError:
        return JSONResponse({"ok": False, "code": 520}, status_code=520)



@app.get("/wallet/transactions/admin/check")
def check_admin(request: Request):
    return FileResponse(path="user.db")








if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)


