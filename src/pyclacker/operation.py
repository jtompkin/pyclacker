from shutil import get_terminal_size
from collections.abc import Callable
from typing import NoReturn, TextIO
from textwrap import wrap
from string import digits
import sys, os

from pyclacker import stack


class StackOperator:
    def __init__(self, initial_stack: stack.Stack | None = None) -> None:
        if initial_stack is None:
            self.stack = stack.Stack()
        else:
            self.stack = initial_stack
        self.operators: dict[str, stack.Action | MetaOperator] = {
            "+": stack.Action(2, 1, stack.add),
            "-": stack.Action(2, 1, stack.subtract),
            "*": stack.Action(2, 1, stack.multiply),
            "/": stack.Action(2, 1, stack.divide),
            "^": stack.Action(2, 1, stack.power),
            "!": stack.Action(1, 1, stack.factorial),
            "deg": stack.Action(1, 1, stack.degrees),
            "rad": stack.Action(1, 1, stack.radians),
            "sin": stack.Action(1, 1, stack.sine),
            "cos": stack.Action(1, 1, stack.cosine),
            "round": stack.Action(2, 1, stack.round_value),
            ".": stack.Action(0, 0, stack.display),
            ",": stack.Action(1, 0, stack.pop),
            "clear": stack.Action(0, 0, stack.clear),
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

    def add_word(self, definition: list[str]) -> bool:
        """
        Add `definition` to dictionary of words and return `False` if unsuccessful.

        Arguments:
        `definition` -- Includes word to define and definition. First item
        should be '='.
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
        """Parse file and return `False` if any adds were unsuccessful."""
        good_adds = True
        for line in words_file:
            line_split = line.strip().split(" ")
            if not self.add_word(["="] + line_split):
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
        operator = self.operators.get(token, stack.Action())
        if len(self.stack) < operator.pops:
            return
        if isinstance(operator, stack.Action):
            operator(self.stack)
            return
        operator(self)


class MetaOperator:
    """
    Operator that does not operate on the stack, only uses information from
    a `StackOperator` instance
    """

    def __init__(self, action: Callable[[StackOperator], None]):
        self.pops = 0
        self.pushes = 0
        self.action = action
        self.help = self._make_help()

    def _make_help(self) -> str:
        help_string = self.action.__doc__
        if help_string is None:
            return ""
        return f'"{" ".join(help_string.strip().split())}"'

    def __call__(self, value: StackOperator) -> None:
        self.action(value)


def _words(operator: StackOperator) -> None:
    """Print all defined words to the screen."""
    for word, definition in operator.words.items():
        print(f"{word}: {' '.join(definition)}")


def _help(stack: StackOperator) -> None:
    """Print information about available operators to the screen."""
    extra_space = 2
    prefix = "operator: "
    max_length = max(len(i) for i in stack.operators) + len(prefix)
    term_width = get_terminal_size()[0] - (max_length + extra_space)
    for token, operator in stack.operators.items():
        operator_help = f"{prefix}{token}"
        padding = max_length - len(operator_help) + extra_space
        sys.stdout.write(operator_help + " " * padding)
        for chunk in wrap(
            operator.help,
            term_width,
            subsequent_indent=" " * (max_length + extra_space),
        ):
            print(chunk)


def _clear(_: StackOperator) -> None:
    """Clear the terminal screen."""
    if sys.platform.startswith("win32"):
        os.system("cls")
    elif sys.platform.startswith(("linux", "darwin")):
        os.system("clear")


def _quit(_: StackOperator) -> NoReturn:
    """Exit interactive mode."""
    sys.exit(0)
