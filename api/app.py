from fastapi import FastAPI, Depends
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import handlers
from fastapi import FastAPI, Request, Response
from slowapi.errors import RateLimitExceeded
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as redis
from contextlib import asynccontextmanager
import asyncio
import aioredis
import uvicorn

limiter = Limiter(key_func=get_remote_address)
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
            if type(j) == dict:
                return JSONResponse(j, status_code=j['code'])
            else:
                return JSONResponse(j)
        else:
            return JSONResponse({"ok": False, "code": 415, "error": "invalid type"}, status_code=415)
    except:
        return JSONResponse({"ok": False, "code": 520}, status_code=520)


@app.get("/wallet/amount/")
@limiter.limit("10/second")
async def check_wallet_amount(request: Request, pub, priv):
    try:
        if type(pub) == str and type(priv):
            j = await handler.check_amount(pub=pub, priv=priv)
            return JSONResponse(j, status_code=j['code'])
        else:
            return JSONResponse({"ok": False, "code": 415, "error": "invalid type"}, status_code=415)
    except:
        return JSONResponse({"ok": False, "code": 520}, status_code=520)


@app.get("/wallet/transactions/")
@limiter.limit("10/second")
async def check_transaction(request: Request, priv, pub):
    try:
        if type(priv) == str:
            j = await handler.check_transaction(priv, pub)
            return JSONResponse(j, status_code=j['code'])
        else:
            return JSONResponse({"ok": False, "code": 415, "error": "invalid type"}, status_code=415)
    except:
        return JSONResponse({"ok": False, "code": 520}, status_code=520)



@app.get("/wallet/transactions/admin/check")
@limiter.limit("10/minute")
def check_admin(request: Request):
    return FileResponse(path="user.db")







if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

