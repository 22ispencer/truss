from enum import Enum
from typing import TypedDict, NotRequired


# alternative syntax to get around `type` keyword
Reaction = TypedDict("Reaction", {"node": int, "type": str})


class Force(TypedDict):
    node: int
    x: float
    y: float


class Node(TypedDict):
    x: float
    y: float


class Truss(TypedDict):
    nodes: list[Node]
    members: list[list[int]]
    reactions: list[Reaction]
    forces: list[Force]
