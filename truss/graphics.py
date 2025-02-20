import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from truss.types import Truss


def plot(data: Truss):
    _, ax = plt.subplots()

    ax.axis("equal")

    mean_member_len = np.mean(
        [
            np.hypot(
                data["nodes"][member[0]]["x"] - data["nodes"][member[1]]["x"],
                data["nodes"][member[0]]["y"] - data["nodes"][member[1]]["y"],
            )
            for member in data["members"]
        ]
    )
    mean_force_magnitude = np.mean(
        [
            np.hypot(node["force"]["x"], node["force"]["y"])
            for node in data["nodes"]
            if "force" in node
        ]
    )

    for member in data["members"]:
        x = [data["nodes"][node]["x"] for node in member]
        y = [data["nodes"][node]["y"] for node in member]
        ax.plot(x, y, "-b")

    print(mean_member_len, mean_force_magnitude)

    x = [node["x"] for node in data["nodes"]]
    y = [node["y"] for node in data["nodes"]]

    ax.plot(x, y, "og")

    support_scale = float(mean_member_len / 10)

    for node in data["nodes"]:
        if "force" in node and node["force"]:
            scaled_x = float(
                node["force"]["x"] / mean_force_magnitude * 0.5 * mean_member_len
            )
            scaled_y = float(
                node["force"]["y"] / mean_force_magnitude * 0.5 * mean_member_len
            )
            arrow = mpatches.FancyArrowPatch(
                (node["x"] - scaled_x, node["y"] - scaled_y),
                (node["x"], node["y"]),
                mutation_scale=20,
            )
            ax.add_patch(arrow)
        if "supports" in node:
            if (
                "x" in node["supports"]
                and node["supports"]["x"]
                and "y" in node["supports"]
                and node["supports"]["y"]
            ):
                triangle = mpatches.Polygon(
                    [
                        [node["x"], node["y"]],
                        [
                            node["x"] - 0.5 * support_scale,
                            node["y"] - support_scale,
                        ],
                        [
                            node["x"] + 0.5 * support_scale,
                            node["y"] - support_scale,
                        ],
                    ],
                    color="#663d17",
                )
                ax.add_patch(triangle)
            elif "y" in node["supports"] and node["supports"]["y"]:
                circle = mpatches.Circle(
                    (node["x"], node["y"] - support_scale / 2),
                    support_scale / 2,
                    color="#663d17",
                )
                ax.add_patch(circle)

    plt.show()
