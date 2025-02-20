from typing import Annotated
import typer
import truss.json
import truss.graphics

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

    if plot:
        print("Showing plot...")
        truss.graphics.plot(data)

    with open(output, "w+") as f:
        f.write("Empty report")


@app.command()
def repl():
    print("repl")


def entry():
    app()
