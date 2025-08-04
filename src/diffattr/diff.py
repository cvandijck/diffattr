from dataclasses import dataclass
from typing import Any, Generator, Optional


@dataclass
class Diff:
    path: str
    ref: Any
    test: Any


PRIMITIVE_TYPES = (int, float, str, bool, type(None))


def _yield_diffs(
    ref: Any, test: Any, prefix_path: str = ''
) -> Generator[Diff, None, None]:
    # if different types, yield directly a diff
    if type(ref) is not type(test):
        yield Diff(path=prefix_path + '', ref=ref, test=test)
        return

    # if they are not equal, directly yield a diff
    if ref != test:
        yield Diff(path=prefix_path + '', ref=ref, test=test)

    # if type is primitive diff has been handled already, return
    if isinstance(ref, PRIMITIVE_TYPES):
        return

    # if type is a sequence, check the elements
    elif isinstance(ref, (list, tuple, set)):
        for i, (r, t) in enumerate(zip(ref, test)):
            yield from _yield_diffs(r, t, prefix_path + f'[{i}]')

    # if type is a dict, check the items
    elif isinstance(ref, dict):
        for key in ref.keys():
            r_value = ref.get(key)
            t_value = test.get(key)
            yield from _yield_diffs(r_value, t_value, prefix_path + f'[{key}]')

    # if type is a custom object, check the attributes
    elif hasattr(ref, '__dict__'):
        for attr in ref.__dict__.keys():
            r_value = getattr(ref, attr)
            t_value = getattr(test, attr, None)
            yield from _yield_diffs(r_value, t_value, prefix_path + f'.{attr}')

    # bit different for slots
    elif hasattr(ref, '__slots__'):
        for attr in ref.__slots__:
            r_value = getattr(ref, attr)
            t_value = getattr(test, attr, None)
            yield from _yield_diffs(r_value, t_value, prefix_path + f'.{attr}')

    # lord have mercy on us
    else:
        raise TypeError(f'Unsupported type: {type(ref)}')


def yield_diffs(ref: Any, test: Any) -> Generator[Diff, None, None]:
    """Yield differences between two objects."""
    yield from _yield_diffs(ref, test)


def report_diffs(ref: Any, test: Any) -> Optional[str]:
    """Generate a report of differences between two objects."""
    diffs = list(yield_diffs(ref, test))
    if not diffs:
        return None

    report_lines = []
    for diff in diffs:
        report_lines.append(
            f'Path: {diff.path}, Ref: {diff.ref}, Test: {diff.test}'
        )

    return '\n'.join(report_lines)
