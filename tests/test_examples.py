import truss
import jsonschema.exceptions
from pytest import raises, approx


def test_soln_a():
    with open("tests/ex_a.json") as f:
        data = truss.json.validate(f)

    soln = truss.math.solve(data)

    assert soln[0] == approx(195000.0)
    assert soln[3] == approx(-169705.62748477142)


def test_out_of_range():
    with raises(truss.json.TrussValidationException):
        with open("tests/out_of_range.json") as f:
            truss.json.validate(f)


def test_invalid():
    with raises(jsonschema.exceptions.ValidationError):
        with open("tests/invalid.json") as f:
            truss.json.validate(f)
