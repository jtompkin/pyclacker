#!/usr/bin/env python3
from collections.abc import Callable
from typing import NoReturn
import argparse
import sys

try:
    from .version import __version__
except ImportError:
    __version__ = "standalone"


class Stack:
    """
    Simple implementation of a stack. Return value of operator methods is
    boolean of whether or not to display the stack after the operation completes
    properties:
        `tokens`[dict]:
            Keys:
                str: String representing a call to an operator method
            Values:
                tuple[Callable, int]: Operator method and number of
                arguments the method takes from the stack
    """

    def __init__(self, initial: list[float] | None = None) -> None:
        if initial is None:
            self.stack: list[float] = []
        else:
            self.stack: list[float] = []
        self.tokens: dict[str, tuple[Callable[[], bool], int]] = {
            "+": (self._add, 2),
            "-": (self._sub, 2),
            "*": (self._mult, 2),
            "/": (self._div, 2),
            "^": (self._pow, 2),
            ".": (self._display, 0),
            ",": (self._clear, 0),
            "help": (self._help, 0),
        }

    def parse_token(self, token: str) -> None:
        action, nargs = self.tokens.get(token, (self._nop, 0))
        if len(self.stack) < nargs:
            return
        if action():
            self._display()

    def push(self, value: str) -> bool:
        try:
            numerical_value = float(value)
            if numerical_value.is_integer():
                numerical_value = int(value)
            self.stack.append(numerical_value)
            return True
        except ValueError:
            self.parse_token(value)
            return False

    def _display(self) -> bool:
        if len(self.stack) == 0:
            print()
        else:
            print(" ".join(str(i) for i in self.stack))
        return False

    def _add(self) -> bool:
        self.stack.append(self.stack.pop() + self.stack.pop())
        return True

    def _sub(self) -> bool:
        x = self.stack.pop()
        y = self.stack.pop()
        self.stack.append(y - x)
        return True

    def _mult(self) -> bool:
        self.stack.append(self.stack.pop() * self.stack.pop())
        return True

    def _div(self) -> bool:
        x = self.stack.pop()
        y = self.stack.pop()
        self.stack.append(y / x)
        return True

    def _pow(self) -> bool:
        x = self.stack.pop()
        y = self.stack.pop()
        self.stack.append(y**x)
        return True

    def _clear(self) -> bool:
        self.stack = []
        return False

    def _help(self) -> bool:
        print("Available operations:")
        for token in self.tokens:
            print(f"Operator: {token}\tStack Pops: {self.tokens[token][1]}")
        print("'.' prints the stack, ',' clears the stack")
        return False

    def _nop(self) -> bool:
        return False


def interactive() -> NoReturn:
    stack = Stack()
    try:
        while True:
            sys.stdout.write("  > ")
            input_string = input()
            if input_string == "\\":
                break
            for value in input_string.split(" "):
                stack.push(value)
    except EOFError:
        sys.stdout.write("\n")
    sys.exit()


def single_program(program: list[str]) -> NoReturn:
    stack = Stack()
    for value in program:
        stack.push(value)
    sys.exit()


def main(arguments: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="pyclacker", description="Reverse polish notation (RPN) calculator"
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{parser.prog}: {__version__}",
    )
    parser.add_argument(
        "program",
        nargs="?",
        help="Program to pass to calculator. Provide as a string with statements separated by a space. Enter interactive moded if not provided",
    )

    args = parser.parse_args(arguments)
    if args.program is None:
        interactive()
    single_program(args.program)


if __name__ == "__main__":
    main()
