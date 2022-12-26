from rules import Rules
from linter import Linter


def main():
    # мы должны поддерживать ввод нескольких файлов, можно сделат как у маши с наташей
    rules = Rules('C:\\Users\\portu\\Desktop\\Linter\\rules.json')
    path_code = "C:\\Users\\portu\\Desktop\\Linter\\Program.cs"
    linter = Linter(rules)
    errors = linter.run(path_code)


if __name__ == '__main__':
    main()
