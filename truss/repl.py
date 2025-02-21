from enum import Enum
from typing import override
from prompt_toolkit import HTML, PromptSession, print_formatted_text as print
from prompt_toolkit.completion import Completer, Completion, CompleteEvent
from prompt_toolkit.document import Document
from collections.abc import Iterable
from truss.types import Truss


class Command(str, Enum):
    new = "new"
    delete = "delete"
    print = "print"
    exit_ = "exit"


class Object(str, Enum):
    node = "node"
    reaction = "reaction"
    force = "force"
    member = "member"


class CommandCompleter(Completer):
    @override
    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        input_command = document.current_line.split(" ")
        if len(input_command) == 1:
            for command in Command:
                if command.startswith(input_command[0]):
                    yield Completion(command, start_position=-len(input_command[0]))
        elif len(input_command) == 2:
            if input_command[0] in [Command.new, Command.delete]:
                for obj in Object:
                    if obj.startswith(input_command[1]):
                        yield Completion(obj, start_position=-len(input_command[1]))


class InvalidArgumentException(Exception):
    pass


class Session:
    data: Truss = {"nodes": [], "members": [], "forces": [], "reactions": []}
    completer: Completer = CommandCompleter()
    session: PromptSession[str] = PromptSession(completer=completer)

    def new_node(self, args: list[str]):
        if len(args) == 0:
            user_input = self.session.prompt("x: ")
            x = safe_float(user_input)
            while x is None:
                print(
                    f"Please enter a valid number, '{user_input}' not parseable to int"
                )
                user_input = self.session.prompt("x: ")
                x = safe_float(user_input)

            user_input = self.session.prompt("y: ")
            y = safe_float(user_input)
            while y is None:
                print(
                    f"Please enter a valid number, '{user_input}' not parseable to int"
                )
                user_input = self.session.prompt("y: ")
                y = safe_float(user_input)

            self.data["nodes"].append({"x": x, "y": y})

        elif len(args) == 2:
            x = safe_float(args[0])
            y = safe_float(args[1])
            print(x, y)
            if x is None:
                raise InvalidArgumentException("'x' not parseable to float")
            if y is None:
                raise InvalidArgumentException("'y' not parseable to float")
            self.data["nodes"].append({"x": x, "y": y})
    print(HTML("\n<b><u>New Node</u></b>"))
        print(f"node {len(self.data["nodes"])-1}: {self.data["nodes"][-1]}")

    def loop(self):
        while True:
            input_command = self.session.prompt("> ").split()
            if len(input_command) > 0 and Command.exit_ in input_command:
                break
            elif (
                len(input_command) >= 2
                and input_command[0] == Command.new
                and input_command[1] == Object.node
            ):
                self.new_node(input_command[2:])
            elif (
                len(input_command) >= 2
                and input_command[0] == Command.delete
                and input_command[1] == Object.node
            ):
                pop_ind = (
                    len(input_command) > 2
                    and (n := safe_int(input_command[2])) is not None
                    and n
                    or -1
                )

                _ = self.data["nodes"].pop(pop_ind)
            elif (
                len(input_command) >= 2
                and input_command[0] == Command.print
                and input_command[1] == Object.node
            ):
                print("")
                if (
                    len(input_command) > 2
                    and (n := safe_int(input_command[2])) is not None
                ):
                    print(self.data["nodes"][n])
                else:
                    print(HTML("<b><u>Nodes</u></b>"))
                    for i, node in enumerate(self.data["nodes"]):
                        print(f"node {i}: {node}")
                print("")


def main_loop():
    Session().loop()


def safe_float(string: str) -> float | None:
    try:
        return float(string)
    except ValueError:
        return None


def safe_int(string: str) -> int | None:
    try:
        return int(string)
    except ValueError:
        return None
