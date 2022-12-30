from rules import Rules
from linter import Linter
from colorama import init

def main():
    init(autoreset=True)
    rules = Rules('C:\\Users\\German\\Linter_CSharp\\rules.json')
    path_code = "C:\\Users\\German\\Linter_CSharp\\Program.cs"
    linter = Linter(rules)
    errors = linter.run(path_code)
    for error in sorted(errors, key=lambda e: e.number_line):
        print(error)


if __name__ == '__main__':
    main()
