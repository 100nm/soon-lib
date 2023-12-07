from abc import ABC, abstractmethod

class AbstractFactory[T](ABC):
    @abstractmethod
    def build(self, /, *args, **kwargs) -> T: ...
