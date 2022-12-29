import unittest
from rules import Rules

class TestRules(unittest.TestCase):
    def setUp(self):
        self.rules = Rules('C:\\Users\\German\\Linter_CSharp\\Tests\\r1.json')

    def test_parse_max_enters(self):
        self.assertEqual(self.rules.max_enters, 1)

    def test_parse_max_symbol_line(self):
        self.assertEqual(self.rules.max_symbol_line, 120)

    #def test_parse_min_enters_after_method(self):
    #    self.assertEqual(self.rules.min_enters, 1)

    def test_parse_tabulation_size(self):
        self.assertEqual(self.rules.tabulation_size, 4)

    def test_parse_max_enters_after_method(self):
        self.assertEqual(self.rules.max_enters, 1)

    def test_check_parse_max_spaces(self):
        self.assertEqual(self.rules.max_spaces, 1)

    def test_check_parse_tabulation_size(self):
        self.assertEqual(self.rules.tabulation_size, 4)

    def test_check_parse_bracket_separate_line(self):
        self.assertTrue(self.rules.bracket_separate_line)

    def test_check_parse_alphabet_variable(self):
        self.assertEqual(len(self.rules.alphabet_variable), 52)

    def test_check_parse_camel_case(self):
        self.assertTrue(self.rules.is_camel_case)

    def test_parse_pascal_case(self):
        self.assertTrue(self.rules.method_pascal_case)

    def test_parse_inner_variable_lowercase(self):
        self.assertTrue(self.rules.inner_variable_lowercase)

    def test_parse_tabulation_after_command(self):
        self.assertEqual(len(self.rules.tabulation_after_command), 9)

    def test_parse_characters_separated_spaces(self):
        self.assertEqual(len(self.rules.characters_separated_spaces), 14)

    def test_parse_separate_symbol(self):
        self.assertEqual(self.rules.separate_symbol, ";")



