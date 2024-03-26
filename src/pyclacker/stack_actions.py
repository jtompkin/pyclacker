import sys
from typing import NoReturn
import math


def display(stack: list[float]) -> list[float]:
    """Print the stack to the screen"""
    print(" ".join(str(i) for i in stack))
    return stack


def add(stack: list[float]) -> list[float]:
    """Pop 2 values from the stack, add them, and push the result to the stack"""
    return _push(stack, stack.pop() + stack.pop())


def subtract(stack: list[float]) -> list[float]:
    """Pop 2 values from the stack, subtract the second item popped from the first, and push the result to the stack"""
    x = stack.pop()
    y = stack.pop()
    return _push(stack, y - x)


def multiply(stack: list[float]) -> list[float]:
    """Pop 2 values from the stack, multiply them, and push the result to the stack"""
    return _push(stack, stack.pop() * stack.pop())


def divide(stack: list[float]) -> list[float]:
    """Pop 2 values from the stack, divide the second value popped by the first, and push the result to the stack"""
    divisor = stack.pop()
    if int(divisor) == 0:
        return _fail(stack, "Cannot divide by 0", divisor)
    dividend = stack.pop()
    return _push(stack, dividend / divisor)


def power(stack: list[float]) -> list[float]:
    """Pop 2 values from the stack, raise the second value popped to the power of the first, and push the result to the stack"""
    exponent = stack.pop()
    base = stack.pop()
    if not float(exponent).is_integer() and base < 0:
        return _fail(
            stack,
            "Negative number cannot be raised to non-integer power",
            base,
            exponent,
        )
    if exponent < 0 and int(base) == 0:
        return _fail(stack, "0 Cannot be raised to a negative power")
    return _push(stack, base**exponent)


def factorial(stack: list[float]) -> list[float]:
    """Pop 1 value from the stack, take its factorial, and push the result to the stack"""
    x = stack.pop()
    if not isinstance(x, int):
        return _fail(stack, "Cannot take the factorial of non-integer number", x)
    if x < 0:
        return _fail(stack, "Cannot take the factorial of negative number", x)
    return _push(stack, math.factorial(x))


def degrees(stack: list[float]) -> list[float]:
    """Pop 1 value from the stack, convert it to degrees, and push the result to the stack"""
    return _push(stack, math.degrees(stack.pop()))


def radians(stack: list[float]) -> list[float]:
    """Pop 1 value from the stack, convert it to radians, and push the result to the stack"""
    return _push(stack, math.radians(stack.pop()))


def sine(stack: list[float]) -> list[float]:
    """Pop 1 value from the stack as radians, take its sine, and push the result to the stack"""
    return _push(stack, math.sin(stack.pop()))


def cosine(stack: list[float]) -> list[float]:
    """Pop 1 value from the stack as radians, take its cosine, and push the result to the stack"""
    return _push(stack, math.cos(stack.pop()))


def round_value(stack: list[float]) -> list[float]:
    """Pop 2 values from the stack, round the second item popped to the precision of the first, and push the result to the stack"""
    precision = stack.pop()
    if not float(precision).is_integer():
        return _fail(stack, "Precision must be an integer")
    x = stack.pop()
    return _push(stack, round(x, int(precision)))


def pop(stack: list[float]) -> list[float]:
    """Pop a single value from the stack"""
    stack.pop()
    display(stack)
    return stack


def clear(stack: list[float]) -> list[float]:
    """Clear the entire stack"""
    print(f"cleared {len(stack)} values")
    return []


def nop(stack: list[float]) -> list[float]:
    """Do Nothing"""
    return stack


def quit(_: list[float]) -> NoReturn:
    """Exit interactive mode"""
    sys.exit(0)


def _cond_float_to_int(value: float) -> float | int:
    if float(value).is_integer():
        return int(value)
    return value


def _push(stack: list[float], value: float | int) -> list[float]:
    stack.append(_cond_float_to_int(value))
    display(stack)
    return stack


def _fail(
    stack: list[float], message: str, *values: float, push: bool = True
) -> list[float]:
    """
    Called when a computation cannot be done. Prints a message to the screen,
    and optionally pushes values back onto the stack
    """
    if push:
        stack += values
    sys.stderr.write(message + "\n")
    return stack
