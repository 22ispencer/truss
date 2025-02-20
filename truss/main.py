from typing import Annotated
import typer

app = typer.Typer()


@app.command()
def file(
    file: str,
    output: Annotated[
        str, typer.Option(help="The file to output the report to")
    ] = "report.txt",
):
    with open(output, "w+") as f:
        f.write("Empty report")


@app.command()
def repl():
    print("repl")


def entry():
    app()
