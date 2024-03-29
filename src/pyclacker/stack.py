from typing import TextIO
from string import digits
import sys

from pyclacker import interfaces, operations, actions


class Stack(interfaces.Stack):
    def __init__(self, initial: list[int | float] | None = None) -> None:
        if initial is None:
            self._values: list[int | float] = []
        else:
            self._values = initial

    @property
    def values(self) -> list[int | float]:
        return self._values

    @values.setter
    def values(self, value: list[int | float]):
        self._values = value

    def push(self, *values: int | float, display: bool = True) -> None:
        """Push each value from `values` onto stack and optionally display"""
        for value in values:
            if float(value).is_integer():
                self.values.append(int(value))
            else:
                self.values.append(value)
        if display:
            print(self)
        return

    def pop(self, index: int = -1) -> int | float:
        """Return popped value from stack"""
        return self.values.pop(index)

    def __len__(self) -> int:
        return len(self.values)

    def __repr__(self) -> str:
        return " ".join(str(i) for i in self.values)


class StackOperator(interfaces.StackOperator):
    def __init__(self, stack: Stack | None = None) -> None:
        if stack is None:
            self._stack = Stack()
        else:
            self._stack = stack
        self._operations: dict[str, interfaces.Action] = {
            "+": actions.StackAction(2, 1, operations.add),
            "-": actions.StackAction(2, 1, operations.subtract),
            "*": actions.StackAction(2, 1, operations.multiply),
            "/": actions.StackAction(2, 1, operations.divide),
            "^": actions.StackAction(2, 1, operations.power),
            "!": actions.StackAction(1, 1, operations.factorial),
            "deg": actions.StackAction(1, 1, operations.degrees),
            "rad": actions.StackAction(1, 1, operations.radians),
            "sin": actions.StackAction(1, 1, operations.sine),
            "cos": actions.StackAction(1, 1, operations.cosine),
            "round": actions.StackAction(2, 1, operations.round_value),
            ".": actions.StackAction(0, 0, operations.display),
            ",": actions.StackAction(1, 0, operations.pop),
            "clear": actions.StackAction(0, 0, operations.clear),
            "quit": actions.MetaAction(operations.quit),
            "cls": actions.MetaAction(operations.clear_screen),
            "words": actions.MetaAction(operations.words),
            "help": actions.MetaAction(operations.help),
        }
        self._words: dict[str, list[str]] = {
            "sqrt": ["0.5", "^"],
            "pi": ["3.141592653589793"],
        }
        self._parse_length: int = 0
        self._current: int = 0

    @property
    def stack(self) -> Stack:
        return self._stack

    @property
    def operations(self) -> dict[str, interfaces.Action]:
        return self._operations

    @property
    def words(self) -> dict[str, list[str]]:
        return self._words

    @property
    def parse_length(self) -> int:
        return self._parse_length

    @parse_length.setter
    def parse_length(self, value: int) -> None:
        self._parse_length = value

    @property
    def current(self) -> int:
        return self._current

    @current.setter
    def current(self, value: int) -> None:
        self._current = value

    def add_word(self, definition: list[str], echo: bool = True) -> bool:
        """
        Add `definition` to dictionary of words and return `False` if unsuccessful.

        Arguments:
        `definition` -- Includes word to define and definition. First item
        should be '='.
        `echo` -- Print result of adding word if `True`.
        """
        if len(definition) < 2:
            return True
        if len(definition) == 2:
            self.words.pop(definition[1], None)
            return True
        forbidden = list(self.operations) + list(digits) + ["="]
        if definition[1] in forbidden:
            sys.stderr.write(f"Cannot redefine: {definition[1]}\n")
            return False
        self.words.update({definition[1]: definition[2:]})
        if echo:
            print(f"defined {definition[1]}: {' '.join(definition[2:])}")
        return True

    def parse_words_file(self, words_file: TextIO) -> bool:
        """Parse file and return `False` if any adds were unsuccessful."""
        good_adds = True
        for line in words_file:
            line_split = line.strip().split(" ")
            if not self.add_word(["="] + line_split, False):
                good_adds = False
        return good_adds

    def parse_input(self, input_string: str) -> None:
        """Split `input_string` into tokens and handle each token."""
        words = input_string.strip().split(" ")
        self.parse_length = len(words)
        self.current = 0
        for token in words:
            if token == "=":
                self.add_word(words[self.current :])
                return
            self._parse_token(token)
            self.current += 1

    def _parse_token(self, token: str) -> None:
        if token in self.words:
            self._expand_word(token)
            return
        try:
            display = self.current == self.parse_length - 1
            self.stack.push(float(token), display=display)
            return
        except ValueError:
            self._execute(token)
            return

    def _expand_word(self, word: str) -> None:
        for token in self.words[word]:
            self._parse_token(token)
            self.current += 1

    def _execute(self, token: str) -> None:
        operator = self.operations.get(token, actions.StackAction())
        if len(self.stack) < operator.pops:
            return
        if isinstance(operator, actions.StackAction):
            operator(self.stack)
            return
        operator(self)
