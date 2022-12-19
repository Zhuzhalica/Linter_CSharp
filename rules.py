import json


class Rules:
    def __init__(self, path: str):
        self.max_enters: int = 0
        self.max_spaces: int = 0
        self.tabulation_size: int = 0
        self.transfer_after_bracket: bool = True
        self.alphabet_variable: list[str] = []
        self.is_camel_case: bool = True

        with open(path, 'r') as file:
            rule = json.load(file)
        self.parse(rule)

    def parse(self, rules: dict):
        for rule in rules.keys():
            if rule == 'max_enters':
                self.max_enters = rules[rule]
            elif rule == 'max_spaces':
                self.max_enters = rules[rule]
            elif rule == 'tabulation_size':
                self.tabulation_size = rules[rule]
            elif rule == 'transfer_after_bracket':
                self.transfer_after_bracket = rules[rule]
            elif rule == 'alphabet_variable':
                self.alphabet_variable = self.__parse_alphabet(rules[rule])
            elif rule == 'is_camel_case':
                self.is_camel_case = rules[rule]

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
