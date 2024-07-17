# fastapi
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from models.my_models import Data

# router
from routes.my_routes import test_router

# uvicorn
import asyncio
import uvicorn
from uvicorn import Config, Server
from asyncio.windows_events import ProactorEventLoop, SelectorEventLoop

from utils import sleep_func

import os
import sys
import httpx
import requests

sys.path.append( os.path.abspath(os.path.dirname(__file__)) )

# number of process
if os.cpu_count() == 16:
    process_cnt = 14
elif os.cpu_count() == 32:
    process_cnt = 29
else:
    process_cnt = round(os.cpu_count()*0.8)
semaphore = asyncio.Semaphore(process_cnt)

USE_SEMA = True
BLOCK_SEMA = False; BLOCK_SEMA = BLOCK_SEMA if USE_SEMA else False
USE_WORKER = False if USE_SEMA else True

# fastapi
my_app = FastAPI(docs_url=None, redoc_url=None) # No use swagger API docs

# routers
my_app.include_router(test_router)

# GET api
@my_app.post("/get")
async def get_func(request: Request):
    """
    get functions
    """
    return "Done"

# POST api
@my_app.post("/url")
async def win_func(request: Request, my_data: Data):
    print(my_data.user)
    print(my_data.code)

    if USE_SEMA:
        if BLOCK_SEMA:
            print(semaphore.locked())
            if semaphore.locked(): # True = server busy
                return JSONResponse(content={"result":"blocked"})

        # semaphore로 돌지 않을 부분
        try:
            result = await sleep_func(t=5)
        except Exception as e:
            return JSONResponse(content={"result":"fail"})

        # semaphore로 돌릴 부분
        async with semaphore:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post("http://url:8000", headers={"Content-Type":"application/json"}, data={"data":"data"})
                    response.raise_for_status()
                    print(response)
            except Exception as e:
                return JSONResponse(content={"result":"fail"})
    else:
        response = requests.post("http://url:8000", headers={"Content-Type":"application/json"}, data={"data":"data"})
        print(response)
    
    return JSONResponse(content={"result":"success"})

if __name__ == "__main__":
    """
    서버 시작 전에 실행해야할 또는 필요한 설정들
    """

    """
    # ver 1. for async using single process
    if not USE_WORKER and not USE_SEMA:
        class ProactorServer(Server):
            def run(self, sockets=None):
                loop = ProactorEventLoop()
                asyncio.set_event_loop(loop)
                asyncio.run(self.serve(sockets=sockets))

        config = Config(app=my_app, host="0.0.0.0", port=8000, reload=True, log_level="info")
        server = ProactorServer(config=config)
        server.run()
    """

    # ver 2. for multiprocessing with workers
    if USE_WORKER:
        uvicorn.run("main:my_app", host="0.0.0.0", port=8000, workers=process_cnt)

    # ver 3. for semaphore
    elif USE_SEMA:
        uvicorn.run("main:my_app", host="0.0.0.0", port=8000) # log_config="log_config.ini"