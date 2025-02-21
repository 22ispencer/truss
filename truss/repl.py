from prompt_toolkit import PromptSession, print_formatted_text as print

session = PromptSession()


def main_loop():
    in1 = session.prompt("> ")
    print(in1)
