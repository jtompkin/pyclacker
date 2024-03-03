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
            "words": (self._words, 0),
            "help": (self._help, 0),
        }
        self.words: dict[str, str] = {
            "sqrt": "0.5 ^",
            "pi": "3.14159265358979323846",
        }

    def parse_token(self, token: str) -> None:
        action, nargs = self.tokens.get(token, (self._nop, 0))
        if len(self.stack) < nargs:
            return
        if action():
            self._display()

    def parse_word(self, word: str) -> None:
        for value in self.words.get(word, " ").split(" "):
            self.push(value)

    def push(self, value: str) -> bool:
        try:
            numerical_value = float(value)
            if numerical_value.is_integer():
                numerical_value = int(value)
            self.stack.append(numerical_value)
            return True
        except ValueError:
            if value in self.words:
                self.parse_word(value)
            else:
                self.parse_token(value)
            return False

    def add_word(self, word: str, definition: str) -> bool:
        if word in self.tokens:
            sys.stderr.write(f"Cannot redefine: {word}\n")
            return False
        self.words.update({word: definition})
        return True

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

    def _words(self) -> bool:
        print("Defined words:")
        for word, definition in self.words.items():
            print(f"{word}: {definition}")
        return False

    def _nop(self) -> bool:
        return False


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
                "Run help to see list of operators that cannot be redefined\n"
            )
    return stack


def interactive(stack: Stack) -> NoReturn:
    try:
        while True:
            sys.stdout.write("  > ")
            input_string = input().strip()
            if input_string == "\\":
                break
            for value in input_string.split(" "):
                stack.push(value)
    except EOFError:
        sys.stdout.write("\n")
    sys.exit()


def single_program(program: list[str], stack: Stack) -> NoReturn:
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
        "-w",
        "--words-file",
        dest="words_file",
        help="Path to file containing word definitions. Reads from standard in if '-', which is the default if provided withouth an argument. One definition per line. First word per line is the word itself, the rest is the definition. Ex. sqrt 0.5 ^",
    )
    parser.add_argument(
        "program",
        nargs="?",
        help="Program to pass to calculator. Provide as a string with statements separated by a space. Enter interactive moded if not provided",
    )

    args = parser.parse_args(arguments)
    if args.words_file is not None:
        stack = parse_words_file(args.words_file)
    else:
        stack = Stack()
    if args.program is not None:
        single_program(args.program.split(" "), stack)
    interactive(stack)


if __name__ == "__main__":
    main()
