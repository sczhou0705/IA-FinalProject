"""
Tests that the specified index column (a.k.a "index_col")
is properly handled or inferred during parsing for all of
the parsers defined in parsers.py
"""
from io import StringIO

import numpy as np
import pytest

from pandas import DataFrame, Index, MultiIndex
import pandas._testing as tm


@pytest.mark.parametrize("with_header", [True, False])
def test_index_col_named(all_parsers, with_header):
    parser = all_parsers
    no_header = """\
KORD1,19990127, 19:00:00, 18:56:00, 0.8100, 2.8100, 7.2000, 0.0000, 280.0000
KORD2,19990127, 20:00:00, 19:56:00, 0.0100, 2.2100, 7.2000, 0.0000, 260.0000
KORD3,19990127, 21:00:00, 20:56:00, -0.5900, 2.2100, 5.7000, 0.0000, 280.0000
KORD4,19990127, 21:00:00, 21:18:00, -0.9900, 2.0100, 3.6000, 0.0000, 270.0000
KORD5,19990127, 22:00:00, 21:56:00, -0.5900, 1.7100, 5.1000, 0.0000, 290.0000
KORD6,19990127, 23:00:00, 22:56:00, -0.5900, 1.7100, 4.6000, 0.0000, 280.0000"""
    header = "ID,date,NominalTime,ActualTime,TDew,TAir,Windspeed,Precip,WindDir\n"

    if with_header:
        data = header + no_header

        result = parser.read_csv(StringIO(data), index_col="ID")
        expected = parser.read_csv(StringIO(data), header=0).set_index("ID")
        tm.assert_frame_equal(result, expected)
    else:
        data = no_header
        msg = "Index ID invalid"

        with pytest.raises(ValueError, match=msg):
            parser.read_csv(StringIO(data), index_col="ID")


def test_index_col_named2(all_parsers):
    parser = all_parsers
    data = """\
1,2,3,4,hello
5,6,7,8,world
9,10,11,12,foo
"""

    expected = DataFrame(
        {"a": [1, 5, 9], "b": [2, 6, 10], "c": [3, 7, 11], "d": [4, 8, 12]},
        index=Index(["hello", "world", "foo"], name="message"),
    )
    names = ["a", "b", "c", "d", "message"]

    result = parser.read_csv(StringIO(data), names=names, index_col=["message"])
    tm.assert_frame_equal(result, expected)


def test_index_col_is_true(all_parsers):
    # see gh-9798
    data = "a,b\n1,2"
    parser = all_parsers

    msg = "The value of index_col couldn't be 'True'"
    with pytest.raises(ValueError, match=msg):
        parser.read_csv(StringIO(data), index_col=True)


def test_infer_index_col(all_parsers):
    data = """A,B,C
foo,1,2,3
bar,4,5,6
baz,7,8,9
"""
    parser = all_parsers
    result = parser.read_csv(StringIO(data))

    expected = DataFrame(
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        index=["foo", "bar", "baz"],
        columns=["A", "B", "C"],
    )
    tm.assert_frame_equal(result, expected)


@pytest.mark.parametrize(
    "index_col,kwargs",
    [
        (None, dict(columns=["x", "y", "z"])),
        (False, dict(columns=["x", "y", "z"])),
        (0, dict(columns=["y", "z"], index=Index([], name="x"))),
        (1, dict(columns=["x", "z"], index=Index([], name="y"))),
        ("x", dict(columns=["y", "z"], index=Index([], name="x"))),
        ("y", dict(columns=["x", "z"], index=Index([], name="y"))),
        (
            [0, 1],
            dict(
                columns=["z"], index=MultiIndex.from_arrays([[]] * 2, names=["x", "y"])
            ),
        ),
        (
            ["x", "y"],
            dict(
                columns=["z"], index=MultiIndex.from_arrays([[]] * 2, names=["x", "y"])
            ),
        ),
        (
            [1, 0],
            dict(
                columns=["z"], index=MultiIndex.from_arrays([[]] * 2, names=["y", "x"])
            ),
        ),
        (
            ["y", "x"],
            dict(
                columns=["z"], index=MultiIndex.from_arrays([[]] * 2, names=["y", "x"])
            ),
        ),
    ],
)
def test_index_col_empty_data(all_parsers, index_col, kwargs):
    data = "x,y,z"
    parser = all_parsers
    result = parser.read_csv(StringIO(data), index_col=index_col)

    expected = DataFrame(**kwargs)
    tm.assert_frame_equal(result, expected)


def test_empty_with_index_col_false(all_parsers):
    # see gh-10413
    data = "x,y"
    parser = all_parsers
    result = parser.read_csv(StringIO(data), index_col=False)

    expected = DataFrame(columns=["x", "y"])
    tm.assert_frame_equal(result, expected)


@pytest.mark.parametrize(
    "index_names",
    [
        ["", ""],
        ["foo", ""],
        ["", "bar"],
        ["foo", "bar"],
        ["NotReallyUnnamed", "Unnamed: 0"],
    ],
)
def test_multi_index_naming(all_parsers, index_names):
    parser = all_parsers

    # We don't want empty index names being replaced with "Unnamed: 0"
    data = ",".join(index_names + ["col\na,c,1\na,d,2\nb,c,3\nb,d,4"])
    result = parser.read_csv(StringIO(data), index_col=[0, 1])

    expected = DataFrame(
        {"col": [1, 2, 3, 4]}, index=MultiIndex.from_product([["a", "b"], ["c", "d"]])
    )
    expected.index.names = [name if name else None for name in index_names]
    tm.assert_frame_equal(result, expected)


def test_multi_index_naming_not_all_at_beginning(all_parsers):
    parser = all_parsers
    data = ",Unnamed: 2,\na,c,1\na,d,2\nb,c,3\nb,d,4"
    result = parser.read_csv(StringIO(data), index_col=[0, 2])

    expected = DataFrame(
        {"Unnamed: 2": ["c", "d", "c", "d"]},
        index=MultiIndex(
            levels=[["a", "b"], [1, 2, 3, 4]], codes=[[0, 0, 1, 1], [0, 1, 2, 3]]
        ),
    )
    tm.assert_frame_equal(result, expected)


def test_no_multi_index_level_names_empty(all_parsers):
    # GH 10984
    parser = all_parsers
    midx = MultiIndex.from_tuples([("A", 1, 2), ("A", 1, 2), ("B", 1, 2)])
    expected = DataFrame(np.random.randn(3, 3), index=midx, columns=["x", "y", "z"])
    with tm.ensure_clean() as path:
        expected.to_csv(path)
        result = parser.read_csv(path, index_col=[0, 1, 2])
    tm.assert_frame_equal(result, expected)


def test_header_with_index_col(all_parsers):
    # GH 33476
    parser = all_parsers
    data = """
I11,A,A
I12,B,B
I2,1,3
"""
    midx = MultiIndex.from_tuples([("A", "B"), ("A", "B.1")], names=["I11", "I12"])
    idx = Index(["I2"])
    expected = DataFrame([[1, 3]], index=idx, columns=midx)

    result = parser.read_csv(StringIO(data), index_col=0, header=[0, 1])
    tm.assert_frame_equal(result, expected)

    col_idx = Index(["A", "A.1"])
    idx = Index(["I12", "I2"], name="I11")
    expected = DataFrame([["B", "B"], ["1", "3"]], index=idx, columns=col_idx)

    result = parser.read_csv(StringIO(data), index_col="I11", header=0)
    tm.assert_frame_equal(result, expected)


@pytest.mark.slow
def test_index_col_large_csv(all_parsers):
    # https://github.com/pandas-dev/pandas/issues/37094
    parser = all_parsers

    N = 1_000_001
    df = DataFrame({"a": range(N), "b": np.random.randn(N)})

    with tm.ensure_clean() as path:
        df.to_csv(path, index=False)
        result = parser.read_csv(path, index_col=[0])

    tm.assert_frame_equal(result, df.set_index("a"))
