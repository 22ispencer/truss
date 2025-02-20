import truss.json
import truss.main
import jsonschema.exceptions
import pytest


def test_valid():
    with open("tests/ex_a.json") as f:
        truss.json.validate(f)


def test_out_of_range():
    with pytest.raises(truss.json.TrussValidationException):
        with open("tests/out_of_range.json") as f:
            truss.json.validate(f)


def test_invalid():
    with pytest.raises(jsonschema.exceptions.ValidationError):
        with open("tests/invalid.json") as f:
            truss.json.validate(f)
