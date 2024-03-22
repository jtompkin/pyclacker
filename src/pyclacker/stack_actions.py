import sys
from typing import NoReturn


def display(stack: list[float]) -> list[float]:
    """Print the stack to the screen"""
    print(" ".join(str(i) for i in stack))
    return stack


def add(stack: list[float]) -> list[float]:
    """Pop 2 values from the stack, add them, and push the result to the stack"""
    stack.append(stack.pop() + stack.pop())
    display(stack)
    return stack


def subtract(stack: list[float]) -> list[float]:
    """Pop 2 values from the stack, subtract the second item popped from the first, and push the result to the stack"""
    x = stack.pop()
    y = stack.pop()
    stack.append(_cond_float_to_int(y - x))
    display(stack)
    return stack


def multiply(stack: list[float]) -> list[float]:
    """Pop 2 values from the stack, multiply them, and push the result to the stack"""
    stack.append(_cond_float_to_int(stack.pop() * stack.pop()))
    display(stack)
    return stack


def divide(stack: list[float]) -> list[float]:
    """Pop 2 values from the stack, divide the second value popped by the first, and push the result to the stack"""
    divisor = stack.pop()
    dividend = stack.pop()
    if int(divisor) == 0:
        return _fail(stack, "Cannot divide by 0", dividend, divisor)
    stack.append(_cond_float_to_int(dividend / divisor))
    display(stack)
    return stack


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
    stack.append(_cond_float_to_int(base**exponent))
    display(stack)
    return stack


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
