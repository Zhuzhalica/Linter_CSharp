from error import Error
from error_type import Error_type
from rules import Rules
import re


class Linter:
    def __init__(self, rules: Rules):
        self.rules: Rules = rules
        self.number_line: int = 1
        self.enters_count: int = 0
        self.offset_level: int = 0
        self.errors: list[Error] = []
        self.in_method: bool = False
        self.first_inner_line: bool = False

    def run(self, path_code: str) -> None:
        with open(path_code, 'r', encoding='UTF-8') as code:
            for line in code:
                # возможно стоит перенести проверки внутрь класса rules, но это мало что изменит, тогда просто он будет на 200 строк
                self.check_line_length(line)

                if self.in_method:
                    if self.first_inner_line:
                        self.check_bracket_line(line)
                        self.first_inner_line = False

                decls = self.is_method_declaration(line)
                if len(decls) > 0:
                    if self.in_method:
                        self.errors.append(
                            Error(Error_type.serious_error, self.number_line,
                                  (0, len(line)),
                                  "Method cannot be inside another method"))
                    else:
                        name = self.get_method_name(decls[0])
                        self.check_method_name(name)
                        self.in_method = True
                        self.first_inner_line = True

                # по идее у переменных внутри метода и внутри класса есть одинаковый способ объявления типо: "HashSet<int> T;", но при этом другие типы объявления внутри и вне метода отличются и не должны пересекаться (тоесть "public static  HashSet<int> T;" не может быть внутри метода, а var вне). Сейчас они могут быть везде
                decls = self.check_method_variable_declaration(line)
                if len(decls) > 0:
                    for decl in decls:
                        name = self.get_variable_name(decl)
                        self.check_variable_name(name)

                decls = self.check_class_variable_declaration(line)
                if len(decls) > 0:
                    for decl in decls:
                        self.check_class_variable_name(decl)

                if '{' in line or '}' in line:
                    self.check_bracket_line(line)

                self.check_spaces(line)
                self.check_enters(line)
                self.check_level_tabulation(line)
                self.check_count_tabulation(line)
                self.check_separate_symbol(line)

            self.number_line += 1

        if self.offset_level != 0:
            self.errors.append(
                Error(Error_type.serious_error, self.number_line,
                      (0, len(line)),
                      "Not all brackets are closed"))

    @staticmethod
    def is_method_declaration(line: str) -> list[str]:
        line = re.sub(r'\s+', ' ',
                      line.strip())  # заменяю все двойные, тройный и т.д. пробелы на одинарные
        temp = re.findall(
            r'(?:public |private |protected |internal )?'
            r'(?:static |abstract )?'
            r'(?:async )?'
            r'[\S]+ [\S]+[\s]?\(.*\)',
            line)  # патерн объявления метода

        return temp

    def check_spaces(self, line: str) -> None:
        line = line.lstrip()
        spaces_count = 0
        for i in range(len(line)):
            ch = line[i]
            if ch == ' ':
                spaces_count += 1
            else:
                if spaces_count > self.rules.max_spaces:
                    self.errors.append(
                        Error(Error_type.serious_error, self.number_line,
                              (0, len(line)),
                              "Extra spaces"))

                if ch in self.rules.characters_separated_spaces:
                    if line[i - 1] != ' ' or line[i + 1] != ' ':
                        self.errors.append(
                            Error(Error_type.serious_error, self.number_line,
                                  (0, len(line)),
                                  "There are no spaces around the operation"))

                if ch == '(':
                    if line[i - 1] == ' ':
                        self.errors.append(
                            Error(Error_type.serious_error, self.number_line,
                                  (0, len(line)),
                                  "Extra spaces before ("))

                spaces_count = 0

        if len(line) != len(line.rstrip()):
            self.errors.append(
                Error(Error_type.serious_error, self.number_line,
                      (0, len(line)),
                      "Extra spaces at the end of the line"))

    def check_count_tabulation(self, line: str) -> None:
        if len(line.lstrip()) + self.rules.tabulation_size * \
                self.offset_level != len(line):
            self.errors.append(
                Error(Error_type.serious_error, self.number_line,
                      (0, len(line)),
                      "Incorrect tab level"))

    def check_enters(self, line: str) -> None:
        if line.strip() == '':
            self.enters_count += 1
        else:
            if self.in_method:
                if self.enters_count > self.rules.max_enters:
                    self.errors.append(
                        Error(Error_type.serious_error, self.number_line,
                              (0, len(line)),
                              "Extra enters inside the method"))
            else:
                if self.enters_count > self.rules.max_enters_after_method or \
                        self.enters_count < self.rules.min_enters_after_method:
                    self.errors.append(
                        Error(Error_type.serious_error, self.number_line,
                              (0, len(line)),
                              "Extra enters around the method"))

    def check_level_tabulation(self, line: str) -> None:
        words = line.split(' ')
        for word in words:
            if word != '':
                if word == '{':
                    self.offset_level += 1
                if word == '}':
                    self.offset_level -= 1
                # после методов как for и т.д. может не быть скобок, если метод в одну строчку, надо это как-то обработать, но я не могу понять как это правильно сделать
                # if word in self.rules.tabulation_after_command:
                #     self.

    def check_method_name(self, name: str) -> None:
        self.check_correspondence_alphabet(name)

        if self.rules.method_pascal_case and name[0].islower():
            self.errors.append(
                Error(Error_type.serious_error, self.number_line,
                      (0, len(line)),
                      "Incorrect method name"))

    def check_variable_name(self, name: str):
        self.check_correspondence_alphabet(name)

        if self.rules.is_camel_case and name[0].isupper():
            self.errors.append(
                Error(Error_type.serious_error, self.number_line,
                      (0, len(line)),
                      "Incorrect variable name"))

    def check_correspondence_alphabet(self, name: str):
        for c in name:
            if c not in self.rules.alphabet_variable:
                self.errors.append(
                    Error(Error_type.serious_error, self.number_line,
                          (0, len(line)),
                          "The name does not match the allowed alphabet"))

    @staticmethod
    def get_method_name(declaration: str):
        ind = declaration.index('(')
        words = declaration[:ind].strip().split(' ')
        return words[len(words) - 1]

    def check_bracket_line(self, line: str) -> None:
        l = line.strip()
        if self.rules.bracket_separate_line and (l != '{' or l != '}'):
            self.errors.append(
                Error(Error_type.serious_error, self.number_line,
                      (0, len(line)),
                      "Characters in a string with a bracket"))

    @staticmethod
    def check_method_variable_declaration(line: str):
        line = re.sub(r'\s+', ' ',
                      line.strip())  # заменяю все двойные, тройный и т.д. пробелы на одинарные
        temp = re.findall(
            r'(?:var |[\S]+ )?'
            r'[\S]+\s?=\s?[\S]+',
            line)
        temp.extend(re.findall(
            r'(?:var |[\S]+ )?'
            r'[\S]+',
            line))

        return temp

    @staticmethod
    def get_variable_name(declaration: str):
        ind = declaration.index('=')
        if ind == -1:
            ind = declaration.index(';')
        if ind == -1:
            ind = len(declaration)

        words = declaration[:ind].strip().split(' ')
        return words[len(words) - 1]

    def check_line_length(self, line: str):
        if len(line) > self.rules.max_symbol_line:
            self.errors.append(
                Error(Error_type.serious_error, self.number_line,
                      (0, len(line)),
                      "Exceeding the number of characters in a string"))

    def check_separate_symbol(self, line: str):
        l = line.strip()
        parts = l.split(';')
        if len(parts) != 2 or parts[1] != '':
            self.errors.append(
                Error(Error_type.serious_error, self.number_line,
                      (l.index(';'), l.index(';')),
                      "Incorrect line separation"))

    @staticmethod
    def check_class_variable_declaration(line: str):
        line = re.sub(r'\s+', ' ',
                      line.strip())  # заменяю все двойные, тройный и т.д. пробелы на одинарные
        temp = re.findall(
            r'(?:public |private |protected |internal |)?'
            r'(?:static)?'
            r'[\S]+ [\S]+\s?=\s?[\S]+',
            line)
        temp.extend(re.findall(
            r'(?:public |private |protected |internal |)?'
            r'(?:static)?'
            r'[\S]+ [\S]+',
            line))
        return temp

    def check_class_variable_name(self, line: str):
        ind = line.index('=')
        if ind == -1:
            ind = line.index(';')
        if ind == -1:
            ind = len(line)

        decl = line[:ind]
        words = re.sub(r'\s+', ' ', decl.strip()).split(' ')
        name = words[len(words) - 1]
        if words[0] == 'private' or words[0] == 'static' or len(words) == 2:
            self.check_correspondence_alphabet(
                words[len(words) - 1].replace('_', ''))
            if name[0] != '_' or name[0].isupper():
                self.errors.append(
                    Error(Error_type.serious_error, self.number_line,
                          (0, len(line)),
                          "Incorrect variable name"))
        else:
            self.check_correspondence_alphabet(name)
            if name[0].islower():
                self.errors.append(
                    Error(Error_type.serious_error, self.number_line,
                          (0, len(line)),
                          "Incorrect variable name"))
