import asyncio
from time import sleep

from fastapi import FastAPI

app = FastAPI()


@app.get('/sleep/sys')
def nsys_sleep():
    sleep(1)
    return {'error': None}


@app.get('/sleep/async-sys')
async def sys_sleep():
    sleep(1)
    return {'error': None}


@app.get('/sleep/async-aio')
async def aio_sleep():
    await asyncio.sleep(1)
    return {'error': None}
