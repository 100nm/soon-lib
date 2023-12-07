from abc import ABCMeta


class ControllerMeta(ABCMeta):
    ...


class Controller(metaclass=ControllerMeta):
    __slots__ = ()
