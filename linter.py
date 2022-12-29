from error import Error
from error_type import Error_type
from rules import Rules
import re
from collections import defaultdict

class Linter:
    def __init__(self, rules: Rules):
        self.rules: Rules = rules
        self.number_line: int = 1
        self.enters_count: int = 0
        self.offset_level: int = 0
        self.errors: list[Error] = []
        self.dict_variables: defaultdict[str, list[int]] = defaultdict(list)
        self.dict_methods: defaultdict[str, list[int]] = defaultdict(list)
        self.in_method: bool = False
        self.first_inner_line_method: bool = False
        self.first_inner_line_func: bool = False
        self.tabs_check: bool = True
        self.separator_check: bool = True
        self.variable_check: bool = False
        self.method_start_offset_level: int = -1

    def run(self, path_code: str) -> list[Error]:
        with open(path_code, 'r', encoding='UTF-8') as code:
            for line in code:
                first_word = line.strip().split(' ')[0]
                self.check_line_length(line)
                self.configure_options(first_word)
                self.check_enters(line)
                line = line.replace("\n", "")
                self.check_first_line_in_method(line)
                self.check_content_method_in_method(line)
                if self.variable_check:
                    self.check_variable(line)

                if '{' in line or '}' in line:
                    self.check_bracket_line(line)

                if self.tabs_check:
                    self.check_count_tabulation(line)
                else:
                    self.tabs_check = True

                self.calculate_level_tabulation(line)
                self.check_method_end()
                self.check_spaces(line)
                if self.separator_check:
                    self.check_separate_symbol(line)
                else:
                    self.separator_check = True
                self.check_variable_usage_line(line)
                self.number_line += 1

        self.check_closed_brackets(line)
        self.check_variables_usage()
        self.print_errors()
        return self.errors

    def configure_options(self, word):
        if word == 'namespace':
            self.separator_check = False
        if word == 'class':
            self.separator_check = False
            self.variable_check = True
        if word in self.rules.tabulation_after_command:
            self.separator_check = False

    def check_first_line_in_method(self, line):
        if self.in_method:
            if self.first_inner_line_method:
                self.check_bracket_line(line)
                self.first_inner_line_method = False
        if self.first_inner_line_func:
            self.first_inner_line_func = False
            if '{' in line:
                self.check_bracket_line(line)
            else:
                self.offset_level += 1
                self.check_count_tabulation(line)
                self.offset_level -= 1
                self.tabs_check = False

    def check_method_end(self):
        if self.method_start_offset_level != -1 and \
                self.method_start_offset_level == self.offset_level and \
                not self.first_inner_line_method:
            self.in_method = False
            self.method_start_offset_level = -1

    def check_content_method_in_method(self, line):
        decls = self.find_method_declaration(line)
        if len(decls) > 0:
            self.separator_check = False
            if self.in_method:
                self.errors.append(
                    Error(Error_type.serious_error, self.number_line,
                          (0, len(line)),
                          "Method cannot be inside another method"))
            else:
                self.method_start_offset_level = self.offset_level
                name = self.get_method_name(decls[0])
                self.check_method_name(name)
                self.in_method = True
                self.first_inner_line_method = True

    def check_closed_brackets(self, line):
        if self.offset_level != 0:
            self.errors.append(
                Error(Error_type.serious_error, self.number_line,
                      (0, len(line)),
                      "Not all brackets are closed"))

    def print_errors(self):
        for error in sorted(self.errors, key=lambda e: e.number_line):
            print(f'{error.number_line}: {error.text}')

    def check_variable(self, line):
        variable_decls = self.find_common_variable_declaration(line)

        decls = self.find_methods_variable_declaration(line)
        if len(decls) > 0:
            if self.in_method:
                decls.extend(variable_decls)
                for decl in decls:
                    name = self.get_variable_name(decl)
                    self.check_variable_name(name)
            else:
                self.errors.append(
                    Error(Error_type.serious_error,
                          self.number_line,
                          (0, len(line)),
                          "Incorrect way to declare a variable"))

        decls = self.find_classes_variable_declaration(line)
        if len(decls) > 0:
            if not self.in_method:
                decls.extend(variable_decls)
                for decl in decls:
                    self.check_class_variable_name(decl)
            else:
                self.errors.append(
                    Error(Error_type.serious_error,
                          self.number_line,
                          (0, len(line)),
                          "Incorrect way to declare a variable"))

    @staticmethod
    def find_method_declaration(line: str) -> list[str]:
        line = re.sub(r'\s+', ' ', line.strip())
        temp = re.findall(
            r'(?:^public |^private |^protected |^internal )?'
            r'(?:static |abstract |^static |^abstract )?'
            r'(?:[^\s]+|^[^\s]+) [^\s\.><]+[\s]?\(.*\)$',
            line)

        return temp

    @staticmethod
    def get_method_name(declaration: str):
        ind = declaration.index('(')
        words = declaration[:ind].strip().split(' ')
        return words[len(words) - 1]

    def check_method_name(self, name: str) -> None:
        self.check_correspondence_alphabet(name)
        self.dict_methods[name].append(self.number_line)
        if self.rules.method_pascal_case and name[0].islower():
            self.errors.append(
                Error(Error_type.serious_error, self.number_line,
                      (0, 0),
                      "Incorrect method name"))


    @staticmethod
    def find_common_variable_declaration(line: str) -> list[str]:
        line = re.sub(r'\s+', ' ', line.strip())
        temp = re.findall(r'[\S]+ [^\s\.]+\s?=\s?[\S]+\s?[;]?', line)
        temp.extend(re.findall(r'^[\S]+ [\S]+\s?[;]?$', line))
        result = []
        for t in temp:
            first_word = t.split(' ')[0]
            if first_word != "using" and first_word != "namespace" and \
                    first_word != "class" and first_word != "var":
                result.append(t)

        return result

    @staticmethod
    def find_methods_variable_declaration(line: str):
        line = re.sub(r'\s+', ' ', line.strip())
        temp = re.findall(r'^var [\S]+\s?=\s?.+\s?[;]?$', line)

        return temp

    @staticmethod
    def find_classes_variable_declaration(line: str):
        line = re.sub(r'\s+', ' ', line.strip())
        temp = re.findall(
            r'(?:^public |^private |^protected |^internal )'
            r'(?:static)?'
            r'[\S]+ [\S]+\s?=\s?[\S]+\s?[;]?$',
            line)
        temp.extend(re.findall(
            r'(?:^public |^private |^protected |^internal )'
            r'(?:static)?'
            r'[\S]+ [\S]+\s?[;]?$',
            line))
        temp.extend(re.findall(
            r'^static [\S]+ [\S]+\s?[;]?$',
            line))
        temp.extend(re.findall(
            r'^static [\S]+ [\S]+\s?=\s?[\S]+\s?[;]?$',
            line))
        return temp

    @staticmethod
    def get_variable_name(declaration: str):
        ind = declaration.find('=')
        if ind == -1:
            ind = declaration.find(';')
        if ind == -1:
            ind = len(declaration)

        words = declaration[:ind].strip().split(' ')
        return words[len(words) - 1]

    def check_variable_name(self, name: str):
        self.dict_variables[name].append(self.number_line)
        self.check_correspondence_alphabet(name)
        if self.rules.is_camel_case and name[0].isupper():
            self.errors.append(
                Error(Error_type.serious_error, self.number_line,
                      (0, 0),
                      "Incorrect variable name"))

    def check_variables_usage(self):
        for variable in self.dict_variables:
            numbers_line = self.dict_variables[variable]
            if len(numbers_line) <= 2:
                self.errors.append(Error(Error_type.serious_error, numbers_line[0],
                                   (0,0), f"The variable '{variable}' is declared but not used"))

    def check_variable_usage_line(self, text):
        for name in self.dict_variables:
            all_occurrences = [_ for _ in re.finditer(name, text)]
            for i in range(len(all_occurrences)):
                occurrence = all_occurrences[i]
                if not (text[occurrence.start()-1].isalpha() or text[occurrence.start()-1].isdigit() or text[occurrence.end()].isalpha() or text[occurrence.end()].isdigit()):
                    self.dict_variables[name].append(self.number_line)

    def check_correspondence_alphabet(self, name: str):
        for c in name:
            if c not in self.rules.alphabet_variable:
                self.errors.append(
                    Error(Error_type.serious_error, self.number_line,
                          (0, 0),
                          "The name does not match the allowed alphabet"))

    def check_class_variable_name(self, line: str):
        ind = line.find('=')
        if ind == -1:
            ind = line.find(';')
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

    def check_line_length(self, line: str):
        if len(line) > self.rules.max_symbol_line:
            self.errors.append(
                Error(Error_type.serious_error, self.number_line,
                      (0, len(line)),
                      "Exceeding the number of characters in a string"))

    def check_separate_symbol(self, line: str):
        l = line.strip()
        if not self.first_inner_line_func and \
                not self.first_inner_line_method and \
                '{' not in l and '}' not in l and line != '':

            parts = l.split(';')
            if len(parts) != 2 or parts[1] != '':
                self.errors.append(
                    Error(Error_type.serious_error, self.number_line,
                          (0, 0),
                          "Incorrect line separation"))

    def check_count_tabulation(self, line: str) -> None:
        if line.strip() != '' and '}' not in line:
            if len(line.lstrip()) + self.rules.tabulation_size * \
                    self.offset_level != len(line):
                self.errors.append(
                    Error(Error_type.serious_error, self.number_line,
                          (0, len(line)),
                          "Incorrect tab level"))

    def calculate_level_tabulation(self, line: str) -> None:
        words = line.split(' ')
        for word in words:
            if word != '':
                if word == '{':
                    self.offset_level += 1
                elif word == '}':
                    self.offset_level -= 1
                elif word in self.rules.tabulation_after_command:
                    self.first_inner_line_func = True

    def check_enters(self, line: str) -> None:
        if line.strip() == '':
            self.enters_count += 1
        else:
            self.enters_count = 0
            if self.enters_count > self.rules.max_enters:
                self.errors.append(
                    Error(Error_type.serious_error, self.number_line,
                          (0, len(line)),
                          "Extra enters inside the method"))

    def check_bracket_line(self, line: str) -> None:
        l = line.strip()
        if self.rules.bracket_separate_line and l != '{' and l != '}':
            self.errors.append(
                Error(Error_type.serious_error, self.number_line,
                      (0, len(line)),
                      "Characters in a string with a bracket"))

    def check_spaces(self, line: str) -> None:
        line = line.lstrip().replace('\n', '')
        first_word = line.split(' ')[0]
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
                        if ch == '=' and line[i + 1] != '>':
                            self.errors.append(
                                Error(Error_type.serious_error,
                                      self.number_line,
                                      (0, len(line)),
                                      "There are no spaces around the operation"))

                if first_word not in self.rules.tabulation_after_command and \
                        ch == '(':
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
