from prompt_toolkit import PromptSession, print_formatted_text as print
from prompt_toolkit.completion import Completer, Completion, CompleteEvent
from prompt_toolkit.document import Document
from typing import Iterable


class CommandCompleter(Completer):
    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        commands = ["new", "delete"]
        objects = ["node", "reaction", "force", "member"]
        input_command = document.current_line.split(" ")
        if len(input_command) == 1:
            for command in commands:
                if command.startswith(input_command[0]):
                    yield Completion(command, start_position=-len(input_command[0]))
        elif len(input_command) == 2:
            for obj in objects:
                if obj.startswith(input_command[1]):
                    yield Completion(obj, start_position=-len(input_command[1]))


completer = CommandCompleter()

session = PromptSession(completer=completer)


def main_loop():
    command: str = session.prompt(
        "> ",
    )
    for chunk in command.split(" "):
        print(chunk)
