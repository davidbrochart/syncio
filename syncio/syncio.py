import asyncio
import inspect
import ast
import contextvars
from inspect import getsource

in_event_loop_var = contextvars.ContextVar("in_event_loop")
in_event_loop_var.set(False)

class AutoAwaiter(ast.NodeTransformer):
    def visit_Call(self, node):
        new_node = ast.IfExp(
            test=ast.Call(
                func=ast.Name(id='hasattr', ctx=ast.Load()),
                args=[
                    node.func,
                    ast.Constant(value='is_sync')],
                keywords=[]),
            body=ast.Await(
                value=node),
            orelse=node)
        return new_node

def sync(f):
    code = "\n".join(getsource(f).splitlines()[1:])
    tree = ast.parse(code)
    auto_awaiter = AutoAwaiter()
    tree = auto_awaiter.visit(tree)
    fdef = tree.body[0]
    if not inspect.iscoroutinefunction(f):
        tree.body[0] = ast.AsyncFunctionDef(name=fdef.name, args=fdef.args, body=fdef.body, decorator_list=fdef.decorator_list)
    ast.fix_missing_locations(tree)
    bytecode = compile(tree, filename="<string>", mode="exec")
    frame = inspect.currentframe()
    out_locals = frame.f_back.f_locals
    out_globals = frame.f_back.f_globals
    exec(bytecode, out_globals, out_locals)
    f = out_locals[fdef.name]

    def wrapper(*args, **kwargs):
        r = f(*args, **kwargs)
        if in_event_loop_var.get():
            return r
        else:
            in_event_loop_var.set(True)
            return asyncio.run(r)

    wrapper.is_sync = None

    return wrapper

@sync
async def sleep(s):
    await asyncio.sleep(s)
