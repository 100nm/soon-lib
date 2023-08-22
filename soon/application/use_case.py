import inspect
from asyncio import iscoroutinefunction
from contextlib import AbstractAsyncContextManager, AsyncExitStack, asynccontextmanager
from functools import wraps
from inspect import Parameter
from types import FunctionType, MethodType, new_class
from typing import (
    Any,
    AsyncContextManager,
    Callable,
    Iterator,
    Protocol,
    Self,
    runtime_checkable,
)


@runtime_checkable
class Middleware(AbstractAsyncContextManager, Protocol):
    ...


MiddlewareType = Callable[..., Middleware]

_sentinel = new_class("Sentinel")()


class UseCase:
    __slots__ = ("__base", "__function", "__middlewares")

    def __init__(self, base_function: FunctionType):
        if not iscoroutinefunction(base_function):
            raise TypeError(f"`{base_function.__qualname__}` isn't an async function.")

        self.__base = base_function
        self.__function = None
        self.__middlewares = set()

    def __call__(self, /, *args, **kwargs) -> Any:
        return self.function(*args, **kwargs)

    def __get__(self, instance: object | None, owner: type) -> MethodType | Self:
        if instance is None:
            return self

        return self.function.__get__(instance, owner)

    @property
    def function(self) -> FunctionType:
        if self.__function is not None:
            return self.__function

        @wraps(self.__base)
        async def function(*args, **kwargs):
            async with self.post_processing(*args, **kwargs) as result:
                return result

        self.__function = function
        return function

    @asynccontextmanager
    async def post_processing(self, /, *args, **kwargs) -> AsyncContextManager[Any]:
        async with AsyncExitStack() as stack:
            for middleware in self.__bound_middlewares(*args, **kwargs):
                await stack.enter_async_context(middleware)

            yield await self.__base(*args, **kwargs)

    def middleware(self, wrapped: FunctionType | MiddlewareType = None) -> Any:
        def decorator(wp):
            if isinstance(wp, FunctionType):
                middleware = asynccontextmanager(wp)
            else:
                middleware = wp

            if not issubclass(middleware, Middleware):
                raise TypeError(f"`{middleware}` isn't a valid middleware.")

            self.__middlewares.add(middleware)
            return middleware

        return decorator(wrapped) if wrapped else decorator

    def __bound_middlewares(self, /, *args, **kwargs) -> Iterator[Middleware]:
        arguments = inspect.signature(self.__base).bind(*args, **kwargs).arguments

        for middleware in self.__middlewares:
            signature = inspect.signature(middleware)
            copy = arguments.copy()
            kw = {}

            for name, parameter in signature.parameters.items():
                if parameter.kind is Parameter.VAR_KEYWORD:
                    kw.update(copy)

                else:
                    kw[name] = copy.pop(name, _sentinel)

            yield middleware(**kw)


def use_case(function: FunctionType = None) -> Any | UseCase:
    def decorator(fn):
        return UseCase(fn)

    return decorator(function) if function else decorator
