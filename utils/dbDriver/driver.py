from abc import ABCMeta, abstractmethod


class IDatabaseDriver:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def get(self, query, args=None) -> list:
        raise NotImplementedError

    @abstractmethod
    def send(self, query, args=None) -> None:
        raise NotImplementedError

    @abstractmethod
    def save(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def selfCheck(self) -> None:
        raise NotImplementedError
