from shutil import get_terminal_size
from collections.abc import Callable
from typing import NoReturn, TextIO
from textwrap import wrap
from string import digits
import sys, os

from pyclacker import stack as stk


class StackOperator:
    def __init__(self, initial_stack: stk.Stack | None = None) -> None:
        if initial_stack is None:
            self._stack = stk.Stack()
        else:
            self._stack = initial_stack
        self.operators: dict[str, stk.Action | MetaOperator] = {
            "+": stk.Action(2, 1, stk.add),
            "-": stk.Action(2, 1, stk.subtract),
            "*": stk.Action(2, 1, stk.multiply),
            "/": stk.Action(2, 1, stk.divide),
            "^": stk.Action(2, 1, stk.power),
            "!": stk.Action(1, 1, stk.factorial),
            "deg": stk.Action(1, 1, stk.degrees),
            "rad": stk.Action(1, 1, stk.radians),
            "sin": stk.Action(1, 1, stk.sine),
            "cos": stk.Action(1, 1, stk.cosine),
            "round": stk.Action(2, 1, stk.round_value),
            ".": stk.Action(0, 0, stk.display),
            ",": stk.Action(1, 0, stk.pop),
            "clear": stk.Action(0, 0, stk.clear),
            "quit": MetaOperator(_quit),
            "cls": MetaOperator(_clear),
            "words": MetaOperator(_words),
            "help": MetaOperator(_help),
        }
        self.words: dict[str, list[str]] = {
            "sqrt": ["0.5", "^"],
            "pi": ["3.141592653589793"],
        }
        self.parse_length: int = 0
        self.current: int = 0

    @property
    def stack(self) -> stk.Stack:
        return self._stack

    def add_word(self, definition: list[str]) -> bool:
        """
        Add word and definition. `definition` should include
        '=' as first item. Returns `False` if unsuccessful
        """
        if len(definition) < 2:
            return True
        if len(definition) == 2:
            self.words.pop(definition[1], None)
            return True
        forbidden = list(self.operators) + list(digits) + ["="]
        if definition[1] in forbidden:
            sys.stderr.write(f"Cannot redefine: {definition[1]}\n")
            return False
        self.words.update({definition[1]: definition[2:]})
        return True

    def parse_words_file(self, words_file: TextIO) -> bool:
        """Parse file and add words from it. Return `False` if any adds were
        unsuccessful"""
        good_adds = True
        for line in words_file:
            line_split = line.strip().split(" ")
            if not self.add_word(["="] + line_split):
                good_adds = False
        return good_adds

    def parse_input(self, input_string: str) -> None:
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
        operator = self.operators.get(token, stk.Action())
        if len(self.stack) < operator.pops:
            return
        if isinstance(operator, stk.Action):
            operator(self.stack)
            return
        operator(self)


class MetaOperator:
    """
    Operator that does not operate on the stack,
    only uses information from a `Stack` instance
    """

    def __init__(self, action: Callable[[StackOperator], None]):
        self.pops = 0
        self.pushes = 0
        self._action = action

    @property
    def action(self) -> Callable[[StackOperator], None]:
        return self._action

    def __call__(self, value: StackOperator) -> None:
        self.action(value)


def _words(operator: StackOperator) -> None:
    """Print all defined words to the screen"""
    for word, definition in operator.words.items():
        print(f"{word}: {' '.join(definition)}")


def _help(stack: StackOperator) -> None:
    """Print information about available operators to the screen"""
    extra_space = 2
    prefix = "operator: "
    max_length = max(len(i) for i in stack.operators) + len(prefix)
    term_width = get_terminal_size()[0] - (max_length + extra_space)
    for token, operator in stack.operators.items():
        operator_help = f"{prefix}{token}"
        padding = max_length - len(operator_help) + extra_space
        description_help = operator.action.__doc__
        if description_help is None:
            description_help = ""
        else:
            description_help = f'"{description_help}"'
        sys.stdout.write(operator_help + " " * padding)
        for chunk in wrap(
            description_help,
            term_width,
            subsequent_indent=" " * (max_length + extra_space),
        ):
            print(chunk)


def _clear(_: StackOperator) -> None:
    """Clear the terminal screen"""
    if sys.platform.startswith("win32"):
        os.system("cls")
    elif sys.platform.startswith(("linux", "darwin")):
        os.system("clear")


def _quit(_: StackOperator) -> NoReturn:
    """Exit interactive mode"""
    sys.exit(0)
