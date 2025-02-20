from typing import Annotated
import typer
import truss.json
import truss.graphics
import truss.math

app = typer.Typer()


@app.command()
def file(
    file: str,
    output: Annotated[
        str, typer.Option(help="The file to output the report to")
    ] = "report.txt",
    plot: Annotated[bool, typer.Option(help="Plot the truss graphically")] = False,
):
    with open(file, "r") as f:
        data = truss.json.validate(f)

    soln = truss.math.solve(data)

    if plot:
        print("Showing plot...")
        truss.graphics.plot(data)

    with open(output, "w+") as f:
        for i in range(len(data["members"])):
            f.write(f"member {i}: {soln[i]}\n")


@app.command()
def repl():
    print("repl")


def entry():
    app()
