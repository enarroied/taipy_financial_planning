from functools import partial
from typing import Any, Callable, Tuple

from taipy.gui import State, notify


def _check_and_notify(
    condition_func: Callable[[Any, Any], bool],
    state: State,
    operands: Tuple[Any, Any],
    message: str,
    notification_type: str = "w",
) -> bool:
    """
    Core function that executes the given comparison (condition_func)
    and triggers notify if the result is True.
    """
    val1, val2 = operands

    if condition_func(val1, val2):
        notify(state, notification_type, message)
        return True
    else:
        return False


def _compare_equal(a: Any, b: Any) -> bool:
    return a == b


def _compare_in(a: Any, b: Any) -> bool:
    return a in b


def cond_equal_notify(
    state: State, condition: tuple, message: str, notification_type: str = "w"
) -> bool:
    """Checks if condition[0] == condition[1] and notifies if true."""
    return partial(_check_and_notify, _compare_equal)(
        state, condition, message, notification_type
    )


def cond_in_notify(
    state: State, condition: tuple, message: str, notification_type: str = "w"
) -> bool:
    """Checks if condition[0] in condition[1] and notifies if true."""
    return partial(_check_and_notify, _compare_in)(
        state, condition, message, notification_type
    )
