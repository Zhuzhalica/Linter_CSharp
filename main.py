import sys
from tkinter import Tk
from tkinter.filedialog import askopenfilenames, askopenfilename
from rules import Rules
from linter import Linter
from colorama import init

sys.tracebacklimit = 0


def main():
    finish, rule_path, code_paths = console_args_processing()

    if not finish:
        init(autoreset=True)

        if rule_path == "":
            Tk().withdraw()
            rule_path = askopenfilename(title='Open a file',
                                        filetypes=[("Rules", "*.json")])
        rules = Rules(rule_path)

        if len(code_paths) == 0:
            Tk().withdraw()
            code_paths = askopenfilenames(title='Open a file',
                                          filetypes=[("C# File", "*.cs")])

        for path in code_paths:
            linter = Linter(rules)
            errors = linter.run(path)
            print(path)
            for error in sorted(errors, key=lambda e: e.number_line):
                print(error)
            print("\n")


def console_args_processing() -> tuple[bool, str, list[str]]:
    rule_path: str = ""
    code_paths: list[str] = []
    for i in range(0, len(sys.argv)):
        arg = sys.argv[i]

        if '--help' in arg or '-h' in arg:
            if len(sys.argv) == 2:
                with open('help.txt', 'r', encoding="utf-8") as file:
                    for line in file.readlines():
                        sys.stdout.write(line + '\n')
            else:
                raise ValueError("With console command --help or -h there can "
                                 "be no other commands")
            return True, rule_path, code_paths
        if '--pathR=' in arg or '-pr=' in arg:
            rule_path = arg.split('=')[1]
            if rule_path.split('.')[1] != "json":
                raise ValueError("Invalid file format: valid is .json")
        if '--pathC=' in arg or '-pc=' in arg:
            code_paths.append(arg.split('=')[1])
            if code_paths[0].split('.')[1] != "cs":
                raise ValueError("Invalid file format: valid is .cs")

    return False, rule_path, code_paths


if __name__ == '__main__':
    main()
