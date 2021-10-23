# syncio: asyncio, without async/await

`asyncio` can look very intimidating to newcomers, because of the `async`/`await` syntax. Even
experienced programmers can get caught in the "async hell", when awaiting a single async function
propagates to the entire code base. Sometimes you wish you could call an async function just like a
regular function, whether running in an event loop or not.

`syncio` is an attempt to make both worlds, asynchronous and synchronous, play better together. By
decorating a function with `@sync`, it is automatically awaited if needed. You can still launch it
in the background with `asyncio.create_task`. Actually, it is auto-awaited only if it is the
outer-most call.

In the snippet of code below, you can see that while `wait` is an async function, it is not awaited
in the `main` function, yet this code takes full advantage of `asyncio`'s features, like tasks
running in the background. The `sync` decorator effectively stopped the viral effect of `async`.

```python
import asyncio
from syncio import sync

@sync
async def wait(s):
    await asyncio.sleep(s)
    print(f"Waited {s} second(s)")

@sync
def main():
    asyncio.create_task(wait(2))  # launched in the background
    wait(1)  # auto-awaited
    wait(1)  # auto-awaited

main()
# prints:
# Waited 1 second(s)
# Waited 2 second(s)
# Waited 1 second(s)
```
