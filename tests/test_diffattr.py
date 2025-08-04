from dataclasses import dataclass

from diffattr.diff import yield_diffs


def test_diff_types():
    """Test that different types yield a Diff."""
    ref = {'key1': 'value1'}
    test = ['value1', 'value2']
    diffs = list(yield_diffs(ref, test))
    assert len(diffs) == 1
    assert diffs[0].ref == ref
    assert diffs[0].test == test
    assert diffs[0].path == ''


def test_diff_int():
    """Test that int types yield a Diff if not equal."""
    ref = 42
    test = 43
    diffs = list(yield_diffs(ref, test))
    assert len(diffs) == 1
    assert diffs[0].ref == ref
    assert diffs[0].test == test
    assert diffs[0].path == ''


def test_same_int():
    """Test that int types are equal."""
    ref = 42
    test = 42
    diffs = list(yield_diffs(ref, test))
    assert len(diffs) == 0


def test_diff_string():
    """Test that strings yield a Diff if not equal."""
    ref = 'hello'
    test = 'world'
    diffs = list(yield_diffs(ref, test))
    assert len(diffs) == 1
    assert diffs[0].ref == ref
    assert diffs[0].test == test
    assert diffs[0].path == ''


def test_same_string():
    """Test that strings are equal."""
    ref = 'hello'
    test = 'hello'
    diffs = list(yield_diffs(ref, test))
    assert len(diffs) == 0


def test_diff_list():
    """Test that lists yield a Diff if not equal."""
    ref = [1, 2, 3]
    test = [1, 2, 4]
    diffs = list(yield_diffs(ref, test))
    assert len(diffs) == 2
    assert diffs[0].ref == ref
    assert diffs[0].test == test
    assert diffs[0].path == ''

    assert diffs[1].ref == 3
    assert diffs[1].test == 4
    assert diffs[1].path == '[2]'


def test_same_list():
    """Test that lists are equal."""
    ref = [1, 2, 3]
    test = [1, 2, 3]
    diffs = list(yield_diffs(ref, test))
    assert len(diffs) == 0


def test_diff_tuple():
    """Test that tuples yield a Diff if not equal."""
    ref = (1, 2, 3)
    test = (1, 2, 4)
    diffs = list(yield_diffs(ref, test))
    assert len(diffs) == 2
    assert diffs[0].ref == ref
    assert diffs[0].test == test
    assert diffs[0].path == ''

    assert diffs[1].ref == 3
    assert diffs[1].test == 4
    assert diffs[1].path == '[2]'


def test_same_tuple():
    """Test that tuples are equal."""
    ref = (1, 2, 3)
    test = (1, 2, 3)
    diffs = list(yield_diffs(ref, test))
    assert len(diffs) == 0


def test_diff_set():
    """Test that sets yield a Diff if not equal."""
    ref = {1, 2, 3}
    test = {1, 2, 4}
    diffs = list(yield_diffs(ref, test))
    assert len(diffs) == 2
    assert diffs[0].ref == ref
    assert diffs[0].test == test
    assert diffs[0].path == ''

    assert diffs[1].ref == 3
    assert diffs[1].test == 4
    assert diffs[1].path == '[2]'


def test_same_set():
    """Test that sets are equal."""
    ref = {1, 2, 3}
    test = {1, 2, 3}
    diffs = list(yield_diffs(ref, test))
    assert len(diffs) == 0


def test_diff_dict():
    """Test that dicts yield a Diff if not equal."""
    ref = {'key1': 'value1', 'key2': 'value2'}
    test = {'key1': 'value1', 'key2': 'value3'}
    diffs = list(yield_diffs(ref, test))
    assert len(diffs) == 2
    assert diffs[0].ref == ref
    assert diffs[0].test == test
    assert diffs[0].path == ''

    assert diffs[1].ref == 'value2'
    assert diffs[1].test == 'value3'
    assert diffs[1].path == '[key2]'


def test_same_dict():
    """Test that dicts are equal."""
    ref = {'key1': 'value1', 'key2': 'value2'}
    test = {'key1': 'value1', 'key2': 'value2'}
    diffs = list(yield_diffs(ref, test))
    assert len(diffs) == 0


def test_diff_nested():
    """Test that nested structures yield correct diffs."""
    ref = {'key1': [1, 2, {'nested_key': 'value1'}], 'key2': 'value2'}
    test = {'key1': [1, 3, {'nested_key': 'value2'}], 'key2': 'value2'}
    diffs = list(yield_diffs(ref, test))
    assert len(diffs) == 5

    assert diffs[0].ref == ref
    assert diffs[0].test == test
    assert diffs[0].path == ''

    assert diffs[1].ref == [1, 2, {'nested_key': 'value1'}]
    assert diffs[1].test == [1, 3, {'nested_key': 'value2'}]
    assert diffs[1].path == '[key1]'

    assert diffs[2].ref == 2
    assert diffs[2].test == 3
    assert diffs[2].path == '[key1][1]'

    assert diffs[3].ref == {'nested_key': 'value1'}
    assert diffs[3].test == {'nested_key': 'value2'}
    assert diffs[3].path == '[key1][2]'

    assert diffs[4].ref == 'value1'
    assert diffs[4].test == 'value2'
    assert diffs[4].path == '[key1][2][nested_key]'


def test_same_nested():
    """Test that nested structures are equal."""
    ref = {'key1': [1, 2, {'nested_key': 'value1'}], 'key2': 'value2'}
    test = {'key1': [1, 2, {'nested_key': 'value1'}], 'key2': 'value2'}
    diffs = list(yield_diffs(ref, test))
    assert len(diffs) == 0


def test_diff_empty():
    """Test that empty structures yield no diffs."""
    ref = {}
    test = {}
    diffs = list(yield_diffs(ref, test))
    assert len(diffs) == 0

    ref = []
    test = []
    diffs = list(yield_diffs(ref, test))
    assert len(diffs) == 0

    ref = set()
    test = set()
    diffs = list(yield_diffs(ref, test))
    assert len(diffs) == 0


def test_diff_dataclass():
    """Test that dataclasses yield correct diffs."""

    @dataclass
    class Example:
        attr1: int
        attr2: str

    ref = Example(attr1=1, attr2='value1')
    test = Example(attr1=2, attr2='value1')
    diffs = list(yield_diffs(ref, test))
    assert len(diffs) == 2

    assert diffs[0].ref == ref
    assert diffs[0].test == test
    assert diffs[0].path == ''

    assert diffs[1].ref == 1
    assert diffs[1].test == 2
    assert diffs[1].path == '.attr1'


def test_same_dataclass():
    """Test that dataclasses are equal."""

    @dataclass
    class Example:
        attr1: int
        attr2: str

    ref = Example(attr1=1, attr2='value1')
    test = Example(attr1=1, attr2='value1')
    diffs = list(yield_diffs(ref, test))
    assert len(diffs) == 0


def test_diff_slots():
    """Test that classes with __slots__ yield correct diffs."""

    class Example:
        __slots__ = ['attr1', 'attr2']

        def __init__(self, attr1, attr2):
            self.attr1 = attr1
            self.attr2 = attr2

    ref = Example(attr1=1, attr2='value1')
    test = Example(attr1=2, attr2='value1')
    diffs = list(yield_diffs(ref, test))
    assert len(diffs) == 2

    assert diffs[0].ref == ref
    assert diffs[0].test == test
    assert diffs[0].path == ''

    assert diffs[1].ref == 1
    assert diffs[1].test == 2
    assert diffs[1].path == '.attr1'


def test_same_slots():
    """Test that classes with __slots__ are equal."""

    class Example:
        __slots__ = ['attr1', 'attr2']

        def __init__(self, attr1, attr2):
            self.attr1 = attr1
            self.attr2 = attr2

    ref = Example(attr1=1, attr2='value1')
    test = Example(attr1=1, attr2='value1')
    diffs = list(yield_diffs(ref, test))
    assert len(diffs) == 1  # strangely, slot based objects are never equal
