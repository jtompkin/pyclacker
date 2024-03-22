#!/usr/bin/env python3
from collections.abc import Callable
from string import digits
import argparse
import sys
from typing import Literal

try:
    from .version import __version__
except ImportError:
    __version__ = "standalone"


class Stack:
    """
    Stack with methods to push, pull, and operate. Return value of operator methods is
    boolean of whether or not the operator succesfully completed the calculation
    properties:
        `tokens`[dict]:
            Keys:
                str: String used to call to an operator method
            Values:
                tuple[Callable, int]: Operator method and number of
                arguments the method takes from the stack
    """

    def __init__(self, initial: list[float] | None = None) -> None:
        if initial is None:
            self.stack: list[float] = []
        else:
            self.stack: list[float] = initial
        self.tokens: dict[str, tuple[Callable[[], bool], int]] = {
            "+": (self._add, 2),
            "-": (self._sub, 2),
            "*": (self._mult, 2),
            "/": (self._div, 2),
            "^": (self._pow, 2),
            ".": (self._display, 0),
            ",": (self._clear, 0),
            "=": (self._nop, 0),
            "pop": (self._pop, 0),
            "words": (self._words, 0),
            "help": (self._help, 0),
        }
        self.words: dict[str, str] = {
            "sqrt": "0.5 ^",
            "pi": "3.14159265358979323846",
        }

    def parse_token(self, token: str) -> bool:
        action, nargs = self.tokens.get(token, (self._nop, 0))
        if len(self.stack) < nargs:
            return True
        return action()

    def parse_word(self, word: str) -> bool:
        for value in self.words.get(word, " ").split(" "):
            if not self.push(value):
                return False
        return True

    def push(self, value: str, display: bool = False) -> bool:
        """
        Push value to stack and optionally print or parse operator.
        Returns `False` to indicate that no more items should be pushed.
        """
        if value == "=":
            return False
        try:
            numerical_value = float(value)
            if numerical_value.is_integer():
                numerical_value = int(value)
            self.stack.append(numerical_value)
            if display:
                self._display()
            return True
        except ValueError:
            if value in self.words:
                return self.parse_word(value)
            return self.parse_token(value)

    def add_word(self, word: str, definition: str) -> bool:
        """Return `True` if succesfully added/deleted word"""
        if word in self.tokens or word in digits:
            sys.stderr.write(f"Cannot redefine: {word}\n")
            return False
        if definition == "":
            del self.words[word]
            return True
        self.words.update({word: definition})
        return True

    def _display(self) -> bool:
        print(" ".join(str(i) for i in self.stack))
        return True

    def _add(self) -> bool:
        self.stack.append(self.stack.pop() + self.stack.pop())
        self._display()
        return True

    def _sub(self) -> bool:
        x = self.stack.pop()
        y = self.stack.pop()
        self.stack.append(y - x)
        self._display()
        return True

    def _mult(self) -> bool:
        self.stack.append(self.stack.pop() * self.stack.pop())
        self._display()
        return True

    def _div(self) -> bool:
        divisor = self.stack.pop()  # Divisor
        dividend = self.stack.pop()  # Dividend
        if int(divisor) == 0:
            return self._fail("Cannot divide by 0", dividend, divisor)
        self.stack.append(dividend / divisor)
        self._display()
        return True

    def _pow(self) -> bool:
        exponent = self.stack.pop()  # Exponent
        base = self.stack.pop()  # Base
        if not float(exponent).is_integer() and base < 0:
            return self._fail("Negative number cannot be raised to decimal power", base, exponent)
        if exponent < 0 and int(base) == 0:
            return self._fail("0 cannot be raised to a negative power", base, exponent)
        self.stack.append(base**exponent)
        self._display()
        return True

    def _clear(self) -> bool:
        self.stack = []
        return True

    def _pop(self) -> bool:
        self.stack.pop()
        self._display()
        return True

    def _fail(self, message: str, *values: float, push: bool = True) -> Literal[False]:
        if push:
            for value in values:
                self.stack.append(value)
        sys.stderr.write(message + "\n")
        return False

    def _help(self) -> bool:
        token_help = {
            "+": "Pop two items from the stack, add them,\n\t\tand return the result to the stack",
            "-": "Pop two items from the stack, subtract them,\n\t\tand return the result to the stack",
            "*": "Pop two items from the stack, multiply them,\n\t\tand return the result to the stack",
            "/": "Pop two items from the stack, divide them,\n\t\tand return the result to the stack",
            "^": "Pop two items from the stack, raise the\n\t\tsecond item popped to the power of the first item popped,\n\t\tand return the result to the stack",
            ".": "Print all the items in the stack",
            ",": "Clear all the items from the stack",
            "=": "Start word definition. Next item is the word itself,\n\t\tfollowed by its definition",
            "pop": "Pop one item from the stack, does not perform any operation.",
            "words": "Print all defined words",
            "help": "Print this help message",
        }
        for token, desctiption in token_help.items():
            print(f"Operator: {token}\tDesctiption: {desctiption}")
        return True

    def _words(self) -> bool:
        for word, definition in self.words.items():
            print(f"{word}: {definition}")
        return True

    def _nop(self) -> bool:
        return True


def parse_words_file(words_file_path: str) -> Stack:
    stack = Stack()
    with open(words_file_path, "r") as words_file:
        good_adds = True
        for line in words_file:
            line_split = line.strip().split(" ")
            if not stack.add_word(line_split[0], " ".join(line_split[1:])):
                good_adds = False
        if not good_adds:
            sys.stderr.write(
                "Run `help` to see list of operators that cannot be redefined\n"
            )
    return stack


def interactive(stack: Stack) -> None:
    try:
        while True:
            input_words = input("  > ").strip().split(" ")
            for i, value in enumerate(input_words):
                if not stack.push(value, i + 1 == len(input_words)):
                    if value != "=":
                        break
                    try:
                        stack.add_word(
                            input_words[i + 1], " ".join(input_words[i + 2 :])
                        )
                        break
                    except IndexError:
                        break
    except EOFError:
        sys.stdout.write("\n")


def single_program(program: list[str], stack: Stack) -> None:
    for value in program:
        stack.push(value)


def main(arguments: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="pyclacker", description="Reverse polish notation (RPN) calculator"
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{parser.prog} {__version__}",
    )
    parser.add_argument(
        "-w",
        "--words-file",
        dest="words_file",
        help="Path to file containing word definitions. Reads from standard in if '-', which is the default if provided withouth an argument. One definition per line. First word per line is the word itself, the rest is the definition. Ex. sqrt 0.5 ^",
    )
    parser.add_argument(
        "program",
        nargs="?",
        help="Program to pass to calculator. Provide as a string with statements separated by a space. Enter interactive mode if not provided",
    )

    args = parser.parse_args(arguments)
    if args.words_file is not None:
        stack = parse_words_file(args.words_file)
    else:
        stack = Stack()
    if args.program is not None:
        single_program(args.program.split(" "), stack)
    else:
        interactive(stack)


if __name__ == "__main__":
    main()
