from abc import ABC, abstractmethod


class AbstractFactory[T](ABC):
    __slots__ = ()

    @abstractmethod
    def build(self, /, *args, **kwargs) -> T:
        raise NotImplementedError
