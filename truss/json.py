import json
import jsonschema as js
from typing import TextIO, TypedDict


class NodeSupport(TypedDict):
    x: bool | None
    y: bool | None
    xy: bool | None


class NodeForce(TypedDict):
    x: float
    y: float


class Node(TypedDict):
    x: float
    y: float
    supports: NodeSupport | None
    force: NodeForce | None


class Truss(TypedDict):
    nodes: list[Node]
    members: list[list[int]]


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
