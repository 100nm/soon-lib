from __future__ import annotations

import inspect
from abc import ABC
from asyncio import iscoroutinefunction
from contextlib import (
    AbstractAsyncContextManager,
    AbstractContextManager,
    AsyncExitStack,
    ExitStack,
    asynccontextmanager,
    contextmanager,
)
from types import FunctionType, MethodType
from typing import (
    Any,
    AsyncContextManager,
    Callable,
    ContextManager,
    Iterator,
    Protocol,
    Self,
    runtime_checkable,
)

from soon.utils import Binder, FunctionWrapper


class UseCaseBase(FunctionWrapper, ABC):
    __slots__ = ("__middlewares",)

    def __init__(self, function: FunctionType, /):
        super().__init__(function)
        self.__middlewares = set()

    def add_middleware(self, middleware: MiddlewareType) -> Self:
        self.__middlewares.add(middleware)
        return self

    def middleware(self, wrapped: MiddlewareType = None, /) -> Any | MiddlewareType:
        def decorator(wp):
            self.add_middleware(wp)
            return wp

        return decorator(wrapped) if wrapped else decorator

    def bound_middlewares(self, /, *args, **kwargs) -> Iterator[Middleware]:
        arguments = inspect.signature(self).bind_partial(*args).arguments
        yield from Binder.map(self.__middlewares, **kwargs | arguments)


class SyncUseCase(UseCaseBase):
    __slots__ = ()

    def wrapper(self, /, *args, **kwargs) -> Any:
        with self.post_processing(*args, **kwargs) as result:
            return result

    @contextmanager
    def post_processing(self, /, *args, **kwargs) -> ContextManager[Any]:
        with ExitStack() as stack:
            for middleware in self.bound_middlewares(*args, **kwargs):
                stack.enter_context(middleware)

            yield self.function(*args, **kwargs)


class AsyncUseCase(UseCaseBase):
    __slots__ = ()

    async def wrapper(self, /, *args, **kwargs) -> Any:
        async with self.post_processing(*args, **kwargs) as result:
            return result

    @asynccontextmanager
    async def post_processing(self, /, *args, **kwargs) -> AsyncContextManager[Any]:
        async with AsyncExitStack() as stack:
            for middleware in self.bound_middlewares(*args, **kwargs):
                if isinstance(middleware, AsyncMiddleware):
                    await stack.enter_async_context(middleware)
                    continue

                stack.enter_context(middleware)

            yield await self.function(*args, **kwargs)


def use_case(function: FunctionType | MethodType = None, /) -> Any | UseCase:
    def decorator(fn):
        if iscoroutinefunction(fn):
            return AsyncUseCase(fn)

        return SyncUseCase(fn)

    return decorator(function) if function else decorator


@runtime_checkable
class SyncMiddleware(AbstractContextManager, Protocol):
    ...


@runtime_checkable
class AsyncMiddleware(AbstractAsyncContextManager, Protocol):
    ...


Middleware = SyncMiddleware | AsyncMiddleware
MiddlewareType = Callable[..., Middleware]
UseCase = SyncUseCase | AsyncUseCase

del UseCaseBase
