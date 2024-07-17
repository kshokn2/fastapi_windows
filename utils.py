import asyncio
import httpx

async def sleep_func(t):
    await asyncio.sleep(t)

    return True