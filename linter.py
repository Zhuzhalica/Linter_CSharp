from Rules import Rules


class Linter:
    def __init__(self, rules: Rules):
        self.rules = rules
        self.enters_count = 0

    def linter(self, path_code: str):
        with open(path_code, 'r', encoding='UTF-8') as code:
            for line in code:
                if line == '\n':
                    self.enters_count += 1
                else:
                    self.enters_count = 0

                self.check()

    def check(self):
        if self.enters_count > self.rules.max_enters:
            print("Warning")
