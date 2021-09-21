from prompt_toolkit import prompt
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
import code

PROMPTS = {
    False: ">>> ",
    True: "... "
}


def main():
    c = code.InteractiveConsole()
    more = False
    while 1:
        user_input = prompt(PROMPTS[more],
                            history=FileHistory('history.txt'),
                            auto_suggest=AutoSuggestFromHistory(),
                            )
        for line in user_input.split('\n'):
            more = c.push(line)


if __name__ == '__main__':
    main()
