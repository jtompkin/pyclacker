#!/usr/bin/env python3
import argparse
import sys

from pyclacker.version import __version__
from pyclacker.operation import StackOperator


def get_stack(words_file_path: str | None) -> StackOperator:
    operator = StackOperator()
    if words_file_path is None:
        return operator
    with open(words_file_path, "r") as words_file:
        if not operator.parse_words_file(words_file):
            sys.stderr.write(
                "Run `help` to see list of operators that cannot be redefined\n"
            )
    return operator


def interactive(operator: StackOperator, display_counter: bool) -> None:
    while True:
        try:
            operator.parse_input(
                input(f" {len(operator.stack) if display_counter else ''} > ")
            )
        except EOFError:
            sys.stdout.write("\n")
            return


def single_program(program: str, operator: StackOperator) -> None:
    operator.parse_input(program)


def main(arguments: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="pyclacker", description="Reverse polish notation (RPN) calculator"
    )
    parser.add_argument(
        "-c",
        "--calc-help",
        dest="calc_help",
        action="store_true",
        help="show information about available operators and exit",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{parser.prog} {__version__}",
    )
    parser.add_argument(
        "-n",
        "--no-counter",
        dest="display_counter",
        action="store_false",
        help="do not display stack counter in interactive mode",
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
    stack = get_stack(args.words_file)
    if args.calc_help:
        stack.parse_input("help")
        return
    if args.program is not None:
        single_program(args.program, stack)
        return
    interactive(stack, args.display_counter)


if __name__ == "__main__":
    main()
