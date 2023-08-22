from asyncio import get_running_loop, iscoroutinefunction
from concurrent.futures import Executor
from functools import partial, wraps
from typing import Callable


class RunInExecutor:
    __slots__ = ("__executor", "__shutdown")

    def __init__(self, executor: Executor, shutdown: bool = False):
        self.__executor = executor
        self.__shutdown = shutdown

    def __repr__(self) -> str:  # pragma: no cover
        executor_name = self.__executor.__class__.__name__
        return f"<Run in {executor_name}>"

    def __call__(self, function: Callable = None):
        def decorator(fn):
            if iscoroutinefunction(fn):
                raise ValueError("Works only with synchronous functions.")

            @wraps(fn)
            async def wrapper(*args, **kwargs):
                loop = get_running_loop()
                executable = partial(fn, *args, **kwargs)
                return await loop.run_in_executor(self.__executor, executable)

            return wrapper

        return decorator(function) if function else decorator

    def __del__(self):
        if self.__shutdown is False:
            return

        self.__executor.shutdown()
