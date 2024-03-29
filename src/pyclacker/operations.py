from shutil import get_terminal_size
from typing import NoReturn
from textwrap import wrap
import sys, os
import math

from pyclacker.interfaces import Stack, StackOperator


def _fail(stack: Stack, message: str, *values: int | float) -> None:
    """Print `message` and push any `values` to the `stack`."""
    stack.push(*values, display=False)
    sys.stderr.write(message + "\n")


# ================
# Stack operations
# ================


def nop(_: Stack) -> None:
    """Do Nothing."""
    return


def add(stack: Stack) -> None:
    """Pop 2 values from the stack, add them, and push the result to the stack."""
    stack.push(stack.pop() + stack.pop())


def subtract(stack: Stack) -> None:
    """
    Pop 2 values from the stack, subtract the second item popped from the first,
    and push the result to the stack.
    """
    x = stack.pop()
    y = stack.pop()
    stack.push(y - x)


def multiply(stack: Stack) -> None:
    """Pop 2 values from the stack, multiply them, and push the result to the
    stack."""
    stack.push(stack.pop() * stack.pop())


def divide(stack: Stack) -> None:
    """
    Pop 2 values from the stack, divide the second value popped by the first,
    and push the result to the stack.
    """
    divisor = stack.pop()
    if divisor == 0:
        _fail(stack, "Cannot divide by 0", divisor)
        return
    dividend = stack.pop()
    stack.push(dividend / divisor)


def modulo(stack: Stack) -> None:
    """
    Pop 2 values from the stack, divide the second value popped by the first,
    and push the remainder of the division to the stack.
    """
    divisor = stack.pop()
    if int(divisor) == 0:
        _fail(stack, "Cannot divide by 0", divisor)
        return
    dividend = stack.pop()
    stack.push(dividend % divisor)


def power(stack: Stack) -> None:
    """
    Pop 2 values from the stack, raise the second value popped to the power of
    the first, and push the result to the stack.
    """
    exponent = stack.pop()
    base = stack.pop()
    if not float(exponent).is_integer() and base < 0:
        _fail(
            stack,
            "Negative number cannot be raised to non-integer power",
            base,
            exponent,
        )
        return
    if exponent < 0 and int(base) == 0:
        _fail(stack, "0 Cannot be raised to a negative power")
        return
    stack.push(base**exponent)


def factorial(stack: Stack) -> None:
    """
    Pop 1 value from the stack, take its factorial, and push the result to the
    stack.
    """
    x = stack.pop()
    if not isinstance(x, int):
        _fail(stack, "Cannot take the factorial of non-integer number", x)
        return
    if x < 0:
        _fail(stack, "Cannot take the factorial of negative number", x)
        return
    stack.push(math.factorial(x))


def degrees(stack: Stack) -> None:
    """
    Pop 1 value from the stack, convert it to degrees, and push the result to
    the stack.
    """
    stack.push(math.degrees(stack.pop()))


def radians(stack: Stack) -> None:
    """
    Pop 1 value from the stack, convert it to radians, and push the result to
    the stack.
    """
    stack.push(math.radians(stack.pop()))


def sine(stack: Stack) -> None:
    """
    Pop 1 value from the stack as radians, take its sine, and push the result to
    the stack.
    """
    stack.push(math.sin(stack.pop()))


def cosine(stack: Stack) -> None:
    """
    Pop 1 value from the stack as radians, take its cosine, and push the result
    to the stack.
    """
    stack.push(math.cos(stack.pop()))


def round_value(stack: Stack) -> None:
    """
    Pop 2 values from the stack, round the second item popped to the precision
    of the first, and push the result to the stack.
    """
    precision = stack.pop()
    if not float(precision).is_integer():
        _fail(stack, "Precision must be an integer")
        return
    x = stack.pop()
    stack.push(round(x, int(precision)))


def pop(stack: Stack) -> None:
    """Pop a single value from the stack."""
    stack.pop()
    print(stack)


def clear(stack: Stack) -> None:
    """Clear the entire stack."""
    print(f"cleared {len(stack.values)} values")
    stack.values = []


def display(stack: Stack) -> None:
    """Print values from the stack."""
    print(stack)


def log(stack: Stack) -> None:
    """
    Pop 1 value from the stack, take its logarithm base 10, and push the result
    to the stack.
    """
    value = stack.pop()
    if value <= 0:
        _fail(stack, "Cannot take logarithm of non-positive number", value)
        return
    stack.push(math.log10(value))


def ln(stack: Stack) -> None:
    """
    Pop 1 value from the stack, take its natural logarithm, and push the result
    to the stack.
    """
    value = stack.pop()
    if value <= 0:
        _fail(stack, "Cannot take logarithm of non-positive number", value)
        return
    stack.push(math.log(value, math.e))


def stack_sum(stack: Stack) -> None:
    """Pop all vaues from the stack, sum them, and push the result to the stack."""
    value = sum(stack.values)
    stack.values = []
    stack.push(value)


def stash(stack: Stack) -> None:
    """Pop 1 value from the stack and stash it."""
    stack.stash = stack.pop()


def pull(stack: Stack) -> None:
    """Copy value from the stash and push it to the stack."""
    stack.push(stack.stash)


# ===============
# Meta operations
# ===============


def words(operator: StackOperator) -> None:
    """Print all defined words to the screen."""
    for word, definition in operator.words.items():
        print(f"{word}: {' '.join(definition)}")


def help(stack: StackOperator) -> None:
    """Print information about available operations to the screen."""
    extra_space = 2
    prefix = "operator: "
    max_length = max(len(i) for i in stack.operations) + len(prefix)
    term_width = get_terminal_size()[0] - (max_length + extra_space)
    for token, operator in stack.operations.items():
        operator_help = f"{prefix}{token}"
        padding = max_length - len(operator_help) + extra_space
        sys.stdout.write(operator_help + " " * padding)
        for chunk in wrap(
            operator.help,
            term_width,
            subsequent_indent=" " * (max_length + extra_space),
        ):
            print(chunk)


def clear_screen(_: StackOperator) -> None:
    """Clear the terminal screen."""
    if sys.platform.startswith("win32"):
        os.system("cls")
    elif sys.platform.startswith(("linux", "darwin")):
        os.system("clear")


def quit(_: StackOperator) -> NoReturn:
    """Exit interactive mode."""
    sys.exit(0)
