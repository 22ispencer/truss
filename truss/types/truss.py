from typing import TypedDict, NotRequired


class NodeSupport(TypedDict):
    x: NotRequired[bool]
    y: NotRequired[bool]
    xy: NotRequired[bool]


class NodeForce(TypedDict):
    x: float
    y: float


class Node(TypedDict):
    x: float
    y: float
    supports: NotRequired[NodeSupport]
    force: NotRequired[NodeForce]


class Truss(TypedDict):
    nodes: list[Node]
    members: list[list[int]]
