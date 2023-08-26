import inspect
from asyncio import iscoroutinefunction
from contextlib import AbstractAsyncContextManager, AsyncExitStack, asynccontextmanager
from types import FunctionType, MethodType
from typing import (
    Any,
    AsyncContextManager,
    Callable,
    Iterator,
    Protocol,
    runtime_checkable,
)

from soon.utils import Binder, FunctionWrapper


@runtime_checkable
class Middleware(AbstractAsyncContextManager, Protocol):
    ...


MiddlewareType = Callable[..., Middleware]


class UseCase(FunctionWrapper):
    __slots__ = ("__middlewares",)

    def __init__(self, function: FunctionType, /):
        if not iscoroutinefunction(function):
            raise TypeError(f"`{function.__qualname__}` isn't an async function.")

        super().__init__(function)
        self.__middlewares = set()

    async def wrapper(self, /, *args, **kwargs) -> Any:
        async with self.post_processing(*args, **kwargs) as result:
            return result

    @asynccontextmanager
    async def post_processing(self, /, *args, **kwargs) -> AsyncContextManager[Any]:
        async with AsyncExitStack() as stack:
            for middleware in self.__bound_middlewares(*args, **kwargs):
                await stack.enter_async_context(middleware)

            yield await self.function(*args, **kwargs)

    def middleware(self, wrapped: FunctionType | MiddlewareType = None) -> Any:
        def decorator(wp):
            if inspect.isfunction(wp):
                middleware = asynccontextmanager(wp)
            else:
                middleware = wp

            self.__middlewares.add(middleware)
            return middleware

        return decorator(wrapped) if wrapped else decorator

    def __bound_middlewares(self, /, *args, **kwargs) -> Iterator[Middleware]:
        arguments = inspect.signature(self).bind_partial(*args).arguments
        yield from Binder.map(self.__middlewares, **kwargs | arguments)


def use_case(function: FunctionType | MethodType = None, /) -> Any | UseCase:
    def decorator(fn):
        return UseCase(fn)

    return decorator(function) if function else decorator
