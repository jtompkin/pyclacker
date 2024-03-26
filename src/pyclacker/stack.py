from collections.abc import Callable
from shutil import get_terminal_size
from textwrap import wrap
from string import digits
import sys, os

try:
    import pyclacker.stack_actions as sacs
except ImportError:
    import stack_actions as sacs


class Stack:
    def __init__(self, initial: list[float] | None = None) -> None:
        if initial is None:
            self.stack: list[float] = []
        else:
            self.stack = initial
        self.operators: dict[str, StackOperator | HelpOperator] = {
            "+": StackOperator(2, 1, sacs.add),
            "-": StackOperator(2, 1, sacs.subtract),
            "*": StackOperator(2, 1, sacs.multiply),
            "/": StackOperator(2, 1, sacs.divide),
            "^": StackOperator(2, 1, sacs.power),
            "!": StackOperator(1, 1, sacs.factorial),
            "deg": StackOperator(1, 1, sacs.degrees),
            "rad": StackOperator(1, 1, sacs.radians),
            "sin": StackOperator(1, 1, sacs.sine),
            "cos": StackOperator(1, 1, sacs.cosine),
            "round": StackOperator(2, 1, sacs.round_value),
            ".": StackOperator(0, 0, sacs.display),
            ",": StackOperator(1, 0, sacs.pop),
            "clear": StackOperator(0, 0, sacs.clear),
            "quit": StackOperator(0, 0, sacs.quit),
            "cls": HelpOperator(_clear),
            "words": HelpOperator(_words),
            "help": HelpOperator(_help),
        }
        self.words: dict[str, list[str]] = {
            "sqrt": ["0.5", "^"],
            "pi": ["3.141592653589793"],
        }
        self.parse_length: int = 0
        self.current: int = 0

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
            return self._expand_word(token)
        try:
            return self._push_value(float(token))
        except ValueError:
            return self._do_operator(token)

    def _expand_word(self, word: str) -> None:
        for token in self.words[word]:
            self._parse_token(token)
            self.current += 1

    def _push_value(self, value: float) -> None:
        if value.is_integer():
            self.stack.append(int(value))
        else:
            self.stack.append(value)
        if self.current == self.parse_length - 1:
            sacs.display(self.stack)

    def _do_operator(self, token: str) -> None:
        operator = self.operators.get(token, StackOperator())
        if len(self.stack) < operator.pops:
            return
        if isinstance(operator, HelpOperator):
            return operator(self)
        self.stack = operator(self.stack)


class StackOperator:
    """Operator that operates directly on the stack of a `Stack` instance"""

    def __init__(
        self,
        pops: int = 0,
        pushes: int = 0,
        action: Callable[[list[float]], list[float]] = sacs.nop,
    ) -> None:
        self.pops = pops
        self.pushes = pushes
        self.action = action

    def __call__(self, stack: list[float]) -> list[float]:
        return self.action(stack)


class HelpOperator:
    """
    Operator that does not operate on the stack,
    only uses information from a `Stack` instance
    """

    def __init__(self, action: Callable[[Stack], None]) -> None:
        self.pops = 0
        self.pushes = 0
        self.action = action

    def __call__(self, stack: Stack) -> None:
        return self.action(stack)


def _words(stack: Stack) -> None:
    """Print all defined words to the screen"""
    for word, definition in stack.words.items():
        print(f"{word}: {' '.join(definition)}")


def _help(stack: Stack) -> None:
    """Print information about available operators to the screen"""
    extra_space = 2
    prefix = "operator: "
    max_length = max(len(i) for i in stack.operators) + len(prefix)
    term_width = get_terminal_size()[0] - (max_length + extra_space)
    for operator in stack.operators:
        operator_help = f"{prefix}{operator}"
        padding = max_length - len(operator_help) + extra_space
        description_help = stack.operators[operator].action.__doc__
        if description_help is None:
            description_help = ''
        else:
            description_help = f'"{description_help}"'
        sys.stdout.write(operator_help + " " * padding)
        for chunk in wrap(
            description_help,
            term_width,
            subsequent_indent=" " * (max_length + extra_space),
        ):
            print(chunk)


def _clear(_: Stack) -> None:
    """Clear the terminal screen"""
    os.system("clear")
