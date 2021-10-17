# syncio: asyncio, without await

`asyncio` can look very intimidating to newcomers, because of the `async`/`await` syntax. Even
experienced programmers can get caught in the "async hell", when awaiting a single async function
propagates to the entire code base. Sometimes you wish you could call an async function just
like a regular function, whether running in an event loop or not.

`syncio` is an attempt to make both worlds, asynchronous and synchronous, play better together.
By decorating a function, be it async or not, with `@sync`, you don't have to remember if you need
to await it, you just always call it directly. This means there is not real difference anymore, any
async function is also a regular function.

```python
import asyncio
import time

import syncio
from syncio import sync


# an async function decorated with @sync
# can be called directly, without "await"
@sync
async def async_function():
    await asyncio.sleep(1)
    # or use syncio's sleep function:
    # syncio.sleep(1)
    print("async_function done")

# this looks like a regular function (no async/await)
# although async_function is async
@sync
def pure_syncio():
    async_function()
    print("pure_syncio done")

# decorating a regular function with @sync has no effect
# this reduces mental overhead: you can always use @sync
@sync
def not_async():
    time.sleep(1)
    print("not_async done")

async_function()
pure_syncio()
not_async()
```
