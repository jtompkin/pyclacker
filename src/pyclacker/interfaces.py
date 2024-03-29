from abc import ABCMeta, abstractmethod
from collections.abc import Callable
from typing import Any, TextIO


class Stack(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError()

    @property
    @abstractmethod
    def values(self) -> list[int | float]:
        raise NotImplementedError()

    @values.setter
    @abstractmethod
    def values(self, value: list[int | float]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def push(self, *values: int | float, display: bool = True) -> None:
        raise NotImplementedError()

    @abstractmethod
    def pop(self, index: int = -1) -> int | float:
        raise NotImplementedError()

    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError()


class Action(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError()

    @property
    @abstractmethod
    def pops(self) -> int:
        raise NotImplementedError()

    @property
    @abstractmethod
    def pushes(self) -> int:
        raise NotImplementedError()

    @property
    @abstractmethod
    def action(self) -> Callable[[Any], None]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def help(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def __call__(self, value: Any) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _make_help(self) -> str:
        raise NotImplementedError()


class StackOperator(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError()

    @property
    @abstractmethod
    def stack(self) -> Stack:
        raise NotImplementedError()

    @property
    @abstractmethod
    def operations(self) -> dict[str, Action]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def words(self) -> dict[str, list[str]]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def parse_length(self) -> int:
        raise NotImplementedError()

    @parse_length.setter
    @abstractmethod
    def parse_length(self, value: int) -> None:
        raise NotImplementedError()

    @property
    @abstractmethod
    def current(self) -> int:
        raise NotImplementedError()

    @current.setter
    @abstractmethod
    def current(self, value: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def add_word(self, definition: list[str]) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def parse_words_file(self, words_file: TextIO) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def parse_input(self, input_string: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _parse_token(self, token: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _expand_word(self, word: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _execute(self, token: str) -> None:
        raise NotImplementedError()
