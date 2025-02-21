from truss.types import Truss
import numpy as np


class SolvingException(Exception):
    pass


def solve(data: Truss):
    """
    Setup system of equations & solve it
      F_AB F_BC ... F_CD
    ┌                      ┐┌      ┐   ┌
    │  c_1  c_2   .    .   ││ F_AB │   │
    │    .    .   .    .   ││  ... │ = │
    │    .    .   .  c_n   ││ F_YZ │   │
    └                      ┘└      ┘   └
    """

    if len(data["members"]) + len(data["reactions"]) != 2 * len(data["nodes"]):
        raise SolvingException(
            "Unfinished truss structures, members + reactions must equal 2 * joints"
        )

    dim = 2 * len(data["nodes"])

    # Each row in `left` represents the sum equations in the x, then y direction.
    # Each column represents first each member, then each support reaction.
    # The matrix is the coefficients showing how much the column influences the equation per say
    # for example a 45 diagonal beam would only influence the x by cos(45) amount
    left = np.zeros((dim, dim))
    right = np.zeros(dim)

    for i, node in enumerate(data["nodes"]):
        # Start adding each 2-force member
        for j, member in enumerate(data["members"]):
            if i not in member:
                continue
            other = data["nodes"][([node for node in member if node != i][0])]

            dx = other["x"] - node["x"]
            dy = other["y"] - node["y"]
            d: float = np.hypot(dx, dy)

            left[2 * i, j] = dx / d
            left[2 * i + 1, j] = dy / d
        # End adding each 2-force member

        # Start adding supports
        if {"node": i, "type": "x"} in data["reactions"]:
            left[
                2 * i,
                len(data["members"])
                + data["reactions"].index({"node": i, "type": "x"}),
            ] = 1
        if {"node": i, "type": "y"} in data["reactions"]:
            left[
                2 * i + 1,
                len(data["members"])
                + data["reactions"].index({"node": i, "type": "y"}),
            ] = 1
        # End adding supports

    # Start force sum
    for force in data["forces"]:
        if force["x"]:
            right[2 * force["node"]] = force["x"]
        if force["y"]:
            right[2 * force["node"] + 1] = force["y"]
    # End force sum

    soln = np.linalg.solve(left, right)

    return soln
