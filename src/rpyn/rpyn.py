#!/usr/bin/env python3
from typing import Never
import argparse
import sys


class Stack:
    def __init__(self, initial: list[float] | None = None) -> None:
        if initial is None:
            self.stack: list[float] = []
        else:
            self.stack: list[float] = []
        self.tokens = {
            "+": self.add,
            "-": self.sub,
            "*": self.mult,
            "/": self.div,
        }

    def parse_token(self, token: str) -> None:
        action = self.tokens.get(token)
        assert action is not None, f"Could not parse operator: {token}"
        action()

    def push(self, value: float) -> None:
        self.stack.append(value)

    def add(self) -> None:
        self.stack.append(self.stack.pop() + self.stack.pop())

    def sub(self) -> None:
        self.stack.append(self.stack.pop() - self.stack.pop())

    def mult(self) -> None:
        self.stack.append(self.stack.pop() * self.stack.pop())

    def div(self) -> None:
        self.stack.append(self.stack.pop() / self.stack.pop())


def print_prompt() -> None:
    sys.stdout.write("    > ")


def interactive() -> Never:
    stack = Stack()
    while True:
        print_prompt()
        value = input()
        if value == "\\":
            break
        try:
            stack.push(float(value))
        except ValueError:
            stack.parse_token(value)
            print(stack.stack[-1])
    sys.exit()


def main(arguments: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="rpyn", description="Reverse polish notation (RPN) calculator"
    )
    parser.add_argument(
        "program",
        nargs="?",
        help="Program to pass to calculator. Seperate statements with spaces. Enter interactive moded if not provided",
    )
    args = parser.parse_args(arguments)
    if args.program is None:
        interactive()
    sys.stderr.write(
        "Only interactive mode is supported (for now). Do not provide program"
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
