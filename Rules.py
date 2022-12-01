import json


class Rules:
    def __init__(self, path: str):
        self.max_enters: int = 0

        with open(path, 'r') as file:
            rule = json.load(file)
        self.parse(rule)

    def parse(self, rules: dict):
        for rule in rules.keys():
            if rule == 'max_enters':
                self.max_enters = rules[rule]