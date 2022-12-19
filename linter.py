from rules import Rules


class Linter:
    def __init__(self, rules: Rules):
        self.rules = rules
        self.enters_count: int = 0
        self.spaces_count_: int = 0
        self.extra_spaces_end: bool = False
        self.offset_level: int = 0
        self.tabulation_error: bool = False
        self.name_error: bool = False

    def linter(self, path_code: str):
        with open(path_code, 'r', encoding='UTF-8') as code:
            i = 1
            for line in code:
                self.line_setup()

                if line == '\n':
                    self.enters_count += 1
                else:
                    self.enters_count = 0
                    line = line.replace('\n', '')

                    temp = line.lstrip()
                    if len(temp) + self.rules.tabulation_size * \
                            self.offset_level != len(line):
                        self.tabulation_error = True

                    temp = temp.split(' ')
                    for j in range(len(temp)):
                        word = temp[j]
                        if word == '':
                            self.spaces_count_ += 1
                        if word == '{':
                            self.offset_level += 1
                        if word == '}':
                            self.offset_level -= 1
                            self.tabulation_error = False
                        if word == '=' and temp[j - 2] == 'var':
                            self.check_variable(temp[j - 1])

                    if len(line) != len(line.rstrip()):
                        self.extra_spaces_end = True

                self.check(i)
                i += 1

    def check(self, i: int):
        if self.enters_count > self.rules.max_enters:
            print(f"{i}: Warning enters")
        if self.spaces_count_ > self.rules.max_spaces:
            print(f"{i}: Warning spaces between words")
        if self.extra_spaces_end:
            print(f"{i}: Warning spaces in the end")
        if self.tabulation_error:
            print(f"{i}: Warning tabulation")
        if self.name_error:
            print(f"{i}: Warning name variable")

    def line_setup(self):
        self.spaces_count_ = False
        self.extra_spaces_end = False
        self.tabulation_error = False
        self.name_error = False

    def check_variable(self, variable: str):
        for c in variable:
            if c not in self.rules.alphabet_variable:
                self.name_error = True

        if (variable[0].islower() and not self.rules.is_camel_case) or \
                (variable[0].isupper() and self.rules.is_camel_case):
            self.name_error = True
