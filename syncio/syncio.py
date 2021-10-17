import asyncio
import inspect

import nest_asyncio
nest_asyncio.apply()


def sync(f):
    def wrapped(*args, **kwargs):
        res = f(*args, **kwargs)
        if inspect.isawaitable(res):
            res = asyncio.run(res)
        return res
    return wrapped

@sync
async def sleep(s):
    await asyncio.sleep(s)
