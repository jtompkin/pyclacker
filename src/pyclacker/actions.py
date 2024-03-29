from collections.abc import Callable

from pyclacker.operations import nop
from pyclacker import interfaces


class StackAction(interfaces.Action):
    """Action that operates on a stack"""

    def __init__(
        self,
        pops: int = 0,
        pushes: int = 0,
        action: Callable[[interfaces.Stack], None] = nop,
    ) -> None:
        self._pops = pops
        self._pushes = pushes
        self._action = action
        self._help = self._make_help()

    @property
    def pops(self) -> int:
        return self._pops

    @property
    def pushes(self) -> int:
        return self._pushes

    @property
    def action(self) -> Callable[[interfaces.Stack], None]:
        return self._action

    @property
    def help(self) -> str:
        return self._help

    def _make_help(self) -> str:
        help_string = self.action.__doc__
        if help_string is None:
            return ""
        return f'"{" ".join(help_string.strip().split())}"'

    def __call__(self, value: interfaces.Stack) -> None:
        self.action(value)


class MetaAction(interfaces.Action):
    """Action that operates on a stack operator"""

    def __init__(self, action: Callable[[interfaces.StackOperator], None]) -> None:
        self._pops = 0
        self._pushes = 0
        self._action = action
        self._help = self._make_help()

    @property
    def pops(self) -> int:
        return self._pops

    @property
    def pushes(self) -> int:
        return self._pushes

    @property
    def action(self) -> Callable[[interfaces.StackOperator], None]:
        return self._action

    @property
    def help(self) -> str:
        return self._help

    def _make_help(self) -> str:
        help_string = self.action.__doc__
        if help_string is None:
            return ""
        return f'"{" ".join(help_string.strip().split())}"'

    def __call__(self, value: interfaces.StackOperator) -> None:
        self.action(value)
