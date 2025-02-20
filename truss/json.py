import json
import jsonschema as js
from typing import TextIO
from truss.types import Truss


class TrussValidationException(Exception):
    pass


def validate(file: TextIO) -> Truss:
    data: Truss = json.load(file)

    with open("truss/schema.json", "r") as f:
        schema = json.load(f)

    js.validate(data, schema)

    node_count = len(data["nodes"])

    for member in data["members"]:
        for node in member:
            if node >= node_count:
                raise TrussValidationException("Node out of range")

    return data
