import truss.json as json
import pytest


def test_valid():
    with open("tests/ex_a.json") as f:
        json.validate(f)


def test_out_of_range():
    with pytest.raises(json.TrussValidationException):
        with open("tests/ex_out_of_range.json") as f:
            json.validate(f)
