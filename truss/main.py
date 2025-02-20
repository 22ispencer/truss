from typing import Annotated
import typer
import truss.json

app = typer.Typer()


@app.command()
def file(
    file: str,
    output: Annotated[
        str, typer.Option(help="The file to output the report to")
    ] = "report.txt",
):
    with open(file, "r") as f:
        data = truss.json.validate(f)

    with open(output, "w+") as f:
        f.write("Empty report")


@app.command()
def repl():
    print("repl")


def entry():
    app()
