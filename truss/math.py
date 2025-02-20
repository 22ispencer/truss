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

    supports = [
        (i, "x")
        for i, node in enumerate(data["nodes"])
        if "supports" in node and "x" in node["supports"] and node["supports"]["x"]
    ] + [
        (i, "y")
        for i, node in enumerate(data["nodes"])
        if "supports" in node and "y" in node["supports"] and node["supports"]["y"]
    ]

    if len(data["members"]) + len(supports) != 2 * len(data["nodes"]):
        raise SolvingException(
            "Unfinished truss structures, members + reactions must equal 2 * joints"
        )

    dim = 2 * len(data["nodes"])

    # each row in `left` represents the sum equations in the x, then y direction.
    # each column represents first each member, then each support reaction.
    # the matrix is the coefficients showing how much the column influences the equation per say
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
            d = np.hypot(dx, dy)

            left[2 * i, j] = dx / d
            left[2 * i + 1, j] = dy / d
        # End adding each 2-force member

        # Start adding supports
        if (i, "x") in supports:
            left[2 * i, len(data["members"]) + supports.index((i, "x"))] = 1
        if (i, "y") in supports:
            left[2 * i + 1, len(data["members"]) + supports.index((i, "y"))] = 1
        # End adding supports

        # Start setup force sum
        if "force" in node:
            right[2 * i] = node["force"]["x"]
            right[2 * i + 1] = node["force"]["y"]

    soln = np.linalg.solve(left, right)

    return soln
