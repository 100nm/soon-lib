from functools import partial
from inspect import Parameter, signature
from types import new_class
from typing import Callable, Generic, Iterable, Iterator, Mapping, TypeVar

T = TypeVar("T")

_sentinel = new_class("Sentinel")()


class Binder(Generic[T]):
    __slots__ = ("__callable", "__parameters")

    def __init__(self, callable_base: Callable[..., T], /):
        self.__callable = callable_base
        self.__parameters = None

    @property
    def parameters(self) -> Mapping[str, Parameter]:
        if self.__parameters is None:
            self.__parameters = signature(self.__callable).parameters

        return self.__parameters

    def bind(self, /, **arguments) -> partial | Callable[[], T]:
        args = []
        kwargs = {}

        for name, parameter in self.parameters.items():
            if (kind := parameter.kind) is Parameter.VAR_KEYWORD:
                kwargs.update(arguments)
                break

            try:
                value = arguments.pop(name)
            except KeyError:
                value = (
                    _sentinel
                    if (default := parameter.default) is Parameter.empty
                    else default
                )
            else:
                if kind is Parameter.VAR_POSITIONAL:
                    args.extend(value)
                    continue

            if kind is Parameter.POSITIONAL_ONLY:
                args.append(value)
            else:
                kwargs[name] = value

        return partial(self.__callable, *args, **kwargs)

    @classmethod
    def map(cls, callables: Iterable[Callable[..., T]], /, **arguments) -> Iterator[T]:
        for _callable in callables:
            yield cls(_callable).bind(**arguments)()
