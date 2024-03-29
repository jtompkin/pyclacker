from collections.abc import Callable
import sys
import math


class Stack:
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


def nop(_: Stack) -> None:
    """Do Nothing."""
    return


class Action:
    """Operates on the stack."""

    def __init__(
        self,
        pops: int = 0,
        pushes: int = 0,
        action: Callable[[Stack], None] = nop,
    ) -> None:
        self.pops = pops
        self.pushes = pushes
        self.action = action
        self.help = self._make_help()

    def _make_help(self) -> str:
        help_string = self.action.__doc__
        if help_string is None:
            return ""
        return f'"{" ".join(help_string.strip().split())}"'

    def __call__(self, stack: Stack) -> None:
        self.action(stack)


def _fail(stack: Stack, message: str, *values: int | float) -> None:
    """Print `message` and push any `values` to the `stack`."""
    stack.push(*values, display=False)
    sys.stderr.write(message + "\n")


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
    if int(divisor) == 0:
        _fail(stack, "Cannot divide by 0", divisor)
        return
    dividend = stack.pop()
    stack.push(dividend / divisor)


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
