from rules import Rules
from linter import Linter


def main():
    rules = Rules('C:\\Users\\portu\\Desktop\\Linter\\rules.json')
    path_code = "C:\\Users\\portu\\Desktop\\C#\\Общее\\Dis\\Dis_1\\Program.cs"
    linter = Linter(rules)
    linter.linter(path_code)


if __name__ == '__main__':
    main()
