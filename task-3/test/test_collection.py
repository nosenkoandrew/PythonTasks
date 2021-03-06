from ..task_collections import task3
import pytest

cases = [
        ("abbbcccdf", 3),
        ("aaaaa", 0),
        ("", 0),
    ]

def test_collections():
    for in_data, out_data in cases:
        res = task3.non_repeating_elems(in_data)
        assert res == out_data

def test_error():
    with pytest.raises(ValueError):
        task3.non_repeating_elems(12435)


