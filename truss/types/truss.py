from typing import TypedDict


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
