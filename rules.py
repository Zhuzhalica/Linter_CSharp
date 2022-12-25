import json


class Rules:
    def __init__(self, path: str):
        self.max_symbol_line: int = 0
        self.max_enters: int = 0
        self.min_enters_after_method: int = 0
        self.max_enters_after_method: int = 0
        self.max_spaces: int = 0
        self.tabulation_size: int = 0
        self.bracket_separate_line: bool = True
        self.alphabet_variable: list[str] = []
        self.is_camel_case: bool = True
        self.method_pascal_case: bool = True
        self.inner_variable_lowercase: bool = True
        self.tabulation_after_command: list[str] = []
        self.characters_separated_spaces: list[str] = []
        self.separate_symbol: str = ""

        with open(path, 'r') as file:
            rule = json.load(file)
        self.parse(rule)

    def parse(self, rules: dict):
        for rule in rules.keys():
            if rule == 'max_enters':
                self.max_enters = rules[rule]
            elif rule == 'min_enters_after_method':
                self.min_enters_after_method = rules[rule]
            elif rule == 'max_enters_after_method':
                self.max_enters_after_method = rules[rule]
            elif rule == 'max_spaces':
                self.max_enters = rules[rule]
            elif rule == 'tabulation_size':
                self.tabulation_size = rules[rule]
            elif rule == 'transfer_after_bracket':
                self.bracket_separate_line = rules[rule]
            elif rule == 'alphabet_variable':
                self.alphabet_variable = self.__parse_alphabet(rules[rule])
            elif rule == 'is_camel_case':
                self.is_camel_case = rules[rule]
            elif rule == 'method_pascal_case':
                self.method_pascal_case = rules[rule]
            elif rule == 'inner_variable_lowercase':
                self.inner_variable_lowercase = rules[rule]
            elif rule == 'tabulation_after_command':
                self.tabulation_after_command = rules[rule]
            elif rule == 'characters_separated_spaces':
                self.characters_separated_spaces = rules[rule]
            elif rule == 'max_symbol_line':
                self.max_symbol_line = rules[rule]
            elif rule == 'separate_symbol':
                self.separate_symbol = rules[rule]

    @staticmethod
    def __parse_alphabet(alphabet: list[str]):
        result: list[str] = []
        for symbol in alphabet:
            if '-' in symbol:
                temp = symbol.split('-')
                for i in range(ord(temp[0]), ord(temp[1])+1):
                    result.append(chr(i))
            else:
                result.append(symbol)
        return result
